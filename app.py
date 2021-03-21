# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, request,json,session,render_template,jsonify
import re
from functions import get_weather,make_calendar,home_dashboard,thread_page,ago,get_page
import db_functions
import datetime
import pandas as pd
import numpy as np
import json
import requests
import re
import math
import pymysql
from dateutil.relativedelta import relativedelta
from datetime import datetime,date,timedelta

con = pymysql.connect('localhost', 'root', 'Karelia', 'geo_data')

#export FLASK_ENV=development

app = Flask(__name__)
app.secret_key = 'ironpond'

@app.route('/login/', methods = ['POST', 'GET'])
def login_page():
	if request.method == 'POST':
		email_username = request.form['email_username']
		password = request.form['password']
		data = db_functions.check_user(email_username,password)
		username = data[0][0]
		email = data[0][1]
		home_town = data[0][2]
		session.permanent = True
		session['username'] = username
		session['hometown'] = home_town.split(',')[0]
		session['log_time'] = datetime.now()
		message = '{} succesfully logged in!'.format(username)
		session['message'] = message
		return redirect(url_for('index'))
	return render_template('login.html')
	

@app.route('/user_validation', methods=['POST'])
def user_validation():
	email_username = request.form['email_username']
	password = request.form['password']
	data = db_functions.check_user(email_username,password)
	if len(data) == 0:
		return jsonify({'error':'no user found'})
	return jsonify({'success':'user found'})

@app.route('/create_profile/', methods = ['POST', 'GET'])
def create_profile():
	if request.method == 'POST':
		email = request.form['email']
		username = request.form['username']
		home_town = request.form['home_town']
		password = request.form['password']
		db_functions.create_new_user(username,email,home_town,password)
		message = 'username {} was succesfully created. now logged in!'.format(username)
		session.permanent = True
		session['username'] = username
		session['message'] = message
		session['hometown'] = home_town
		session['log_time'] = datetime.now()
		return redirect(url_for('index'))
	return render_template('create_profile.html')


@app.route('/profile_validation', methods=['POST'])
def profile_validation():
	username = request.form['username']
	email = request.form['email']
	data = db_functions.check_new_user(email,username)
	if data:
		return jsonify({'error':'that email or username is taken. please use a different one.'})
	return jsonify({'success':'looks good'})

@app.route("/<username>/")
def user_profile(username):
	user_profile = db_functions.user_profile_get(username)
	return render_template("user_profile.html",user_profile=user_profile)


