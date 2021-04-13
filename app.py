# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, request,json,session,render_template,jsonify
from werkzeug.utils import secure_filename
import re
from functions import get_weather,make_calendar,home_dashboard,thread_page,ago,get_page,make_day,tax_year_header
from google_get import main
import db_functions
import datetime
import pandas as pd
import numpy as np
import json
from pandas.tseries.offsets import DateOffset
import requests
import re
import os
from PIL import Image
import math
import pymysql
from dateutil.relativedelta import relativedelta
from datetime import datetime,date,timedelta
con = pymysql.connect('localhost', 'root', '', '')

#export FLASK_ENV=development

UPLOAD_FOLDER = '/home/kokogabriel/Desktop/Python/flask_projects/flask_exp_fix/static/storage'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'ironpond'

@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response

@app.route('/login/', methods = ['POST', 'GET'])
def login_page():
	if request.method == 'POST':
		email_username = request.form['email_username']
		password = request.form['password']
		data = db_functions.check_user(email_username,password)
		username = data[0][0]
		email = data[0][1]
		home_town = data[0][2]
		role = data[0][3]
		session.permanent = True
		session['username'] = username
		session['hometown'] = home_town.split(',')[0]
		session['log_time'] = datetime.now()
		session['role'] = role
		message = '{} succesfully logged in!'.format(username)
		session['message'] = message
		print(session)
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

@app.route("/<username>/",methods = ['POST', 'GET']) 
def user_profile(username):
	if request.method == 'POST':
		username=session['username']
		file = request.files['file']
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], session['username']))
		session['avatar_updated'] = 'avatar updated!'
		return redirect(url_for('user_profile',username=username))
	user_profile = db_functions.user_profile_get(username)
	if 'avatar_updated' in session:
		avatar_updated = session['avatar_updated']
		session.pop('avatar_updated',None)
		return render_template("user_profile.html",user_profile=user_profile,avatar_updated=avatar_updated)
	return render_template("user_profile.html",user_profile=user_profile)

@app.route("/",methods=['GET','POST'])
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
			message = {'greeting':'Hello from Flask!'}
			return render_template("index.html",social_header=social_header,summary=summary,next_task=next_task,text=json.dumps(message))
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
		
		

	
@app.route('/year_validation/', methods=['POST'])
def year_validation():
	years = ["2019","2020","2021"]
	employer = request.form['search_parameter']
	if 'contract' in request.form:
		return jsonify({'fail':'no employer'})
	check_inserted = [len(db_functions.check_inserted_data_v2(str(pd.to_datetime(year)),session['username'],employer)) for year in years]
	print(check_inserted)
	year_dict = [{"year":year ,"inserted":check} for year,check in zip(years,check_inserted)]
	print(year_dict)
	year_dict = json.dumps(year_dict)
	return year_dict
	
	
@app.route('/contract_validation', methods=['POST'])
def contract_validation():
	employer = request.form['employer']
	existing_contracts = db_functions.tax_contract_get(session['username'])
	if employer in [i[2] for i in existing_contracts]:
		print('duplicate found')
		return jsonify({'error':'existing contract for {} found'.format(employer)})
	return jsonify({'success':'can create contract'})

@app.route("/tax-year/",methods=['POST','GET'])
def tax_year():
	if request.method == 'POST':
		#first, send basic info to db, fetch contract id
		employer = request.form['employer']
		paydate_month_offset = request.form['paydate_month_offset']
		base = request.form['base']
		contract_id = db_functions.tax_contract_create(session['username'],employer,paydate_month_offset,base)
		#optional supplement table
		supplement_table = pd.DataFrame(data={'rule_name':request.form.getlist("rule_name"),'rate':request.form.getlist("rate"),'start_time':request.form.getlist("start_times"),'end_time':request.form.getlist("end_times"),'days_arr':request.form.getlist("days_arr")})
		if not supplement_table.empty:
			supplement_table['contract_id'] = contract_id
			db_functions.tax_supplement_create(supplement_table)
		#send to db if parse years requested (exists in form as array)
		parse_years = [int(year) for year in request.form.getlist("parse_years")]
		if parse_years:
			start = [datetime(year, 1, 1) - relativedelta(months=int(paydate_month_offset)) for year in parse_years]
			end =  [datetime(datetime.today().year,datetime.today().month,1) if start_year + relativedelta(years=1) >= datetime.today() else start_year + relativedelta(years=1) for start_year in start]
			parse_arr = [{'start':i.isoformat()+'Z','end':s.isoformat()+'Z'} for i,s in zip(start,end)]
			google_get = pd.concat(main(indexer['start'],indexer['end'],query=employer) for indexer in parse_arr)
			google_get['username'] = session['username']
			google_get = google_get.sort_index().reset_index(drop=True).drop(columns=['cal_id'])
			db_functions.deposit_google_tasks(google_get[['start_time','end_time','username','category','title']])
		'''
		elif 'reappend' in request.form:
		#	reappend = pd.read_pickle('reappend_db.pkl')
		#	db_functions.deposit_google_tasks(reappend)
		'''
		return redirect(url_for("tax_year"))
	contracts = db_functions.tax_contract_get(session['username'])
	times = np.arange(0,25)
	if contracts: 
		contracts = [{'employer':i[2],'paydate_offset':i[3],'base':i[4],'contract_id':i[0]} for i in contracts]
		years = [2019,2020,2021]
		tax_years_frame = tax_year_header(session['username'],years,contracts)
		return render_template("tax_year.html",tax_years_frame=tax_years_frame,contracts=[i['employer'] for i in contracts],times=times)
	return render_template("tax_year.html",times=times)

