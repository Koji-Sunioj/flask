
CREATE TABLE `users` (
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created` datetime DEFAULT CURRENT_TIMESTAMP,
  `home_town` varchar(255) NOT NULL,
  `role` varchar(255) DEFAULT 'user',
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `calendar` (
  `cal_id` int(11) NOT NULL AUTO_INCREMENT,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `category` tinytext NOT NULL,
  `title` text NOT NULL,
  PRIMARY KEY (`cal_id`),
  UNIQUE KEY `calendar_inserts` (`start_time`,`end_time`,`username`),
  KEY `username` (`username`),
  CONSTRAINT `calendar_ibfk_1` FOREIGN KEY (`username`) REFERENCES `users` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8041 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `employer` (
  `contract_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `employer` varchar(255) DEFAULT NULL,
  `paydate_month_offset` int(11) DEFAULT NULL,
  PRIMARY KEY (`contract_id`),
  UNIQUE KEY `username` (`username`,`employer`),
  CONSTRAINT `employer_ibfk_1` FOREIGN KEY (`username`) REFERENCES `users` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `contract_rule` (
  `rule_id` int(11) NOT NULL AUTO_INCREMENT,
  `rule_name` varchar(255) DEFAULT NULL,
  `rate` float DEFAULT NULL,
  `start_time` int(11) DEFAULT NULL,
  `end_time` int(11) DEFAULT NULL,
  `target_days` varchar(255) DEFAULT NULL,
  `contract_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`rule_id`),
  KEY `contract_id` (`contract_id`),
  CONSTRAINT `contract_rule_ibfk_1` FOREIGN KEY (`contract_id`) REFERENCES `employer` (`contract_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE `crud` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category` tinytext,
  `post` text,
  `stamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `when_was` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `username` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`,`stamp`),
  KEY `username` (`username`),
  CONSTRAINT `crud_ibfk_1` FOREIGN KEY (`username`) REFERENCES `users` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=647 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `thread_reply` (
  `reply_id` int(11) NOT NULL AUTO_INCREMENT,
  `thread_id` int(11) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `reply` varchar(255) DEFAULT NULL,
  `stamp` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `when_was` varchar(7) DEFAULT 'created',
  PRIMARY KEY (`reply_id`),
  KEY `thread_id` (`thread_id`),
  CONSTRAINT `thread_reply_ibfk_1` FOREIGN KEY (`thread_id`) REFERENCES `crud` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=119 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `reply_comment` (
  `comment_id` int(11) NOT NULL AUTO_INCREMENT,
  `reply_id` int(11) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `comments` varchar(255) DEFAULT NULL,
  `stamp` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `when_was` varchar(7) DEFAULT 'created',
  PRIMARY KEY (`comment_id`),
  KEY `reply_id` (`reply_id`),
  CONSTRAINT `reply_comment_ibfk_1` FOREIGN KEY (`reply_id`) REFERENCES `thread_reply` (`reply_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `calendar_dashboard`(
    IN session_username	varchar(255)
)
begin

select start_time,end_time,category,title 
from calendar 
where username = session_username 
and start_time >= date(now())
order by start_time asc LIMIT 1;

END //

DELIMITER ;

//

CREATE DEFINER=`root`@`localhost` PROCEDURE `check_calendar_data`(
	IN cal_date datetime,
    IN session_username	varchar(255)
)
begin

SELECT cal_id,timestamp(date(start_time)) as 'db_date',start_time,end_time,category,title
FROM geo_data.calendar 
where month(start_time) = month(cal_date) 
and 
year(start_time) =  year(cal_date) 
and 
username = session_username
order by start_time asc;

END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `check_calendar_exists`(
	IN calendar_date datetime
)
begin

select exists(
select * from calendar 
where 
month(start_time) = month(calendar_date) 
and  
year(start_time) = year(calendar_date) 
and title like '%Ikea%') as is_exists;

END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `check_calendar_v2`(
	IN cal_date_start datetime,
    IN cal_date_end datetime,
    IN session_username	varchar(255)
)
begin

SELECT cal_id,timestamp(date(start_time)) as 'db_date',start_time,end_time,title,category 
FROM geo_data.calendar 
where
start_time >= cal_date_start
and username = session_username
and end_time < cal_date_end;

END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `check_day_tasks`(
	IN calendar_date	date,
    IN input_username	varchar(255)
)
begin

select cal_id,timestamp(date(start_time)) as 'db_date',start_time,end_time,title,category
from calendar 
where date(start_time) = calendar_date
and username = input_username
order by start_time asc;

END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `check_email_password`(
	IN email_username 	varchar(255),
    IN input_password	varchar(255)
)
begin

select username,email,home_town,role from users where 
email = email_username and password = input_password 
or 
username = email_username and password = input_password;


END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `check_inserted_data`(
	IN input_year datetime,
    IN input_username varchar(255)
)
begin

select year(start_time),month(start_time) from calendar 
where start_time >= DATE_SUB(input_year,INTERVAL 1 MONTH) 
and end_time  <  DATE_SUB(DATE_ADD(input_year,INTERVAL 1 YEAR) ,INTERVAL 1 MONTH)
and username = input_username
and category = 'work'
group by year(start_time),month(start_time);

END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `check_inserted_data_v2`(
	IN input_year datetime,
    IN input_username varchar(255),
    IN input_employer varchar(255)
)
begin

select year(start_time),month(start_time) from calendar 
where start_time >= DATE_SUB(input_year,INTERVAL 1 MONTH) 
and end_time  <  DATE_SUB(DATE_ADD(input_year,INTERVAL 1 YEAR) ,INTERVAL 1 MONTH)
and username = input_username
and category = 'work'
and title like  CONCAT('%',input_employer,'%')
group by year(start_time),month(start_time);

END //

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


END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `check_roles`(
	IN session_username varchar(255)
)
begin

select exists(select username from users where username = session_username and role = 'admin') 
as 'db_admin';

END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `covid_header`()
BEGIN

select country,cases,deaths,recovered,active,new_record from covid
where record_date = (
select max(record_date) from covid);

END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `create_new_task`(
    IN input_start_time datetime,
    IN input_end_time datetime,
	IN input_username varchar(255),
    IN input_category varchar(255),
    IN input_title varchar(255)
)
BEGIN
insert ignore into calendar (start_time,end_time,username,category,title) 
values (input_start_time,input_end_time,input_username,input_category,input_title);

END //

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

END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `crud_create`(
    IN input_category TINYTEXT,
    IN input_post TEXT,
    IN input_username VARCHAR(255)
)
BEGIN
insert into crud (category, post,username) values (input_category,input_post,input_username);

END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `crud_dashboard`()
BEGIN

SELECT category,post,stamp,when_was,username FROM geo_data.crud where stamp = (select max(stamp) from geo_data.crud);

END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `crud_delete`(
    IN py_id int
)
BEGIN

delete from crud where id = py_id;

END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `crud_read`()
BEGIN

SELECT id,category,post,stamp,when_was,username FROM geo_data.crud order by stamp desc;

END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `crud_reply_insert`(
	IN input_reply_id 		int,
	IN input_username 		varchar(255),
	IN input_reply  		varchar(255)
)
BEGIN


insert into reply_comment (reply_id,username,comments) 
values (input_reply_id,input_username,input_reply);

END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `crud_reply_read`(
	IN input_thread_id	int
)
BEGIN

select thread_reply.thread_id,reply_comment.reply_id,comment_id,reply_comment.username,comments,reply_comment.stamp, reply_comment.when_was
from thread_reply
join reply_comment on reply_comment.reply_id = thread_reply.reply_id
where thread_id = input_thread_id
order by reply_comment.stamp desc;

END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `crud_thread`(
    IN thread_id int
)
BEGIN

select id,category,post, stamp,when_was,username from geo_data.crud where id = thread_id;

END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `crud_thread_insert`(
	IN input_thread_id 		int,
	IN input_username 		varchar(255),
	IN input_reply  		varchar(255)
)
BEGIN

insert into thread_reply (thread_id, reply,username) values (input_thread_id,input_reply,input_username);

END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `crud_thread_read`(
	IN input_thread_id	int
)
BEGIN

	select reply_id,thread_id,username,reply,stamp,when_was from thread_reply
	where thread_id = input_thread_id
	order by stamp desc ;

END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `crud_update_db`(
    IN py_id int,
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

END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `crud_update_form`(
    IN py_id int
)
BEGIN

select category,post from crud where id = py_id;

END //

DELIMITER ;

DELIMITER //


CREATE DEFINER=`root`@`localhost` PROCEDURE `date_compare`()
BEGIN

select record_date from geo_data.covid ORDER BY record_date DESC LIMIT 1;

END

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `date_first_last`()
BEGIN


select min(record_date), max(record_date) from covid;

END //

DELIMITER ;

DELIMITER //


CREATE DEFINER=`root`@`localhost` PROCEDURE `get_all`()
BEGIN

select record_date,covid.country,cases,deaths,recovered,active,new_record,continent from covid
join continent_table on covid.country = continent_table.country;

END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `search_forums`(
	IN search_input	varchar(255)
)
begin

SELECT id,category,post,stamp,when_was,username 
FROM geo_data.crud 
WHERE 
category like  CONCAT('%',search_input,'%')
or post like  CONCAT('%',search_input,'%')
or username like  CONCAT('%',search_input,'%')
or stamp like  CONCAT('%',search_input,'%')
order by stamp desc;

END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `tax_contract_get`(
    IN session_username	varchar(255)
)
begin

select contract_id,username,employer,paydate_month_offset 
from employer
where username = session_username;

END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `tax_years_get`(
    IN input_username	varchar(255)
)
begin

select date(start_time) as 'work_day',
start_time,end_time 
from geo_data.calendar 
where category = 'work' 
and 
username = input_username
order by date(start_time) asc;

END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `tax_years_get_v2`(
    IN input_username	varchar(255),
    IN input_employer	varchar(255)
)
begin

select date(start_time) as 'work_day',
start_time,end_time,title
from geo_data.calendar 
where category = 'work' 
and username = input_username
and title like CONCAT('%',input_employer,'%')
order by date(start_time) asc;

END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `user_profile_get`(
	IN session_username varchar(255)
)
begin

SELECT username,email,created,home_town,password FROM geo_data.users where username = session_username;

END //

DELIMITER ;
			     
DELIMITER //
			     
CREATE DEFINER=`root`@`localhost` PROCEDURE `tax_contract_create`(
    IN session_username varchar(255),
    IN input_employer varchar(255),
    IN input_paydate_month_offset int,
	IN input_base float
)
BEGIN

insert into employer (username,employer,paydate_month_offset,base)
values (session_username,input_employer,input_paydate_month_offset,input_base);
SELECT LAST_INSERT_ID();

END //

DELIMITER ;
			    
DELIMITER //
			     
CREATE DEFINER=`root`@`localhost` PROCEDURE `tax_supplement_create`(
    IN input_rule_name varchar(255),
    IN input_rate float,
    IN input_start_time int,
    IN input_end_time int,
    IN input_target_days varchar(255),
    IN input_contract_id int
)
BEGIN

insert into contract_rule (rule_name,rate,start_time,end_time,target_days,contract_id)
values (input_rule_name,input_rate,input_start_time,input_end_time,input_target_days,input_contract_id);

END //
