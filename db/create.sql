CREATE DEFINER=`root`@`localhost` PROCEDURE `create`()
BEGIN
/*
create table munic
( 	kunta varchar(15),
	maakunta  varchar(17),
    	latitude float,
    	longitude float,
    
	primary key (kunta)
);

create table pops
(	sample_year MEDIUMINT,
 	kunta varchar(15),
	maakunta  varchar(17),
    	age varchar(7),
    	male MEDIUMINT,
    	female MEDIUMINT,
    
	primary key (sample_year, kunta,age),
	foreign key  (kunta) references munic (kunta)
);


create table covid
(	record_date date,
 	country varchar(32),
	cases int(8),
	eaths int(8),
	recovered int(8),
	active int(8),
	new_record int(8),
 
	primary key (record_date,country) );
 
 
 create table continent_table
(	country varchar(32),
	continent varchar(32),
 
 	primary key (country) );
 
alter table covid
add foreign key (country) references continent_table(country)
on delete cascade;

UPDATE geo_data.continent 
SET 
    country = 'Taiwan'
WHERE
    country = 'Taiwan*'
    
CREATE TRIGGER update_when_was 
	before update ON crud 
	FOR EACH ROW
		 SET new.when_was = 'edited';

create table users 
(	username 	varchar(255) not null,
	email		varchar(255) not null,
    	home_town 	varchar(255) not null,
    	password	varchar(255) not null,
	created 	datetime default now(),
    	primary key(email)

);

create table crud 
(	id tinyint auto_increment,
	category TINYTEXT,
	post TEXT,
    	stamp datetime default now() on update now(),
	when_was varchar(7) default 'created',
   	username varchar(255);

    	primary key(id,stamp),
	foreign key (username) references users(username)
);


create table calendar

( 	cal_id tinyint auto_increment,
	start_time datetime not null,
	end_time  datetime not null,
    	username  varchar(255),
    	category TINYTEXT  not null,
	post TEXT not null,
    
	primary key (cal_id),
    	foreign key (username) references users(username)
);

stored procedures for the app!

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `check_day_tasks`(
	IN calendar_date	date,
    IN input_username	varchar(255)
)
begin

select start_time,end_time,category,post 
from calendar 
where date(start_time) = calendar_date
and username = input_username
order by start_time asc;

END

 //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `check_email_password`(
	IN email_username 	varchar(255),
    IN input_password	varchar(255)
)
begin

select username,email,home_town from users where 
email = email_username and password = input_password 
or 
username = email_username and password = input_password;


END

 //

DELIMITER ;
DELIMITER //


CREATE DEFINER=`root`@`localhost` PROCEDURE `check_new_user`(
	IN input_email	varchar(255),
    IN input_username	varchar(255)
)
begin

select username from users
where username = input_username
or email = input_email;


END
 //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `covid_header`()
BEGIN

select country,cases,deaths,recovered,active,new_record from covid
where record_date = (
select max(record_date) from covid);

END

 //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `create_new_task`(
    IN input_start_time datetime,
    IN input_end_time datetime,
	IN input_username varchar(255),
    IN input_category varchar(255),
    IN input_post varchar(255)
)
BEGIN
insert into calendar (start_time,end_time,username,category,post) 
values (input_start_time,input_end_time,input_username,input_category,input_post);

END


//

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `create_new_user`(
    IN input_username varchar(255),
    IN input_email varchar(255),
	IN input_home_town varchar(255),
    IN input_password varchar(255)
)
BEGIN
insert into users (username, email,home_town,password) values (input_username,input_email,input_home_town,input_password);

END

 //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `crud_create`(
    IN category TINYTEXT,
    IN post TEXT,
    IN username VARCHAR(255)
)
BEGIN
insert into crud (category, post,username) values (category,post,username);

END


 //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `crud_dashboard`()
BEGIN

SELECT category,post,stamp,when_was FROM geo_data.crud where stamp = (select max(stamp) from geo_data.crud);


END

 //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `crud_delete`(
    IN py_id tinyint
)
BEGIN

delete from crud where id = py_id;

END


 //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `crud_read`()
BEGIN

SELECT id,category,post,stamp,when_was,username FROM geo_data.crud order by stamp asc;

END


 //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `crud_update_db`(
    IN py_id tinyint,
    IN py_category TINYTEXT,
	IN py_post TEXT
    
    
)
BEGIN

UPDATE  crud 
SET 
    category = py_category,
    post = py_post
WHERE
    id = py_id;

END


 //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `crud_update_form`(
    IN py_id tinyint
)
BEGIN

select category,post from crud where id = py_id;

END

 //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `date_compare`()
BEGIN

select record_date from geo_data.covid ORDER BY record_date DESC LIMIT 1;

END


 //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `date_first_last`()
BEGIN


select min(record_date), max(record_date) from covid;

END

 //

DELIMITER ;

DELIMITER //


CREATE DEFINER=`root`@`localhost` PROCEDURE `get_all`()
BEGIN

select record_date,covid.country,cases,deaths,recovered,active,new_record,continent from covid
join continent_table on covid.country = continent_table.country;

END

 //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `total_pop_2019`()
BEGIN

select kunta, sum(male) + sum(female) as total  from pops where sample_year = 2019 group by kunta order by total desc;

END

 //

DELIMITER ;




*/
END