@app.route("/")
def index():
	if 'message' in session:
		message = session['message']
		session.pop('message', None)
		if 'username' in session:
			social_header,summary,next_task = home_dashboard(session['hometown'],session['username'])
			session['weather_summary'] = summary
			return render_template("index.html",message=message,social_header=social_header,summary=summary,next_task=next_task)
		else:
			session.clear()
			return render_template("index.html",message=message)
			
	elif 'username' in session:
		diff_weather_log = session['log_time'] - datetime.strptime(session['weather_summary']['forecast_time'],'%Y-%m-%d %H:%M')
		diff_weather_log = ((diff_weather_log.seconds//60))
		print('difference between log time and forecast summary is %s'%diff_weather_log)
		if diff_weather_log < 120:
			social_header = db_functions.home_crud_first()
			next_task = db_functions.calendar_dashboard(session['username'])
			summary = session['weather_summary']
			session['log_time'] = datetime.now()
			return render_template("index.html",social_header=social_header,summary=summary,next_task=next_task)
		elif diff_weather_log > 120:
			social_header,summary,next_task = home_dashboard(session['hometown'],session['username'])
			session['log_time'] = datetime.now()
			session['weather_summary'] = summary
			return render_template("index.html",social_header=social_header,summary=summary,next_task=next_task)
		else:
			print('else')
			social_header,summary,next_task = home_dashboard(session['hometown'],session['username'])
			session['weather_summary'] = summary
			return render_template("index.html",social_header=social_header,summary=summary,next_task=next_task)
	else:
		return render_template("index.html")

@app.route("/calendar/<date>",methods = ['POST', 'GET'])
def home_calendar(date):
	date = datetime.strptime(date,'%Y-%m')
	if request.method == 'POST':
		date = request.form['date']
		year_month = datetime.strptime(date,'%Y-%m-%d').strftime('%Y-%m')
		day = datetime.strptime(date,'%Y-%m-%d').strftime('%d')
		return redirect(url_for('calendar',year_month=year_month,day=day))
	else:
		if 'username' in session:
			state = 'enabled'
			title,framer = make_calendar(date,session['username'])
			next_month = date + relativedelta(months=1)
			prev_month =  date - relativedelta(months=1)
			if 'message' in session:
				message = session['message']
				session.pop('message',None)
				return render_template("calendar.html",framer=framer,title=title,date=date,next_month=next_month,prev_month=prev_month,state=state,message=message)
			else:
				return render_template("calendar.html",framer=framer,title=title,date=date,next_month=next_month,prev_month=prev_month,state=state)
		else:
			title,framer = make_calendar(date)
			next_month = date + relativedelta(months=1)
			prev_month =  date - relativedelta(months=1)
			return render_template("calendar.html",framer=framer,title=title,date=date,next_month=next_month,prev_month=prev_month,state='disabled')

@app.route("/calendar/<year_month>/<day>",methods = ['POST', 'GET'])
def calendar(year_month,day):
	day = pd.to_datetime(year_month +'-'+ day).strftime('%Y-%m-%d')
	times = [str(pd.to_datetime(day) + timedelta(hours = int(i))) for i in np.arange(0,25)]
	if request.method == 'POST':
		checked = [i == '' for i in request.form.values()]
		try:
			if any(checked) == True:
				message = 'please mark all fields!'
				day_data = db_functions.check_day_tasks(day,session['username'])
				title = datetime.strptime(day,'%Y-%m-%d').strftime('%A, %B %d,%Y')
				return render_template("to_do.html",title=title,times=times,day_data=day_data,message=message)
				
			else:
				if 'whole_day' in request.form:
					if db_functions.check_day_tasks(day,session['username']):
						message = '{} tasks already exists for those times!'.format(len(db_functions.check_day_tasks(day,session['username'])))
						day_data = db_functions.check_day_tasks(day,session['username'])
						title = datetime.strptime(day,'%Y-%m-%d').strftime('%B %d,%Y')
						return render_template("to_do.html",title=title,times=times,day_data=day_data,message=message)
					else:
						start_time = datetime.strptime(day,'%Y-%m-%d')
						end_time = start_time + timedelta(hours = 24)
						username = session['username']
						category = request.form['category']
						post = request.form['post']
						message = 'task {} added on {} for the whole day!'.format(category,day)
						session['message'] = message
						db_functions.create_new_task(start_time,end_time,username,category,post)
						return redirect(url_for('home_calendar',date=year_month))
				elif 'start_time' and 'end_time' in request.form:
					start_time = request.form['start_time']
					end_time = request.form['end_time']
					username = session['username']
					category = request.form['category']
					post = request.form['post']
					date_string = pd.date_range(start_time,end_time,freq='H').astype(str).to_list()[:-1]
					day_data = pd.DataFrame(db_functions.check_day_tasks(day,session['username']))
					check_slots = [any(item in date_string for item in pd.date_range(i[0],i[1],freq='H').astype(str).to_list()[:-1])  for i in day_data[day_data.columns[0:2]].values]
					if any(check_slots):
						message = '{} tasks already exists for those times!'.format(sum(check_slots))
						day_data = db_functions.check_day_tasks(day,session['username'])
						title = datetime.strptime(day,'%Y-%m-%d').strftime('%B %d,%Y')
						return render_template("to_do.html",title=title,times=times,day_data=day_data,message=message)
					else:
						message = 'task {} for {} between {} and {}'.format(category,day,pd.to_datetime(start_time).strftime('%H:%M'),pd.to_datetime(end_time).strftime('%H:%M'))
						session['message'] = message
						db_functions.create_new_task(start_time,end_time,username,category,post)
						return redirect(url_for('home_calendar',date=year_month))
				elif 'start_time' or 'end_time'  not in request.form:
					message = 'please mark all fields!'
					day_data = db_functions.check_day_tasks(day,session['username'])
					title = datetime.strptime(day,'%Y-%m-%d').strftime('%A, %B %d,%Y')
					return render_template("to_do.html",title=title,times=times,day_data=day_data,message=message)
		except:
			message = 'please mark all fields!'
			day_data = db_functions.check_day_tasks(day,session['username'])
			title = datetime.strptime(day,'%Y-%m-%d').strftime('%A, %B %d,%Y')
			return render_template("to_do.html",title=title,times=times,day_data=day_data,message=message)
	
	day_data = db_functions.check_day_tasks(day,session['username'])
	title = datetime.strptime(day,'%Y-%m-%d').strftime('%A, %B %d,%Y')
	return render_template("to_do.html",title=title,times=times,day_data=day_data)



@app.route('/logout/')
def logout():
	message = 'username {} was succesfully logged out!'.format(session['username'])
	session['message'] = message
	session.pop('username', None)
	return redirect(url_for('index'))


@app.context_processor
def crud_component():
	crud_read = db_functions.crud_header()
	return {'crud_read':crud_read}
	
	
@app.route('/forum/<thread>/',methods=['POST','GET'])
def forum_thread(thread):
	if request.method == 'POST':
		if 'reply' in request.form: 
				if any(request.form['reply']):
					thread_id, reply,username = request.form['thread_id'], request.form['username'],request.form['reply']
					db_functions.thread_reply(thread_id,reply,username)
					thread,replies,reply_reply = thread_page(thread)
					return render_template('thread.html',thread=thread,replies=replies,reply_reply= reply_reply)
				else:
					thread,replies,reply_reply = thread_page(thread)
					error_message='please fill in the reply!'
					return render_template('thread.html',thread=thread,replies=replies,reply_reply= reply_reply,error_message=error_message)
		elif 'reply_to_replier' in request.form:
			input_reply = request.form['reply_to_replier']
			input_username = request.form['session_to_replier']
			input_reply_id = request.form['reply_to_reply_id']
			db_functions.reply_reply(input_reply_id,input_username,input_reply)
			thread,replies,reply_reply =thread_page(thread)
			return render_template('thread.html',thread=thread,replies=replies,reply_reply= reply_reply)
		
	thread,replies,reply_reply = thread_page(thread)
	return render_template('thread.html',thread=thread,replies=replies,reply_reply=reply_reply)
	
@app.route('/forum/',methods=['POST','GET'])
def forum():
	if request.method == 'POST':
		if request.form.get('category'):
			message = 'post added!'
			username = session['username']
			category = request.form['category']
			post = request.form['post']
			db_functions.crud_insert(category,post,username)
			return render_template('forum.html',message=message)
		elif request.form.get('delete'):
			message = 'post deleted!'
			delete_id = request.form['delete']
			db_functions.crud_delete(delete_id)
			return render_template('forum.html',message=message)
		elif request.form.get('edit'):
			edit_string = request.form['edit']
			title, post = db_functions.crud_edit(edit_string)
			return render_template('forum.html',title=title,post=post,edit_string=edit_string)
		elif request.form.get('update_post'):
			message = 'post updated!'
			edit_string = request.form['update_id']
			update_cat = request.form['update_category']
			update_post = request.form['update_post']
			db_functions.crud_update(edit_string,update_cat,update_post)
			return render_template('forum.html',message=message)
		else:
			error_message = 'please fill in all fields!'
			return render_template('forum.html',error_message=error_message)
	return render_template('forum.html')	

@app.route('/weather/',methods = ['POST', 'GET']) 
def enter_city(): 
	if request.method == 'POST':
		city = request.form['city']
		return redirect(url_for('weather_city', city = city))
	elif request.method == 'GET':
		return render_template("weather.html")

@app.route('/weather/<city>') 
def weather_city(city):
	try:
		table,summary,server_city,maxt,mint,dates = get_weather(city)
		return render_template("weather_city.html", table=table,summary=summary,server_city=server_city,maxt=maxt,mint=mint,dates=dates,city=city)
	except:
		message = 'forecast not found for {}.'.format(city)
		return render_template("weather_city.html",message = message)

@app.context_processor
def inject_now():
	return {'now': datetime.now()}
	
@app.template_filter()
def render_ago(stamp):
	time_string = ago(stamp)
	return time_string

@app.template_filter()
def thousandsFormat(value):
	value = int(value)
	return "{:,}".format(value)
    
@app.errorhandler(404)
def page_not_found(e):
	error = e
	return render_template('404.html',error=error), 404


'''testing highcharts here'''


@app.route('/graph/')
def graph(chartID = 'population'):
	columns,municipality,population = db_functions.top_10_pop()
	chart_type = 'column'
	title = 'hello'
	return render_template('graph.html',chart_type=chart_type,population=population,municipality=municipality,title=columns[0],subtitle=columns[1])


@app.route('/forum_validation', methods=['POST'])
def forum_validation():
	query = request.form['query']
	data = db_functions.search_forums(query)
	if not data:
		return jsonify({'error':'umm yeah nothing'})
	return jsonify({'success':'looks good'})
	

@app.route('/thread_edit_ajax', methods=['POST'])
def thread_edit_ajax():
	thread_id = request.form['thread_id']
	edited_title = request.form['edited_title']
	edited_post = request.form['edited_post']
	db_functions.crud_update(thread_id,edited_title,edited_post)
	return jsonify({'success':'done'})

@app.route("/test/<int:page>/",methods=['GET','POST'])
@app.route("/test/sort_by=<sort_key>&ascending=<ascending>/<int:page>",methods=['GET','POST'])
def test(page,sort_key=None,ascending=None):
	crud_read = db_functions.crud_header()
	pages = math.ceil(len(crud_read) / 5)
	pagination = np.arange(0,pages) + 1
	if 'query' in request.form:
		query = request.form['query']
		return redirect(url_for('test_results',query=query,page=1))
	elif 'post' in request.form:
		title = request.form['title']
		post = request.form['post']
		username = session['username']
		db_functions.crud_insert(title,post,username)
		session['post_added'] = 'post added!'
		return redirect(url_for('test',page=1))
	elif 'title' in request.form:
		if request.form['last']  == 'title':
			ascending = not json.loads(ascending.lower())
			return redirect(url_for('test',page=page,sort_key='title',ascending=ascending))
		ascending= True
		return redirect(url_for('test',page=page,sort_key='title',ascending=ascending))
	elif 'username' in request.form:
		if request.form['last']  == 'username':
			ascending = not json.loads(ascending.lower())
			return redirect(url_for('test',page=page,sort_key='username',ascending=ascending))
		return redirect(url_for('test',page=page,sort_key='username',ascending=True))
	elif 'stamp' in request.form:
		if request.form['last']  == 'stamp':
			ascending = not json.loads(ascending.lower())
			return redirect(url_for('test',page=page,sort_key='stamp',ascending=ascending))
		return redirect(url_for('test',page=page,sort_key='stamp',ascending=True))
	elif sort_key and ascending:
		new_table = get_page(page,crud_read,sort_key,ascending)
		return render_template('test.html',new_table=new_table,pagination=pagination,current_page=page,last=sort_key,sort_key=sort_key,ascending=ascending)
	new_table = get_page(page,crud_read)
	if 'post_added' in session:
		post_success = session['post_added']
		session.pop('post_added',None)
		return render_template('test.html',new_table=new_table,pagination=pagination,current_page=page,post_success=post_success)
	return render_template('test.html',new_table=new_table,pagination=pagination,current_page=page)
	
	
@app.route("/test/query=<query>/<int:page>/",methods=['GET','POST'])
@app.route("/test/query=<query>&sort_by=<sort_key>&ascending=<ascending>/<int:page>",methods=['GET','POST'])
def test_results(query,page,sort_key=None,ascending=None):
	crud_read = db_functions.search_forums(query)
	pages = math.ceil(len(crud_read) / 5)
	pagination = np.arange(0,pages) + 1
	if 'query' in request.form:
		query = request.form['query']
		return redirect(url_for('test_results',query=query,page=1))
	elif 'post' in request.form:
		title = request.form['title']
		post = request.form['post']
		username = session['username']
		db_functions.crud_insert(title,post,username)
		session['post_added'] = 'post added!'
		'''
		crud_read = db_functions.crud_header()
		pages = math.ceil(len(crud_read) / 5)
		pagination = np.arange(0,pages) + 1
		new_table = get_page(1,crud_read)
		return render_template('test.html',new_table=new_table,pagination=pagination,current_page=1,message='post added!')
		'''
		return redirect(url_for('test',page=1))
	elif 'title' in request.form:
		if request.form['last']  == 'title':
			ascending = not json.loads(ascending.lower())
			return redirect(url_for('test_results',query=query,page=page,sort_key='title',ascending=ascending))
		ascending= True
		return redirect(url_for('test_results',query=query,page=page,sort_key='title',ascending=ascending))
	elif 'username' in request.form:
		if request.form['last']  == 'username':
			ascending = not json.loads(ascending.lower())
			return redirect(url_for('test_results',query=query,page=page,sort_key='username',ascending=ascending))
		ascending= True
		return redirect(url_for('test_results',query=query,page=page,sort_key='username',ascending=ascending))
	elif 'stamp' in request.form:
		if request.form['last']  == 'stamp':
			ascending = not json.loads(ascending.lower())
			return redirect(url_for('test_results',query=query,page=page,sort_key='stamp',ascending=ascending))
		ascending= True
		return redirect(url_for('test_results',query=query,page=page,sort_key='stamp',ascending=ascending))
	elif sort_key and ascending:
		new_table = get_page(page,crud_read,sort_key,ascending)
		return render_template('test_query.html',new_table=new_table,pagination=pagination,current_page=page,last=sort_key,sort_key=sort_key,ascending=ascending,query=query)
	new_table = get_page(page,crud_read) 
	return render_template('test_query.html',new_table=new_table,pagination=pagination,current_page=page,query=query)
	


    #print(url_for('login'))
    #print(url_for('login', next='/'))
    #print(url_for('profile', username='John Doe'))
'''
@app.route("/test/query=<query>/<int:page>/",methods=['GET','POST'])
def test_results(query,page):
	if request.form:
		query = request.form['query']
		return redirect(url_for('test_results',query=query,page=page))
	crud_read = db_functions.search_forums(query)
	pages = math.ceil(len(crud_read) / 5)
	pagination = np.arange(0,pages) + 1
	new_table = get_page(page,crud_read)  
	return render_template('test_query.html',new_table=new_table,pagination=pagination,current_page=page,query=query)


elif 'username' in request.form:
	return redirect(url_for('test',page=page,sort_key='username',ascending=True))
elif 'stamp' in request.form:
	return redirect(url_for('test',page=page,sort_key='stamp',ascending=True))
@app.route("/test/<int:page>/",methods=['GET','POST'])
@app.route("/test/<int:page>/sort_by=<sort_key>&ascending=<ascending>",methods=['GET','POST'])
def test(page,sort_key=False,ascending=False):
	print(sort_key)
	crud_read = db_functions.crud_header()
	pages = math.ceil(len(crud_read) / 5)
	pagination = np.arange(0,pages) + 1
	if 'query' in request.form:
		query = request.form['query']
		return redirect(url_for('test_results',query=query,page=page))
	elif 'title' in request.form:
		return redirect(url_for('test',page=page,sort_key='title',ascending=True))
	elif 'username' in request.form:
		return redirect(url_for('test',page=page,sort_key='username'))
	elif 'stamp' in request.form:
		return redirect(url_for('test',page=page,sort_key='stamp'))
	elif sort_key:
		new_table = get_page(page,crud_read,sort_key,ascending)
		return render_template('test.html',new_table=new_table,pagination=pagination,current_page=page)
	new_table = get_page(page,crud_read)
	return render_template('test.html',new_table=new_table,pagination=pagination,current_page=page)

'''




if (__name__ == "__main__"):
	app.run(port = 5000, debug=True)



'''ajax testing here


@app.route('/processpost', methods=['POST'])
def processpost():
	if any([i for i in request.form.values()]) == False:
		return jsonify({'error':'please fill all fields'})
	username = session['username']
	category = request.form['category']
	post = request.form['post']
	ident = 2
	date  =datetime.now()
	when_was = 'created'
	#db_functions.crud_insert(category,post,username)
	
	return jsonify({'username':username,'category':category,'post':post,'id':ident,'date':date,'when_was':when_was,'success':'post added' })

@app.route("/testforum/",methods=['POST','GET'])
def testforum():
	if request.method == 'POST':
		if request.form.get('category'):
			message = 'post added!'
			username = session['username']
			category = request.form['category']
			post = request.form['post']
			db_functions.crud_insert(category,post,username)
			return render_template('testforum.html',message=message)
		elif request.form.get('delete'):
			message = 'post deleted!'
			delete_id = request.form['delete']
			db_functions.crud_delete(delete_id)
			return render_template('testforum.html',message=message)
		elif request.form.get('edit'):
			edit_string = request.form['edit']
			title, post = db_functions.crud_edit(edit_string)
			return render_template('testforum.html',title=title,post=post,edit_string=edit_string)
		elif request.form.get('update_post'):
			message = 'post updated!'
			edit_string = request.form['update_id']
			update_cat = request.form['update_category']
			update_post = request.form['update_post']
			db_functions.crud_update(edit_string,update_cat,update_post)
			return render_template('testforum.html',message=message)
		else:
			error_message = 'please fill in all fields!'
			return render_template('testforum.html',error_message=error_message)
	return render_template('testforum.html')	
	
		
@app.route('/covid/', methods = ['POST', 'GET']) 
def covid_request():
	con.connect()
	select = con.cursor()
	statement = 'call date_compare();'
	select.execute(statement)
	var_last = select.fetchall()[0][0]
	con.commit()
	
	if (date.today() - var_last).days <= 1:
		country,cases,deaths,recovered,active,new,first,last = db_functions.covid_today()
		print('no server call, db select executed')
	else:
		update_values = covid_frame(var_last)
		if update_values == 0:
			country,cases,deaths,recovered,active,new,first,last = db_functions.covid_today()
		else:
			country,cases,deaths,recovered,active,new,first,last = db_functions.covid_today()
			print('db updated with {} values'.format(update_values))
	
	return render_template("covid.html",table = zip(country,cases,deaths,recovered,active,new),start=str(first),finish=str(last))

@app.route("/pops")
def db_load_pop():
	con.connect()
	select_main = con.cursor()
	select_main.execute('call total_pop_2019')
	rows = select_main.fetchall()
	con.commit()
	
	municipality = []
	population = []

	for i in rows:
		municipality.append(i[0])
		population.append(i[1])

	con.close()
	return render_template("pops.html", pop_data = zip(municipality,population))


'''