@app.route("/calendar/<date>",methods = ['POST', 'GET'])
def home_calendar(date):
	date = datetime.strptime(date,'%Y-%m')
	if 'username' in session:
		state = 'enabled'
		title,framer = make_calendar(date,session['username'],session['role'])
		next_month = date + relativedelta(months=1)
		prev_month =  date - relativedelta(months=1)
		if 'message' in session:
			message = session['message']
			session.pop('message',None)
			return render_template("calendar.html",framer=framer,title=title,next_month=next_month,prev_month=prev_month,state=state,message=message)
		else:
			return render_template("calendar.html",framer=framer,title=title,next_month=next_month,prev_month=prev_month,state=state)
			
	title,framer = make_calendar(date)
	next_month = date + relativedelta(months=1)
	prev_month =  date - relativedelta(months=1)
	return render_template("calendar.html",framer=framer,title=title,next_month=next_month,prev_month=prev_month,state='disabled')

@app.route("/calendar/<year_month>/<day>",methods = ['POST', 'GET'])
def calendar(year_month,day):
	day = pd.to_datetime(year_month +'-'+ day).strftime('%Y-%m-%d')
	times = [str(pd.to_datetime(day) + timedelta(hours = int(i))) for i in np.arange(0,25)]
	if request.method == 'POST':
		if 'whole_day' in request.form:
			start_time = datetime.strptime(day,'%Y-%m-%d')
			end_time = start_time + timedelta(hours = 24)
			username = session['username']
			category = request.form['category']
			title = request.form['title']
			message = '{} doing {} added on {} for the whole day!'.format(category,title,day)
			session['message'] = message
			db_functions.create_new_task(start_time,end_time,username,category,title)
			return redirect(url_for('home_calendar',date=year_month))
		elif 'start_time' and 'end_time' in request.form:
			start_time = request.form['start_time']
			end_time = request.form['end_time']
			username = session['username']
			category = request.form['category']
			title = request.form['title']
			message = '{} doing {} for {} between {} and {} created!'.format(category,title,day,pd.to_datetime(start_time).strftime('%H:%M'),pd.to_datetime(end_time).strftime('%H:%M'))
			session['message'] = message
			db_functions.create_new_task(start_time,end_time,username,category,title)
			return redirect(url_for('home_calendar',date=year_month))
	day_data = make_day(day,session['username'],session['role'])
	title = datetime.strptime(day,'%Y-%m-%d').strftime('%A, %B %d,%Y')
	is_future = datetime.strptime(str(date.today()),'%Y-%m-%d') <= (datetime.strptime(day,'%Y-%m-%d'))
	return render_template("to_do.html",title=title,times=times,day_data=day_data,is_future=is_future)

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

'''forum prototyping'''


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

