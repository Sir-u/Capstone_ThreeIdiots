create DATABASE mydatabase;
use mydatabase;
show databases;
show tables;

CREATE TABLE userinfo (
    uid VARCHAR(25) NOT NULL PRIMARY KEY,
    gender INT,
    age INT
);

CREATE TABLE message (
    type varchar(100) PRIMARY KEY,
    morpheme varchar(100),
    speechAct varchar(30) NOT NULL,
    speechReAct varchar(30),
    gender INT,
    age INT
);

insert into userinfo
values('turtle648', 1, 25);

-- gender : 남성의경우 1, 여성의 경우 2