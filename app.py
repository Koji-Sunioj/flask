# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, request,json,session,render_template
import re
from functions import covid_frame,test_graph,get_weather,make_calendar,home_dashboard
import db_functions
import datetime
import pandas as pd
import numpy as np
import pygal
import json
import requests
import re
import pymysql

from datetime import datetime,date,timedelta

con = pymysql.connect('localhost', 'root', 'HIDDEN', 'HIDDEN')

#export FLASK_ENV=development

app = Flask(__name__)
app.secret_key = 'any random string'


@app.route("/")
def index():
	if 'message' in session:
		message = session['message']
		session.pop('message', None)
		if 'username' in session:
			social_header,summary = home_dashboard(session['hometown'])
			session['weather_summary'] = summary
			print('initial login')
			return render_template("index.html",message=message,social_header=social_header,summary=summary)
		else:
			session.clear()
			print('user logged out')
			return render_template("index.html",message=message)
			
	elif 'username' in session:
		diff_weather_log = session['log_time'] - datetime.strptime(session['weather_summary']['forecast_time'],'%Y-%m-%d %H:%M')
		diff_weather_log = ((diff_weather_log.seconds//60))
		if diff_weather_log < 120:
			print(diff_weather_log)
			social_header = db_functions.home_crud_first()
			summary = session['weather_summary']
			session['log_time'] = datetime.now()
			return render_template("index.html",social_header=social_header,summary=summary)
		elif diff_weather_log > 120:
			social_header,summary = home_dashboard(session['hometown'])
			session['log_time'] = datetime.now()
			return render_template("index.html",social_header=social_header,summary=summary)
		else:
			print(diff_weather_log)
			social_header,summary = home_dashboard(session['hometown'])
			session['weather_summary'] = summary
			return render_template("index.html",social_header=social_header,summary=summary)
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
			title,framer = make_calendar(date)
			next_month = date + timedelta(days=int(pd.to_datetime(date).days_in_month))
			prev_month =  date - timedelta(days=int(pd.to_datetime(date).days_in_month))
			return render_template("calendar.html",framer=framer,title=title,date=date,next_month=next_month,prev_month=prev_month,state=state)
		else:
			title,framer = make_calendar(date)
			next_month = date + timedelta(days=int(pd.to_datetime(date).days_in_month))
			prev_month =  date - timedelta(days=int(pd.to_datetime(date).days_in_month))
			return render_template("calendar.html",framer=framer,title=title,date=date,next_month=next_month,prev_month=prev_month,state='disabled')

@app.route("/calendar/<year_month>/<day>",methods = ['POST', 'GET'])
def calendar(year_month,day):
	day = pd.to_datetime(year_month +'-'+ day).strftime('%Y-%m-%d')
	times = [str(pd.to_datetime(day) + timedelta(hours = int(i))) for i in np.arange(0,25)]
	if request.method == 'POST':
		try:
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
					db_functions.create_new_task(start_time,end_time,username,category,post)
					return redirect(url_for('home_calendar',date=day[:7]))
			else:
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
					db_functions.create_new_task(start_time,end_time,username,category,post)
					return redirect(url_for('home_calendar',date=day[:7]))
		except:
			message = 'please select start and end times!'
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


@app.route('/login/', methods = ['POST', 'GET'])
def login_page():
	if request.method == 'POST':
		email_username = request.form['email_username']
		password = request.form['password']
		data = db_functions.check_user(email_username,password)
		if len(data) == 0:
			error_message = 'wrong username and password!'
			return render_template('login.html', error_message=error_message)
		else:
			username = data[0][0]
			email = data[0][1]
			home_town = data[0][2]
			session['username'] = username
			session['hometown'] = home_town
			session['log_time'] = datetime.now()
			message = '{} succesfully logged in!'.format(username)
			session['message'] = message
			return redirect(url_for('index'))
			
	return render_template('login.html')


	
@app.route('/create_profile/', methods = ['POST', 'GET'])
def create_profile():
	if request.method == 'POST':
		checked = [i == '' for i in request.form.values()]
		if any(checked) == True:
			error_message = 'please fill all the fields.'
			return render_template('create_profile.html',error_message=error_message)
		else:
			email = request.form['email']
			username = request.form['username']
			home_town = request.form['home_town']
			password = request.form['password']
			data = db_functions.check_new_user(email,username)
			if data:
				error_message = 'that email or username is taken. please use a different one.'
				return render_template('create_profile.html',error_message=error_message)
			elif request.form['password'] != request.form['password_confirm']:
				error_message = 'passwords do not match.'
				return render_template('create_profile.html',error_message=error_message)
			else:
				db_functions.create_new_user(username,email,home_town,password)
				#title,framer = make_calendar()
				message = 'username {} was succesfully created. now logged in!'.format(username)
				session['username'] = username
				session['message'] = message
				session['hometown'] = home_town
				session['log_time'] = datetime.now()
				return redirect(url_for('index'))
	return render_template('create_profile.html')

@app.context_processor
def crud_component():
	crud_read = db_functions.crud_header()
	return {'crud_read':crud_read}
	
@app.route('/crud/',methods=['POST','GET'])
def crud():
	if request.method == 'GET':
		return render_template('crud.html')
	elif request.method == 'POST':
		if request.form.get('category'):
			username = session['username']
			category = request.form['category']
			post = request.form['post']
			db_functions.crud_insert(category,post,username)
			return render_template('crud.html')
		elif request.form.get('delete'):
			delete_id = request.form['delete']
			db_functions.crud_delete(delete_id)
			return render_template('crud.html')
			
		elif request.form.get('edit'):
			edit_string = request.form['edit']
			title, post = db_functions.crud_edit(edit_string)
			return render_template('crud.html',title=title,post=post,edit_string=edit_string)
			
		elif request.form.get('update_post'):
			edit_string = request.form['update_id']
			update_cat = request.form['update_category']
			update_post = request.form['update_post']
			db_functions.crud_updatet(edit_string,update_cat,update_post)
			return render_template('crud.html')
		else:
			return render_template('crud.html')
			

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


@app.context_processor
def inject_now():
	return {'now': datetime.now()}
	

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


if (__name__ == "__main__"):
	app.run(port = 5000, debug=True)

