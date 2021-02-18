import pymysql
con = pymysql.connect('localhost', 'root', 'Karelia', 'geo_data')

def home_crud_first():
	con.connect()
	select_main = con.cursor()
	select_main.execute('call crud_dashboard()')
	rows = select_main.fetchall()
	con.commit()
	return rows

def create_new_task(start_time,end_time,username,category,post):
	con.connect()
	insert_main = con.cursor()
	insert_main.callproc('create_new_task',(start_time,end_time,username,category,post))
	con.commit()
	

def covid_today():
	con.connect()
	#fetch all data from latest record date, send to five lists
	select_main = con.cursor()
	select_main.execute('call covid_header()')
	rows = select_main.fetchall()
	
	country = [i[0] for i in rows]
	cases = [i[1] for i in rows]
	deaths = [i[2] for i in rows]
	recovered = [i[3] for i in rows]
	active = [i[4] for i in rows]
	new = [i[5] for i in rows]
	
	#get the first and last date for the interface
	select_main.execute('call date_first_last()')
	rows = select_main.fetchall()
	first = rows[0][0]
	last = rows[0][1]
	con.commit()
	print('values fetched from covid database')
	return country,cases,deaths,recovered,active,new,first,last

def crud_header():
	con.connect()
	select_main = con.cursor()
	statement = 'call crud_read();'
	select_main.execute(statement)
	crud_read = select_main.fetchall()
	con.commit()
	return crud_read

def crud_insert(category,post,username):
	con.connect()
	insert_main = con.cursor()
	insert_main.callproc('crud_create',(category,post,username))
	con.commit()

def crud_delete(delete_id):
	con.connect()
	delete_main = con.cursor()
	delete_main.callproc('crud_delete',(delete_id,))
	con.commit()

def crud_edit(edit_string):
	con.connect()
	update_main = con.cursor()
	update_main.callproc('crud_update_form',(edit_string,))
	rows = update_main.fetchall()
	con.commit()
	title = rows[0][0]
	post = rows[0][1]
	return title, post

def crud_updatet(edit_string,update_cat,update_post):
	con.connect()
	update_main = con.cursor()
	update_main.callproc('crud_update_db',(edit_string,update_cat,update_post,))
	con.commit()
	

def update_continent(insert_new_country,insert_new_continent):
	insert_main = con.cursor()
	statement = "insert into geo_data.continent_table(country, continent) values (%s,%s)"

	for country, continent in zip(insert_new_country,insert_new_continent):
		insert_main.execute(statement,(country,continent))
	con.commit()
	print('new country and continent inserted')
    
def delete_forgotten(delete_it):
	delete_main = con.cursor()
	for i in delete_it:
		delete_main.execute("delete from geo_data.continent_table where country=(%s)",i)
	con.commit()
	print('non existant country in server deleted from database')

def update_covid(append_db):
	#insert differential dataframe new values into mysql
	insert_main = con.cursor()
	statement = "insert into geo_data.covid(record_date, country,cases,deaths,recovered,active,new_record) values (%s,%s,%s,%s,%s,%s,%s)"
	
	for record_date, country,cases,deaths,recovered,active,new_record in append_db.values:
		insert_main.execute(statement,(record_date.date(),country,cases,deaths,recovered,active,new_record))
	con.commit()
	print('covid database updated with server values')


def top_10_pop():
	con = pymysql.connect('localhost', 'root', 'Karelia', 'geo_data')
	con.connect()
	select_main = con.cursor()
	select_main.execute('call total_pop_2019')
	rows = select_main.fetchall()
	con.close()
	columns =  [i[0] for i in select_main.description]
	municipality = [i[0] for i in rows[:10]]
	population = [int(i[1]) for i in rows[:10]]
	return columns,municipality,population

def check_user(email_username,password):
	select_main = con.cursor()
	select_main.callproc('check_email_password',(email_username,password))
	rows = select_main.fetchall()
	con.commit()
	return rows

def check_new_user(email,username):
	select_main = con.cursor()
	select_main.callproc('check_new_user',(email,username,))
	rows = select_main.fetchall()
	con.commit()
	return rows

def create_new_user(username,email,home_town,password):
	insert_main = con.cursor()
	insert_main.callproc('create_new_user',(username,email,home_town,password))
	con.commit()
	
def check_day_tasks(date,username):
	select_main = con.cursor()
	select_main.callproc('check_day_tasks',(date,username))
	rows = select_main.fetchall()
	con.commit()
	return rows
