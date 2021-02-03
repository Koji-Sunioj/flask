# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, request,json
import re
from functions import weather_local,covid_frame,test_graph,get_weather
import db_functions
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import numpy as np
import pygal
import base64
import json
import requests
import re
import pymysql
from io import BytesIO
from datetime import datetime,date
from flask import render_template

con = pymysql.connect('localhost', 'root', 'Karelia', 'geo_data')

#export FLASK_ENV=development

app = Flask(__name__)

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
			category = request.form['category']
			post = request.form['post']
			db_functions.crud_insert(category,post)
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
			
@app.context_processor
def test_component():
	firefox = {'name':'Firefox','values':[0,0,0,16.6,25,31,36.4,45.5,46.3,42.8,37.1],'dates':['2020-1','2020-2','2020-3','2020-4','2020-5','2020-6','2020-7','2020-8','2020-9','2020-10','2020-11']}
	chrome = {'name':'Chrome','values':[0 ,0,0,0,0,0,0,3.9,10.8,23.8,35.3],'dates':['2020-1','2020-2','2020-3','2020-4','2020-5','2020-6','2020-7','2020-8','2020-9','2020-10','2020-11']}
	data=list((firefox,chrome))
	return {'data':data}

@app.route("/clear/", methods = ['POST', 'GET'], defaults={'info': None})
def clear(info):
	if request.method == 'GET':
		return render_template("clear.html")
	elif request.method == 'POST':
		if request.form['last']:
			data = request.form.get('plot')
			data = eval(data)
			if data['name'] == request.form['last']:
				print('comparison done: same plot requested, plot cleared')
				return render_template("clear.html")
			else:
				last = data['name']
				graph_data = test_graph(data)
				print('comparison done: different plot requested, plot granted')
				return render_template("clear.html",last=last,graph_data=graph_data)
		else:
			data = request.form.get('plot')
			data = eval(data)
			last = data['name']
			graph_data = test_graph(data)
			print('no comparison performed, plot granted')
			return render_template("clear.html",last=last,graph_data=graph_data)



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

@app.route("/")
def index():
	a,b,c = weather_local()
	return render_template("index.html", stuff = zip(a,b,c))
	
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

'''testing highcharts here'''
    
@app.route('/graph/')
def graph(chartID = 'population'):
	columns,municipality,population = db_functions.top_10_pop()
	series = [{"name": columns[1], "data": population}]
	chart = {"renderTo": chartID, "type": 'column', "height": 500}
	title = {"text": 'Top 10 cities in Finland ranked by population'}
	subtitle = {"text": 'hey'}
	xAxis = {"categories": municipality}
	yAxis = {"title": {"text": columns[1]}}
	return render_template('graph.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis,subtitle=subtitle)

@app.route('/graph_test/')
def graph_test(chartID = 'population'):
	columns,municipality,population = db_functions.top_10_pop()
	chart_type = 'column'
	title = 'hello'
	return render_template('graph_test.html',chart_type=chart_type,population=population,municipality=municipality,title=columns[0],subtitle=columns[1])


if (__name__ == "__main__"):
	app.run(port = 5000, debug=True)

