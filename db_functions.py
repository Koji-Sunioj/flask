import pymysql
import pandas as pd

con = pymysql.connect('localhost', 'root', 'HIDDEN', 'HIDDEN')

'''repetive functions here'''

def connect():
	con.connect()
	db_connect = con.cursor()
	return db_connect


'''login functions'''

def check_user(email_username,password):
	select_main = connect()
	select_main.callproc('check_email_password',(email_username,password))
	rows = select_main.fetchall()
	con.commit()
	return rows

def check_new_user(email,username):
	select_main = connect()
	select_main.callproc('check_new_user',(email,username,))
	rows = select_main.fetchall()
	con.commit()
	return rows

def create_new_user(username,email,home_town,password):
	insert_main = connect()
	insert_main.callproc('create_new_user',(username,email,home_town,password))
	con.commit()

'''blog functions'''

def crud_header():
	select_main = connect()
	select_main.execute('call crud_read()')
	crud_read = select_main.fetchall()
	con.commit()
	return crud_read

def crud_insert(category,post,username):
	insert_main = connect()
	insert_main.callproc('crud_create',(category,post,username))
	con.commit()

def crud_delete(delete_id):
	delete_main = connect()
	delete_main.callproc('crud_delete',(delete_id,))
	con.commit()

def crud_edit(edit_string):
	update_main = connect()
	update_main.callproc('crud_update_form',(edit_string,))
	rows = update_main.fetchall()
	con.commit()
	title = rows[0][0]
	post = rows[0][1]
	return title, post

def crud_update(edit_string,update_cat,update_post):
	update_main = connect()
	update_main.callproc('crud_update_db',(edit_string,update_cat,update_post,))
	con.commit()

'''thread functions'''


def thread_main(thread_id):
	select_main = connect() 
	select_main.callproc('crud_thread',(thread_id,))
	rows = select_main.fetchall()
	thread = {'id':rows[0][0], 'title':rows[0][1],'post':rows[0][2],'stamp':rows[0][3],'when_was':rows[0][4],'author':rows[0][5]}
	con.commit()
	return thread


def thread_reply(thread_id, reply,username):
	insert_main = connect()
	insert_main.callproc('crud_thread_insert',(thread_id, reply,username))
	con.commit()
	
def reply_reply(input_reply_id,input_username,input_reply):
	insert_main = connect()
	insert_main.callproc('crud_reply_insert',(input_reply_id,input_username,input_reply))
	con.commit()

def crud_thread_read(thread):
	select_main = connect() 
	select_main.callproc('crud_thread_read',(thread,))
	rows = select_main.fetchall()
	con.commit()
	if any(rows):
		reply_ids = [i[0] for i in rows]
		thread_id = [i[1] for i in rows]
		username = [i[2] for i in rows]
		reply = [i[3] for i in rows]
		stamp = [i[4] for i in rows]
		when_was = [i[5] for i in rows]
		replies = zip(reply_ids,thread_id,username,reply,stamp,when_was)
		return replies
	replies = False
	return replies
	
def crud_reply_read(thread):
	select_main = connect() 
	select_main.callproc('crud_reply_read',(thread,))
	rows = select_main.fetchall()
	con.commit()
	if any(rows):
		reply_reply = {i[1]:[] for i in rows}
		for i in rows:
			temp = {}
			temp['comment_id'] =  i[2]
			temp['username'] =  i[3]
			temp['reply'] =  i[4]
			temp['stamp'] =  i[5]
			temp['when_was'] =  i[6]
			reply_reply[i[1]].append(temp)
		return reply_reply
	reply_reply = False
	return reply_reply
	
'''calendar functions'''

def check_calendar_data(date,username):
	select_main = connect()
	select_main.callproc('check_calendar_data',(date,username))
	con.commit()
	rows = select_main.fetchall()
	columns =  [i[0] for i in select_main.description]
	cal_data = pd.DataFrame(rows)
	if len(cal_data) == 0:
		return cal_data
	cal_data.columns = columns
	cal_data = cal_data.sort_values('db_date')
	cal_data = cal_data.set_index('db_date',drop=True)
	return cal_data

def create_new_task(start_time,end_time,username,category,post):
	insert_main = connect()
	insert_main.callproc('create_new_task',(start_time,end_time,username,category,post))
	con.commit()

def check_day_tasks(date,username):
	select_main = connect()
	select_main.callproc('check_day_tasks',(date,username))
	rows = select_main.fetchall()
	con.commit()
	return rows

'''home page functions'''

def home_crud_first():
	select_main = connect()
	select_main.execute('call crud_dashboard()')
	rows = select_main.fetchall()
	con.commit()
	return rows

def calendar_dashboard(username):
	select_main = connect()
	select_main.callproc('calendar_dashboard',(username,))
	con.commit()
	rows = select_main.fetchall()
	return rows
	
	
'''highcharts demo'''	

def top_10_pop():
	select_main = connect()
	select_main.execute('call total_pop_2019')
	rows = select_main.fetchall()
	con.commit()
	columns =  [i[0] for i in select_main.description]
	municipality = [i[0] for i in rows[:10]]
	population = [int(i[1]) for i in rows[:10]]
	return columns,municipality,population

'''covid api functions here'''

def covid_today():
	select_main = connect()
	select_main.execute('call covid_header()')
	rows = select_main.fetchall()
	
	country = [i[0] for i in rows]
	cases = [i[1] for i in rows]
	deaths = [i[2] for i in rows]
	recovered = [i[3] for i in rows]
	active = [i[4] for i in rows]
	new = [i[5] for i in rows]

	select_main.execute('call date_first_last()')
	rows = select_main.fetchall()
	first = rows[0][0]
	last = rows[0][1]
	con.commit()
	print('values fetched from covid database')
	return country,cases,deaths,recovered,active,new,first,last


def update_continent(insert_new_country,insert_new_continent):
	insert_main = connect()
	statement = "insert into geo_data.continent_table(country, continent) values (%s,%s)"

	for country, continent in zip(insert_new_country,insert_new_continent):
		insert_main.execute(statement,(country,continent))
	con.commit()
	print('new country and continent inserted')
    
def delete_forgotten(delete_it):
	delete_main = connect()
	for i in delete_it:
		delete_main.execute("delete from geo_data.continent_table where country=(%s)",i)
	con.commit()
	print('non existant country in server deleted from database')

def update_covid(append_db):
	insert_main = connect()
	statement = "insert into geo_data.covid(record_date, country,cases,deaths,recovered,active,new_record) values (%s,%s,%s,%s,%s,%s,%s)"
	
	for record_date, country,cases,deaths,recovered,active,new_record in append_db.values:
		insert_main.execute(statement,(record_date.date(),country,cases,deaths,recovered,active,new_record))
	con.commit()
	print('covid database updated with server values')
