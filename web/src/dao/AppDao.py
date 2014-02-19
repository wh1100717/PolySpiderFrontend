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

def get_app_count():
    '''
    ##获取应用总数
    '''
    return redis_client.get('app::amount')


def get_app_by_app_id(app_id):
    '''
    ##根据app_id来获取app record
    *   input: app_id
    *   output: app::data()
    '''
    return eval(redis_client.get_item('app::data',app_id)) if app_id else None

def get_app_detail_by_app_name(app_name):
    '''
    ##根据app_name来获取app_detail，详细信息
    *   input: app_name
    *   output: app::data['app_detail']
    '''
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
    ##统计每个分类下应用数量
    '''
    categorys={}
    for i in range(10,38):
        category_num=str(i)+'00'
        category=redis_client.hget('app::category',category_num)
        if category!=None:
            category=eval(category)
            categorys[str(i)+'00']=len(category)
    return categorys

def platform_statistic():
    '''
    ##统计平台应用数信息
    '''
    # TODO 需要将平台信息统一写到Config文件中，不直接操作
    # Will be done in v0.5
    platform=['baiduapp','xiaomi','googleplay','hiapk','muzhiwan','appchina']
    platform_app_counts={}
    for i in platform:
        platform_app_count=redis_client.hget('app::platform',i)
        if platform_app_count!=None:
            platform_app_count=eval(platform_app_count)
            if platform_app_count==0:
                platform_app_counts[i]=0
            else:
                platform_app_counts[i]=len(platform_app_count)
    return platform_app_counts

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
        category = \
            '''<div class="btn-group">''' + \
            '''<button class="btn btn-warning dropdown-toggle" data-toggle="dropdown">''' + \
            CategoryUtil.get_category_name_by_id(app['category'][0:4]) + \
            '''<span class="caret"></span></button><ul class="dropdown-menu" role="menu" app_id="''' +\
            str(app['app_id']) + '''"><ul></div>'''
        button = '''<button class="btn btn-info" data-toggle="modal" data-target="#app_detail_modal" onclick="modal_select(''' + str(app['app_id']) + ''');">More</button>'''
        app_item.append(category)
        app_item.append(button)
        result.append(app_item)
    return result

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

'''
    update_category传入app_id,updatecategory
    将updatecategory转化为category_id

'''
def update_category(app_id,updatecategory):
    updatecategory=CategoryUtil.get_category_id_by_name(updatecategory.encode('utf8', 'ignore'))
    app=redis_client.get_item('app::data',app_id)
    app=eval(app)
    categories = app['category'].split(",")
    flag = True
    for index in range(len(categories)):
        category = categories[index]  # 2200:1
        app_category_id = category[:category.find(":")]  # 2200
        if app_category_id == updatecategory:
            categories[index] = app_category_id + ":9999" 
            flag = False
        elif categories[index][(category.find(":")+1):]=='9999':
                categories[index]=category[:category.find(":")]+':1'
    if flag:
            categories.append(updatecategory + ":9999")
    categories = ",".join(category_reorder(categories))
    update_app_category(app_id,categories)
    app['category']=categories
    redis_client.set_item('app::data',app_id,app)
    
def category_reorder(categories):
        length = len(categories)
        for i in range(length - 1):
            for j in range(length - i - 1):
                order_category = categories[j]
                order_category_value = int(order_category[(order_category.find(":") + 1):])
                cmp_category = categories[j + 1]
                cmp_category_value = int(cmp_category[(cmp_category.find(":") + 1):])
                if cmp_category_value > order_category_value:
                    categories[j], categories[j + 1] = categories[j + 1], categories[j]
        return categories

def update_app_category(app_id, category):
    '''
    ##更新app中的分类信息
    *   input: id | category
    '''
    new_categorys=category.split(',')
    for i in range(len(new_categorys)):
        if i==0:
            category_set= redis_client.hget('app::category',int(new_categorys[i].split(':')[0]))
            if category_set:
                category_set=eval(category_set)
                category_set.add(app_id)
                redis_client.hset('app::category',int(new_categorys[i].split(':')[0]),category_set)
            else:
                redis_client.hset('app::category',int(new_categorys[i].split(':')[0]),set([app_id]))
        else:
            category_set= redis_client.hget('app::category',int(new_categorys[i].split(':')[0]))
            if category_set:
                category_set=eval(category_set)
                if app_id in category_set:
                    category_set.remove(app_id)
                    redis_client.hset('app::category',int(new_categorys[i].split(':')[0]),category_set)


# def get_app_list(page_index = 1,row_number = 20):
#     '''
#     ##获取app_list
#     '''
#     result = []
#     app_list = redis_client.get_items('app::data', (page_index-1)*row_number+1, page_index * row_number + 1)
#     for app in app_list:
#         app_item = []
#         app = eval(app)
#         app_item.append(app['app_id'])
#         app_item.append(app['app_name'])
#         app_item.append(app['package_name'])
#         app_item.append(CategoryUtil.get_category_name_by_id(app['category'][0:4]))
#         button = '''
#             <a href='https://github.com/wh1100717/PolySpider' target='_blank' class='demo-button'>More</a>
#         '''
#         app_item.append(button)
#         result.append(app_item)
#     return result