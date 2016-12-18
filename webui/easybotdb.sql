drop database if exists easybotdb;
create database easybotdb;
use easybotdb;

create table t_dialogs
(
	dialog_id int unsigned primary key not null auto_increment,
	dialog_type varchar(10) not null,
	dialog_time varchar(20) not null,
	req_msg varchar(200) not null,
	res_msg varchar(200) not null,
	req_user varchar(20) not null,
	res_user varchar(20) not null,
	remark varchar(20) default ''
 );

create table t_user
(
	user_id int unsigned primary key not null auto_increment,
	user_type varchar(10) not null,  
	user_name varchar(20) not null,
	password varchar(20) default '',
	email varchar(30) default ''
	address varchar(100) default '',
	avatar varchar(200) default '',
	remark varchar(20) default ''
);