@app.route("/forum/<int:page>/",methods=['GET','POST'])
@app.route("/forum/sort_by=<sort_key>&ascending=<ascending>/<int:page>/",methods=['GET','POST'])
def forum(page,sort_key=None,ascending=None):
	crud_read = db_functions.crud_header()
	pages = math.ceil(len(crud_read) / 5)
	pagination = np.arange(0,pages) + 1
	if 'query' in request.form:
		query = request.form['query']
		return redirect(url_for('forum_results',query=query,page=1))
	elif 'post' in request.form:
		title = request.form['title']
		post = request.form['post']
		username = session['username']
		db_functions.crud_insert(title,post,username)
		session['post_added'] = 'post added!'
		return redirect(url_for('forum',page=1))
	elif 'thread_id' in request.form:
		thread_id = request.form['thread_id']
		db_functions.crud_delete(thread_id)
		if len(get_page(page,crud_read)) == 1:
			page = page - 1
		session['post_deleted'] = 'post deleted!'
		return redirect(url_for('forum',page=page,sort_key=sort_key,ascending=ascending))
	elif 'title' in request.form:
		if request.form['last']  == 'title':
			ascending = not json.loads(ascending.lower())
			return redirect(url_for('forum',page=page,sort_key='title',ascending=ascending))
		ascending= True
		return redirect(url_for('forum',page=page,sort_key='title',ascending=ascending))
	elif 'username' in request.form:
		if request.form['last']  == 'username':
			ascending = not json.loads(ascending.lower())
			return redirect(url_for('forum',page=page,sort_key='username',ascending=ascending))
		return redirect(url_for('forum',page=page,sort_key='username',ascending=True))
	elif 'stamp' in request.form:
		if request.form['last']  == 'stamp':
			ascending = not json.loads(ascending.lower())
			return redirect(url_for('forum',page=page,sort_key='stamp',ascending=ascending))
		return redirect(url_for('forum',page=page,sort_key='stamp',ascending=True))
	elif sort_key and ascending:
		new_table = get_page(page,crud_read,sort_key,ascending)
		if 'post_deleted' in session:
			post_removed = session['post_deleted']
			session.pop('post_deleted',None)
			return render_template('forum.html',new_table=new_table,pagination=pagination,current_page=page,last=sort_key,sort_key=sort_key,ascending=ascending,post_removed=post_removed)
		return render_template('forum.html',new_table=new_table,pagination=pagination,current_page=page,last=sort_key,sort_key=sort_key,ascending=ascending)
	new_table = get_page(page,crud_read)
	if 'post_added' in session:
		post_success = session['post_added']
		session.pop('post_added',None)
		return render_template('forum.html',new_table=new_table,pagination=pagination,current_page=page,post_success=post_success)
	elif 'post_deleted' in session:
		post_removed = session['post_deleted']
		session.pop('post_deleted',None)
		return render_template('forum.html',new_table=new_table,pagination=pagination,current_page=page,post_removed=post_removed)
	return render_template('forum.html',new_table=new_table,pagination=pagination,current_page=page)
	
	
@app.route("/forum/query=<query>/<int:page>/",methods=['GET','POST'])
@app.route("/forum/query=<query>&sort_by=<sort_key>&ascending=<ascending>/<int:page>/",methods=['GET','POST'])
def forum_results(query,page,sort_key=None,ascending=None):
	crud_read = db_functions.search_forums(query)
	pages = math.ceil(len(crud_read) / 5)
	pagination = np.arange(0,pages) + 1
	if 'query' in request.form:
		query = request.form['query']
		return redirect(url_for('forum_results',query=query,page=1))
	elif 'post' in request.form:
		title = request.form['title']
		post = request.form['post']
		username = session['username']
		db_functions.crud_insert(title,post,username)
		session['post_added'] = 'post added!'
		return redirect(url_for('forum',page=1))
	elif 'thread_id' in request.form:
		thread_id = request.form['thread_id']
		db_functions.crud_delete(thread_id)
		if len(get_page(page,crud_read)) == 1:
			page = page - 1
		session['post_deleted'] = 'post deleted!'
		return redirect(url_for('forum_results',query=query,page=page,sort_key=sort_key,ascending=ascending))
	elif 'title' in request.form:
		if request.form['last']  == 'title':
			ascending = not json.loads(ascending.lower())
			return redirect(url_for('forum_results',query=query,page=page,sort_key='title',ascending=ascending))
		ascending= True
		return redirect(url_for('forum_results',query=query,page=page,sort_key='title',ascending=ascending))
	elif 'username' in request.form:
		if request.form['last']  == 'username':
			ascending = not json.loads(ascending.lower())
			return redirect(url_for('forum_results',query=query,page=page,sort_key='username',ascending=ascending))
		ascending= True
		return redirect(url_for('forum_results',query=query,page=page,sort_key='username',ascending=ascending))
	elif 'stamp' in request.form:
		if request.form['last']  == 'stamp':
			ascending = not json.loads(ascending.lower())
			return redirect(url_for('forum_results',query=query,page=page,sort_key='stamp',ascending=ascending))
		ascending= True
		return redirect(url_for('forum_results',query=query,page=page,sort_key='stamp',ascending=ascending))
	elif sort_key and ascending:
		new_table = get_page(page,crud_read,sort_key,ascending)
		if 'post_deleted' in session:
			post_removed = session['post_deleted']
			session.pop('post_deleted',None)
			return render_template('forum_results.html',new_table=new_table,pagination=pagination,current_page=page,last=sort_key,sort_key=sort_key,ascending=ascending,query=query,post_removed=post_removed)
		return render_template('forum_results.html',new_table=new_table,pagination=pagination,current_page=page,last=sort_key,sort_key=sort_key,ascending=ascending,query=query)
	new_table = get_page(page,crud_read)
	if 'post_deleted' in session:
		post_removed = session['post_deleted']
		session.pop('post_deleted',None)
		return render_template('forum_results.html',new_table=new_table,pagination=pagination,current_page=page,query=query,post_removed=post_removed) 
	return render_template('forum_results.html',new_table=new_table,pagination=pagination,current_page=page,query=query)
	
