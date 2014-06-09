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
    'host':'192.168.1.105',
    'password':'123456',
    'user':'root',
    'db':'test',
    'charset':'utf8',
    'port':3306
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


    def _save_list_to_mysql(self, app_list):
        try:
            cur = self.conn.cursor()
            sql = "INSERT INTO mdm_disapp_appinfo (app_version, app_name, app_package, app_icon, app_size, app_type, app_from, app_url, app_desc,platform, create_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.executemany(sql,app_list)            
        except Exception, e:
            print Exception, e
            print traceback.format_exc()
            return False
        finally:
            cur.close()


    def populate(self):
        start_index = 0
        while True:
            print "start to populate apps from %d to %d" %(start_index, start_index + 100)
            app_list = self.redis_client.lrange('app::data', start_index, start_index + 100)
            app_infos = []
            if len(app_list) == 0: break
            for app in app_list:
                if not app: continue
                try:
                    app = eval(app)
                    if not self._filter(app): continue
                    app_id = redis_client.hget('app::index', app_list[0])
                    app=eval(redis_client.lindex('app::data',app_id))
                    #获取app分类
                    app_type=app_list[1]
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
                    app_size = '0'
                    #获取app_from
                    app_from = app_detail['platform'].encode('utf8', 'ignore')
                    #获取app_desc
                    app_desc = 'null'
                    #获取download_times
                    app_download_times=app_detail['download_times'].encode('utf8', 'ignore')
                    #获取cover
                    cover=app_detail['cover']
                    #获取creat_time
                    # create_time = app1_detail['last_update'].encode('utf8', 'ignore')
                    create_time = '2014-3-14'
                    #Mysql数据库
                    app_info=[app_version,app_name,app_package,app_icon,app_size,app_type,app_from,app_url,app_desc,platform,create_time]
                    
                    app_infos.append(app_info)                    
                except Exception, e:
                    print Exception, e
                    print traceback.format_exc()
            try:
                #持久化到mysql
                self._save_list_to_mysql(app_infos)                
            except Exception, e:
                print Exception, e
                print traceback.format_exc()
    

if __name__ == "__main__":
    import argparse

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


