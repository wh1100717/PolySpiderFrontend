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
        category_num=str(i)+'00'
        category=redis_client.hget('app::category',category_num)
        if category!=None:
            category=eval(category)
            categorys[str(i)+'00']=len(category)
    return categorys

def app_list(page_index = 1,row_number = 20):
    '''
    ##获取app_list
    '''
    result = []
    app_list = redis_client.get_items('app::data', (page_index-1)*row_number+1, page_index * row_number + 1)
    for app in app_list:
        if app == "0":continue
        app_item = []
        app = eval(app)
        app_item.append(app['app_id'])
        app_item.append(app['app_name'])
        app_item.append(app['package_name'])
        app_item.append(CategoryUtil.get_category_name_by_id(app['category'][0:4]))
        button = '''
            <a href='https://github.com/wh1100717/PolySpider' target='_blank' class='demo-button'>More</a>
        '''
        app_item.append(button)
        result.append(app_item)
    return result

def get_app_list(page_index = 1,row_number = 20):
    '''
    ##获取app_list
    '''
    result = []
    app_list = redis_client.get_items('app::data', (page_index-1)*row_number+1, page_index * row_number + 1)
    for app in app_list:
        app_item = []
        app = eval(app)
        app_item.append(app['app_id'])
        app_item.append(app['app_name'])
        app_item.append(app['package_name'])
        app_item.append(CategoryUtil.get_category_name_by_id(app['category'][0:4]))
        button = '''
            <a href='https://github.com/wh1100717/PolySpider' target='_blank' class='demo-button'>More</a>
        '''
        app_item.append(button)
        result.append(app_item)
    return result

def get_app_count():
    '''
    ##获取应用总数
    '''
    return redis_client.get('app::amount')


def platform_statistic():
    platform=['baiduapp','xiaomi','googleplay','hiapk','muzhiwan','appchina']
    platform_app_counts={}
    for i in platform:
        print i
        platform_app_count=redis_client.hget('app::platform',i)
        if platform_app_count!=None:
            platform_app_count=eval(platform_app_count)
            if platform_app_count==0:
                platform_app_counts[i]=0
            else:
                platform_app_counts[i]=len(platform_app_count)
    return platform_app_counts


def get_app_list_by_categroy(category,page_index = 1,row_number = 200):
    apps=redis_client.hget('app::category',category)
    apps=eval(apps)
    apps=list(apps)
    apps.sort()
    result=[]
    
    app_list=redis_client.get_items_with_index_list('app::data',apps[(page_index-1)*row_number:page_index*row_number])
    for app in app_list:
        if app == "0":continue
        app_item = []
        app = eval(app)
        app_item.append(app['app_id'])
        app_item.append(app['app_name'])
        app_item.append(app['package_name'])
        app_item.append(CategoryUtil.get_category_name_by_id(app['category'][0:4]))
        button = '''
            <a href='https://github.com/wh1100717/PolySpider' target='_blank' class='demo-button'>More</a>
        '''
        app_item.append(button)
        result.append(app_item)
    return result


def get_app_list_by_platform(platform,page_index = 1,row_number = 20):
    apps=redis_client.hget('app::platform',platform)
    apps=eval(apps)
    apps=list(apps)
    apps.sort()
    result=[]
    
    app_list=redis_client.get_items_with_index_list('app::data',apps[(page_index-1)*row_number:page_index*row_number])
    for app in app_list:
        if app == "0":continue
        app_item = []
        app = eval(app)
        app_item.append(app['app_id'])
        app_item.append(app['app_name'])
        app_item.append(app['package_name'])
        app_item.append(CategoryUtil.get_category_name_by_id(app['category'][0:4]))
        button = '''
            <a href='https://github.com/wh1100717/PolySpider' target='_blank' class='demo-button'>More</a>
        '''
        app_item.append(button)
        result.append(app_item)
    return result    
