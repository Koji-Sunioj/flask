# -*- coding: utf-8 -*-
import json
import pandas as pd
import requests
import numpy as np
import re
import pygal
import pymysql
import pycountry_convert as pc
import db_functions
import calendar
con = pymysql.connect('localhost', 'root', 'Karelia', 'geo_data')
from datetime import datetime,date,timedelta


def home_dashboard(hometown,username):
	social_header = db_functions.home_crud_first()
	next_task = db_functions.calendar_dashboard(username)
	url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/forecast?aggregateHours=24&combinationMethod=aggregate&contentType=json&unitGroup=metric&locationMode=single&key=NFL5M6IWKEWK1CTBV54KLQ9JR&dataElements=default&locations={}'.format(hometown)
	response = requests.get(url)
	data = response.json()
	print(str(data['remainingCost']) + ' server requests remaining today')
	home_town = data['location']['id']
	weather_summary =  data['location']['currentConditions']['icon']
	forecast_time = data['location']['currentConditions']['datetime'][:10] + ' '+ data['location']['currentConditions']['datetime'][11:16]
	windchill = data['location']['currentConditions']['windchill']
	temperature = data['location']['currentConditions']['temp']
	
	summary = {'home_town': home_town,'summary':weather_summary,'forecast_time':forecast_time,'wind_chill':windchill,'temperature':temperature}
	
	return social_header,summary,next_task

def test_graph(data):
	graph = pygal.Line()
	graph.title = data['name']
	graph.x_labels = data['dates']
	graph.add('data',  data['values'])
	graph_data = graph.render_data_uri()
	return graph_data

def make_calendar(date,username=None):
	stamp = pd.to_datetime(date)
	stamp_ranger = pd.date_range(start='{}/1/{}'.format(stamp.month,stamp.year), end='{}/{}/{}'.format(stamp.month,stamp.days_in_month,stamp.year))
	framer = pd.DataFrame(stamp_ranger.weekofyear.unique(),columns=['week'])
	framer['year'] =  [stamp_ranger.year.unique().values[0] for i in framer.values ]
	framer['diff'] = framer['week'].diff(periods=-1)
	framer.loc[framer['diff'] > 1,'year'] = framer.loc[framer['diff'] > 1,'year'] - 1
	new_stamper = pd.to_datetime(framer.week.astype(str)+'-'+framer.year.astype(str)+'-1' ,format='%V-%G-%u')
	calender_list = [i + timedelta(days=int(s)) for s in np.arange(0,7) for i in new_stamper]
	calender_list.sort()

	cal_data = db_functions.check_calendar_data(date,username)
	if any(cal_data):
		cal_list = []
		for date_string in calender_list:
			if date_string in cal_data.index:
				try:
					cal_dict = {}
					cal_dict['date'] = date_string
					cal_dict['data'] = {}
					if len(cal_data.loc[date_string]) > 1:  
						for cal_id in cal_data.loc[date_string]['cal_id'].values:
							cal_dict['data'][cal_id] = {'start_time': cal_data[cal_data['cal_id'] == cal_id].start_time[0],'end_time':cal_data[cal_data['cal_id'] == cal_id].end_time[0],'title':cal_data[cal_data['cal_id'] == cal_id].category[0]}    
					cal_list.append(cal_dict)
				except:
					cal_dict = {}
					cal_dict['date'] = date_string
					cal_dict['data'] = {}
					cal_dict['data'][cal_data.loc[date_string]['cal_id']] = {'start_time':cal_data.loc[date_string]['start_time'],'end_time':cal_data.loc[date_string]['end_time'],'title':cal_data.loc[date_string]['category']}
					cal_list.append(cal_dict)
			else:
				cal_list.append(date_string)
				
		framer = pd.DataFrame(np.array(cal_list).reshape(len(framer),7),index = framer['week'])
		framer.columns = [ calendar.day_name[i] for i in framer.columns]
		title = stamp.strftime('%B %Y')
		return title,framer.reset_index()
	
	framer = pd.DataFrame(np.array(calender_list).reshape(len(framer),7),index = framer['week'])
	framer.columns = [ calendar.day_name[i] for i in framer.columns]
	title = stamp.strftime('%B %Y')
	print(framer)
	return title,framer.reset_index()

