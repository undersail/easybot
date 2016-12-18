drop database if exists easybotdb;
create database easybotdb;
use easybotdb;

create table t_dialogs
(
	dialog_id int unsigned primary key not null auto_increment,
	dialog_type varchar(10) not null,
	dialog_time int unsigned not null,
	req_msg varchar(300) not null,
	res_msg varchar(300) not null,
	req_user varchar(100) not null,
	res_user varchar(100) not null,
	remark varchar(20) default ''
 );

create table t_user
(
	user_id int unsigned primary key not null auto_increment,
	user_type varchar(10) not null,  
	user_name varchar(100) not null,
	password varchar(20) default '',
	email varchar(30) default '',
	address varchar(300) default '',
	avatar varchar(300) default '',
	remark varchar(20) default ''
);
