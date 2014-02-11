#!/usr/bin/env python
# -*- coding: utf-8 -*-
from src.util import RedisUtil
from src.util import StringUtil
from src.util import CategoryUtil
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

def category_statistic():
    '''
    ##获取每个分类下应用数量
    '''
    categorys={}
    for i in range(10,38):
        category=redis_client.hget('app:category',str(i)+'00')
        category=eval(category)
        categorys.add(str(i)+'00',len(category))
    return categorys

def get_app_list(page_index = 1,row_number = 100):
    '''
    ##获取app_list
    '''
    app_lists=[]
    for i in range((page_index-1)*row_number,page_index*row_number):
        app_list=[]
        app=eval(redis_client.get_item('app::data',i+1))
        app_list.append(app['app_id'])
        app_list.append(app['app_name'])
        package_name=app['package_name']
        if package_name:
            app_list.append(app['package_name'])
        else:
            app_list.append(app['app_detail'][0]['pakage_name'])        
        app_list.append(CategoryUtil.get_category_name_by_id(app['category'][0:4]))
        app_lists.append(app_list)
    return app_lists
    
def get_app_count():
    '''
    ##获取应用总数
    '''
    return redis_client.get_length('app::data')