def get_weather(city):
	#json requests
	url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/forecast?aggregateHours=24&combinationMethod=aggregate&contentType=json&unitGroup=metric&locationMode=single&key=NFL5M6IWKEWK1CTBV54KLQ9JR&dataElements=default&locations={}'.format(city)
	response = requests.get(url)
	data = response.json()
	print(str(data['remainingCost']) + ' server requests remaining today')
	server_city = data['location']['address']
	#create lists for forecast table
	maxt = [i['maxt'] for i in data['location']['values']]
	mint = [i['mint'] for i in data['location']['values']]
	visib = [i['visibility'] for i in data['location']['values']]
	wind = [i['wspd'] for i in data['location']['values']]
	dates = [i['datetimeStr'][0:10] for i in data['location']['values']]
	clouds = [i['cloudcover'] for i in data['location']['values']]
	rain = [i['precip'] for i in data['location']['values']]
	gust = [i['wgust'] for i in data['location']['values']]
	conditions = [i['conditions'] for i in data['location']['values']]
	humidity = [i['humidity'] for i in data['location']['values']]
	table = zip(dates,maxt,mint,rain,clouds,conditions,humidity,wind,gust,visib)
	
	#create summary table
	weather_summary =  data['location']['currentConditions']['icon']
	forecast_time = data['location']['currentConditions']['datetime'][:10] + ' '+ data['location']['currentConditions']['datetime'][11:16]
	windchill = data['location']['currentConditions']['windchill']
	temperature = data['location']['currentConditions']['temp']
	
	sunrise = data['location']['currentConditions']['sunrise'][11:16]
	sunset = data['location']['currentConditions']['sunset'][11:16]
	day_length = (datetime.strptime(sunset,'%H:%M') - datetime.strptime(sunrise,'%H:%M'))
	day_length_string = str(day_length)
	hours = int(day_length_string.split(':')[0])
	minutes = int(day_length_string.split(':')[1])
	
	summary = {'summary':weather_summary,'forecast_time':forecast_time,'wind_chill':windchill,'temperature':temperature,'sunrise':sunrise,'sunset':sunset,'hours':hours,'minutes':minutes}
	return table,summary,server_city,maxt,mint,dates
	
	
	
def covid_frame(var_last):
	#call server to create dataframe, index from last db date onwards
	url = 'https://pomber.github.io/covid19/timeseries.json'
	r = requests.get(url)
	response_dict = r.json()
	data = []
	for i in response_dict.items():
		data.append(i)
		
	dates = []
	cases = []
	country = []
	deaths = []
	recovered = []
	
	#send json response to lists
	for i in data:
		for l in i[1]:
			country.append(i[0])
			dates.append(l['date'])
			cases.append(l['confirmed'])
			deaths.append(l['deaths'])
			recovered.append(l['recovered'])
	
	#construct frame from dict of lists		
	frame = {'dates':dates, 'country':country, 'cases':cases, 'deaths': deaths, 'recovered': recovered}
	df = pd.DataFrame(frame)
	df.dates = pd.to_datetime(df.dates)
	df['active'] = df['cases'] - df['deaths'] - df['recovered']
	
	#sequencially calculate change of new cases per day
	df_cases = df['cases'].tolist()
	reference = []
	calculated = []
	
	for s in range(len(df_cases)):
		reference.append(df_cases[s])
		if s == 0:
			calculated.append(reference[0])
		else:
			calculated.append(reference[-1] - reference[-2])
	
	#create new column, set date index to fix new case on first date, US to USA		
	df['new'] = calculated
	df = df.set_index('dates')
	df.loc['2020-01-22','new'] = df.loc['2020-01-22','cases']
	df.loc[df['country'] == 'US','country'] = 'United States of America'
	print('frame from server completed')
	
	select = con.cursor()
	select.execute('select country from geo_data.continent_table;')
	db_countries = select.fetchall()
	db_countries = [i[0] for i in db_countries]

	#missing country, if any
	missing_country = df[~df['country'].isin(list(db_countries))]
	all_append = df[df.index > str(var_last)].append(missing_country[missing_country.index <= str(var_last)]).reset_index()
	
	if len(all_append)>0:
		#insert new country in continent table, if exists
		if len(missing_country.country.unique()) > 0:
			mapper = {'AF': 'Africa', 'AS': 'Asia', 'EU': 'Europe', 'NA': 'North America','OC':'Oceana','SA':'South America'}
			insert_new_country = []
			insert_new_continent = []

			for i in missing_country.country.unique():
				country_code = pc.country_name_to_country_alpha2(i, cn_name_format="default")
				continent_name = pc.country_alpha2_to_continent_code(country_code)
				insert_new_country.append(i)
				insert_new_continent.append(mapper[continent_name])
				
			db_functions.update_continent(insert_new_country,insert_new_continent) 
		else:
			pass
		
		#then insert into main table
		db_functions.update_covid(all_append)
	
		#if country exists in db, but not in the covid server anymore, remove it:
		server = list(df.country.unique())
		delete_it = [deleter for deleter in db_countries if deleter not in server]
		if len(delete_it) > 0:
			db_functions.delete_forgotten(delete_it)
		update_values = len(all_append)
	else:
		pass
		print('server frame is same as db')
		update_values = 0
	
	return update_values



'''
def make_calendar(date):
	stamp = pd.to_datetime(date)
	stamp_ranger = pd.date_range(start='{}/1/{}'.format(stamp.month,stamp.year), end='{}/{}/{}'.format(stamp.month,stamp.days_in_month,stamp.year))
	framer = pd.DataFrame(stamp_ranger.weekofyear.unique(),columns=['week'])
	framer['year'] =  [stamp_ranger.year.unique().values[0] for i in framer.values ]
	new_stamper = pd.to_datetime(framer.week.astype(str)+'-'+framer.year.astype(str)+'-1' ,format='%V-%G-%u')
	calender_list = [i + timedelta(days=int(s)) for s in np.arange(0,7) for i in new_stamper]
	db_functions.check_calendar_data(date,session['username'])
	calender_list.sort()
	framer = pd.DataFrame(np.array(calender_list).reshape(len(framer),7),index = framer['week'])
	framer.columns = [ calendar.day_name[i] for i in framer.columns]
	title = stamp.strftime('%B %Y')
	return title,framer.reset_index()


'''
