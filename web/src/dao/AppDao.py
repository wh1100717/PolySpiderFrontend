#!/usr/bin/env python
# -*- coding: utf-8 -*-
from src.util import RedisUtil

redis_client = RedisUtil.RedisClient()

'''
app::index:
    存储格式为key-map_key-value
        key --> app::index
        map_key --> app_name
        value --> app_id
app::data:
    存储格式为key-index-value
        key --> app::data
        map_key --> app_id 
        value --> 举例： 'app_id':0,'app_name':'QQ','author':'Tencent','category':'社交','app_detail':[{},{}]
   
'''

def get_app_by_app_id(app_id):
    return eval(redis_client.get_item('app::data',app_id)) if app_id else None

def get_app_detail_by_app_name(app_name):
    app_id = redis_client.hget('app::index', app_name.encode('utf-8'))
    return get_app_by_app_id(app_id)['app_detail']


def get_app_by_app_name(app_name):
    '''
    ##根据app_name来获取app record
    *   input: app_name
    *   output: app::data()
    '''
    app_id = redis_client.hget('app::index', app_name.encode('utf-8'))
    return get_app_by_app_id(app_id)

