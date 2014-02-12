#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from src.util import RedisUtil

redis_client = RedisUtil.RedisClient()

'''
status::(date):
    存储格式为key-map_key-value
    key --> status::(date&platform)
    map_key --> crawled, new, update
    value --> 0, 0, 0
status::history:
    存储除了当天以外的所有爬虫状态历史数据
    存储格式为key-map_key-value
    key --> status::history
    map_key --> date
    value -->   {
                platform1:{
                    crawled:0,
                    new:0,
                    update:0s
                    },
                platform2:{
                    crawled:0,
                    new:0,
                    update:0
                    }
                }
'''

def move_status_into_history(date, platform):
    date = str(date)
    data = redis_client.hget_all('status::' + date + '&' + platform)
    if redis_client.exists('status::history'):
        value = redis_client.hget('status::history', date)
        if value:
            value = eval(value)
            value[platform] = data
            redis_client.hset('status::history', date, value)
        else:
            redis_client.hset('status::history', date, {platform:data})
    else:
        redis_client.hset('status::history', date, {platform:data})
    redis_client.delete('status::' + date + '&' + platform)

def move_staus_patch():
    today = str(datetime.date.today())
    status_key_list = redis_client.keys('status::*&*')
    for status_key in status_key_list:
        if today in status_key: continue
        date = status_key[8:18]
        platform = status_key[19:]
        move_status_into_history(date, platform)

def change_package_location():
    '''
    app::data:
    存储格式为key-index-value
        key --> app::data
        map_key --> app_id 
        value --> 举例： 'app_id':0,'app_name':'QQ','author':'Tencent','category':'社交','app_detail':[{},{}]
    '''
    index = 1
    while True:
        print "index: %d" %index
        data = redis_client.get_item('app::data',index)
        if not data: break
        if data == '0': 
            index += 1
            continue
        try:
            data = eval(data)
            app_detail_list = data['app_detail']
            data['package_name'] = app_detail_list[0]['pakage_name']
            for i in range(len(app_detail_list)):
                del app_detail_list[i]['pakage_name']
            data['app_detail'] = app_detail_list
            redis_client.set_item('app::data',index,data)
            print "process %d item successfully!" %index
        except Exception, e:
            print "except:",e
            redis_client.set_item('app::data',index,0)
        finally:
            index += 1

def generate_platform_data():
    index = 1
    total_app = 0
    while True:
        data = redis_client.get_item('app::data',index)
        if not data: break
        if data == '0':
            index += 1
            continue
        data = eval(data)
        app_detail_list = data['app_detail']
        print "app: %d" %index
        for app_detail in app_detail_list:
            total_app += 1
            print "total_app: %d" %total_app
            platform = app_detail['platform']
            #把key存入对应的'app::platform'的set里面
            platform_keys = redis_client.hget('app::platform',platform)
            if platform_keys:
                platform_keys = eval(platform_keys)
                platform_keys.add(index)
                redis_client.hset('app::platform',platform,platform_keys)
            else:
                redis_client.hset('app::platform',platform,set([index]))
        index += 1

def get_today_status_by_platform(platform):
    today = str(datetime.date.today())
    data = redis_client.hget_all('status::' + today + '&' + platform)
    if not data:
        yesterday = str(today - datetime.timedelta(days = 1))
        if redis_client.exists('status::' + yesterday + '&' + platform):
            move_status_into_history(yesterday, platform)
        data = {'crawled': 0, 'new': 0, 'update': 0}
        redis_client.hset_map('status::' + today + '&' + platform, data)
    return data

def status_incr(platform, map_key):
    today = str(datetime.date.today())
    redis_client.hincr('status::' + today + '&' + platform, map_key)
