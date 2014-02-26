#!/usr/bin/env python
# -*- coding: utf-8 -*-
from src.util import RedisUtil
import MySQLdb

redis_client = RedisUtil.RedisClient()

mysql_client = MySQLdb.connect(host='',user='',passwd='',db='')
cursor = conn.cursor()
sql = "create table if not exists app(app_name varchar(128) primary key, author varchar(32), category varchar(16), package_name varchar(32))"
cursor.execute(sql)
sql = "create table if not exists app_detail(app_name varchar(128) primary key, author varchar(32), category varchar(16), package_name varchar(32))"

app_amount = redis_client.get('app::amount')



page_index = 0

page_count = 100

page_amount = app_amount / page_count

while True:
	if page_index > page_amount: break
	start = page_index * page_count
	end = start + page_count
	data = redis_client.lrange('app::data', start, end)
	#TODO data写入mySQL数据库
	val = ""
	for d in data:
		val = (val,(d['app_name'], d['author'], d['category'], d['package_name']))
	sql = "insert into app(app_name, author, category, package_name) values ('%s', '%s', '%s', '%s')"
	cursor.executemany(sql, val)
	page_index += 1

cursor.close()
conn.close()