@app.route('/forum/thread/<int:thread>/',methods=['POST','GET'])
def forum_thread(thread):
	print(thread)
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
	
'''testing highcharts here'''





if (__name__ == "__main__"):
	app.run(port = 5000, debug=True)

'''
@app.route('/graph/')
def graph(chartID = 'population'):
	columns,municipality,population = db_functions.top_10_pop()
	chart_type = 'column'
	title = 'hello'
	return render_template('graph.html',chart_type=chart_type,population=population,municipality=municipality,title=columns[0],subtitle=columns[1])

	if any(check_inserted[:-1]):
		tax_years = db_functions.tax_years_get(session['username'])
		tax_years_append = main(pd.to_datetime(datetime.today().strftime('%Y-%m')).isoformat() + 'Z')
		tax_years = tax_years.append(tax_years_append[['start_time','end_time']])
		tax_years['total_hours'] = (tax_years['end_time'] - tax_years['start_time']).dt.seconds / 3600
		monthly = tax_years.resample('m').sum().round(2)
		monthly['post_to'] = monthly.index + DateOffset(months=1)
		true_month_slicer = tax_years.index.to_period('M').to_timestamp('M').unique()
		monthly = monthly[(monthly.index.isin(true_month_slicer))]
		tax_years_frame = [monthly[monthly['post_to'].dt.year == int(year)].drop(columns=['post_to']).reset_index().to_html(classes='table',table_id=int(year), header=True,index=False) for year in years if not monthly[monthly['post_to'].dt.year == int(year)].empty] 
		return render_template("tax_year.html",year_dict=year_dict,tax_years_frame=tax_years_frame)
	tax_years_append = main(pd.to_datetime(datetime.today().strftime('%Y-%m')).isoformat() + 'Z')
	tax_years_append['total_hours'] = (tax_years_append['end_time'] - tax_years_append['start_time']).dt.seconds / 3600
	tax_years_append = [tax_years_append.resample('m').sum().round(2).reset_index().to_html(classes='table',table_id=int(datetime.today().year), header=True,index=False)]
	return render_template("tax_year.html",year_dict=year_dict,tax_years_frame=tax_years_append)
	
	@app.route("/tax-year/",methods=['POST','GET'])
def tax_year():
	if request.method == 'POST':
		if 'search_parameter' in request.form:
			query = request.form['search_parameter']
			year = pd.to_datetime(request.form['year'])
			start = (year - relativedelta(months=1))
			end = (start + relativedelta(years=1))
			google_frame = main(start.isoformat()+'Z',end.isoformat()+'Z',query)
			google_frame['username'] = session['username']
			google_frame = google_frame.sort_index()
			google_frame = google_frame[(google_frame.index < pd.to_datetime(datetime.now().strftime('%Y-%m')))]
			google_frame = google_frame.reset_index(drop=True)
			google_frame = google_frame.drop(columns=['cal_id'])
			google_frame = google_frame[['start_time','end_time','username','category','title']]
			db_functions.deposit_google_tasks(google_frame)
			return redirect(url_for("tax_year"))
		elif 'reappend' in request.form:
			reappend = pd.read_pickle('reappend_db.pkl')
			db_functions.deposit_google_tasks(reappend)
			return redirect(url_for("tax_year"))
	contracts = db_functions.tax_contract_get(session['username'])
	if contracts: 
		contracts = [i[2] for i in contracts]
		years = ['2019','2020','2021']
		for year in years:
			for con in contracts:
				print(db_functions.check_inserted_data_v2(str(pd.to_datetime(year)),session['username'],con))
		#	print(db_functions.check_inserted_data_v2(str(pd.to_datetime(year)),session['username'],employer))
		check_inserted = [len(db_functions.check_inserted_data(str(pd.to_datetime(year)),session['username'])) >=12  for year in years]
		year_dict = [{'year':year ,'inserted':check} for year,check in zip(years,check_inserted)]
		tax_years_frame = tax_year_header(session['username'],years)
		return render_template("tax_year.html",year_dict=year_dict,tax_years_frame=tax_years_frame,contracts=contracts)
	return render_template("tax_year.html")
	
	'''
