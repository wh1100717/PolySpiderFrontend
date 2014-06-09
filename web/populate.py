#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import redis
import time
import MySQLdb
import traceback

'''
    #REDIS配置地址
    *   host: 填写Redis服务器名称或者IP
    *   password: 添加Redis服务器的密码，默认为空
    *   port: 服务器端口，默认为6379
    *   db: redis中配置的数据库编号，默认为0
'''
REDIS = {
    'host':'10.0.1.202',
#   'host': 'localhost',
    'password':'',
    'port':6379,
    'db':0
}

'''
    #MYSQL数据库配置
    *   strat_app_id应用开始id号
    *   end_app_id应用结束id号
    *   app_total要获取的应用总数，默认300
'''
MySQL={
    'host':'localhost',
    'password':'123456',
    'user':'root',
    'db':'test',
    'charset':'utf8',
    'port':3306
}

CATEGORY_NAME = {
    '0'   :'未分类',  
    '1000':'个性化',
    '1100':'交通运输',
    '1200':'体育',
    '1300':'健康与健身',
    '1400':'动态壁纸',
    '1500':'动漫',
    '1600':'医药',
    '1700':'商务',
    '1800':'图书与工具书',
    '1900':'天气',
    '2000':'娱乐',
    '2100':'媒体与视频',
    '2200':'小部件',
    '2300':'工具',
    '2400':'摄影',
    '2500':'效率',
    '2600':'教育',
    '2700':'新闻杂志',
    '2800':'旅游与本地出行',
    '2900':'生活时尚',
    '3000':'社交',
    '3100':'财务',
    '3200':'购物',
    '3300':'软件与演示',
    '3400':'通讯',
    '3500':'音乐与音频',
    '3600':'游戏',
    '3700':'其他'
}


class HotApps:
    
    def __init__(self, args):
        pool = redis.ConnectionPool(host=REDIS['host'], password=REDIS['password'], port=REDIS['port'], db=REDIS['db'])
        self.redis_client = redis.Redis(connection_pool=pool)
        self.conn = MySQLdb.connect(host=MySQL['host'],user=MySQL['user'],passwd=MySQL['password'],db=MySQL['db'],port=MySQL['port'],charset=MySQL['charset'])
        self.app_max = args.app_max
        self.weight = args.weight

    def _filter(self, app):
        if not app: return False
        try:
            categories = app['category'].encode('utf8','ignore').split(',')
            print "processing ",app['app_name']
            w = 0
            for t in categories:
                val = int(t.split(':')[1])
                w += 10 if val > 1000 else val
            if w < self.weight: return False
            if len(app['app_detail'])==1 and app['app_detail'][0]['platform']=='googleplay': return False
        except Exception, e:
            print Exception, e
            print traceback.format_exc()
            return False
        return True

    def _save_app_to_mysql(self, app):
        try:
            cur = self.conn.cursor()
            query_sql = "SELECT * from mdm_disapp_appinfo where app_name = '%s'" %app[1]
            count = cur.execute(query_sql)
            if count == 0:
                insert_sql = "INSERT INTO mdm_disapp_appinfo (app_version, app_name, app_package, app_icon, app_size, app_type, app_from, app_url, app_desc,platform, create_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cur.execute(insert_sql, app)
                self.conn.commit()
        except Exception, e:
            print Exception, e
            print traceback.format_exc()
        finally:
            cur.close()


    def _get_category_name_by_id(self,category_id):
        category_name = CATEGORY_NAME.get(category_id)
        return category_name if category_name else "无"

    def populate(self):
        start_index = 0
        while True:
            if start_index >= self.app_max: break
            if start_index + 100 > self.app_max:
                end_index = start_index - self.app_max
            else:
                end_index = start_index + 100
            print "start to populate apps from %d to %d" %(start_index, end_index)
            app_list = self.redis_client.lrange('app::data', start_index, end_index)
            if len(app_list) == 0: break
            for app in app_list:

                if not app: continue
                try:
                    app = eval(app)
                    #获取app分类
                    app_type = app['category'].encode('utf8', 'ignore').split(',')
                    app_type.sort(key=lambda x:int(x.split(':')[1]))
                    app_type = self._get_category_name_by_id(app_type[0].split(':')[0])
                    #app名称
                    app_name = app['app_name'].encode('utf8', 'ignore')
                    #获取app的package_name
                    app_package = app['package_name'].encode('utf8', 'ignore')
                    #获取app详细信息type=list
                    app_details = app['app_detail']
                    #获取第一个详细信息type=dict
                    app_detail = app_details[0]
                    #获取app_version
                    app_version = app_detail['version'].encode('utf8', 'ignore')
                    #获取app_platform
                    platform = 'Android'
                    #获取apk_url
                    app_url = app_detail['apk_url'].encode('utf8', 'ignore')
                    #获取cover
                    app_icon = app_detail['cover'].encode('utf8', 'ignore')
                    #获取app_size
                    app_size = 0
                    #获取app_from
                    app_from = app_detail['platform'].encode('utf8', 'ignore')
                    #获取app_desc
                    app_desc = 'null'
                    #获取download_times
                    app_download_times = app_detail['download_times'].encode('utf8', 'ignore')
                    #获取cover
                    cover = app_detail['cover']
                    #获取creat_time
                    # create_time = app1_detail['last_update'].encode('utf8', 'ignore')
                    create_time = '2014-3-14'
                    #Mysql数据库
                    print "processing: ", app_name
                    app_info = (app_version,app_name,app_package,app_icon,app_size,app_type,app_from,app_url,app_desc,platform,create_time)
                    self._save_app_to_mysql(app_info)
                except Exception, e:
                    print Exception, e
                    print traceback.format_exc()
            start_index += 100
            

if __name__ == "__main__":
    import argparse

    print "use `python populate.py -h[--help]` to find more configuration"

    start_time = time.time()
    # 通过argParse进行命令行配置
    parser = argparse.ArgumentParser(description='Populate most hot apps')
    # 设置需要抓取的城市
    parser.add_argument('-m', type=str, dest="app_max", default=2000,
                        help="config the max hot apps number, 2000 by default")
    parser.add_argument('-w', type=int, dest="weight", default=6, help="config the weight to filter apps, 6 by default")
    args = parser.parse_args()

    hot_apps = HotApps(args)
    hot_apps.populate()

    end_time = time.time()
    print "consume time: %s secs" %(end_time - start_time)


