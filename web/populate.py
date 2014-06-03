#!/usr/bin/env python
# -*- coding: utf-8 -*-



import sys
import os
import redis
import time


'''
	#REDIS配置地址
	*	host: 填写Redis服务器名称或者IP
	*	password: 添加Redis服务器的密码，默认为空
	*	port: 服务器端口，默认为6379
	*	db: redis中配置的数据库编号，默认为0
'''
REDIS = {
    'host':'10.0.1.202',
#	'host': 'localhost',
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


class HotApps:
    
    def __init__(self, args):
        pool = redis.ConnectionPool(host=REDIS['host'], password=REDIS['password'], port=REDIS['port'], db=REDIS['db'])
        self.redis_client = redis.Redis(connection_pool=pool)
        self.conn = MySQLdb.connect(host=MySQL['host'],user=MySQL['user'],passwd=MySQL['password'],db=MySQL['db'],port=MySQL['port'],charset=MySQL['charset'])
        self.app_max = args.app_max
        self.weight = args.weight

    def _filter(self, app):
        if not app: return False
        categories = app['category'].encode('utf8','ignore').split(',')
        w = 0
        for t in categories:
            val = int(t.split(':')[1])
            w += 10 if val > 1000 else val
        if w < self.weight: return False
        if len(app['app_detail'])==1 and app['app_detail'][0]['platform']=='googleplay': return False

    def _save_list_to_mysql(self, app_list):
        cur = self.conn.cursor()
        sql = "INSERT INTO mdm_disapp_appinfo (app_version, app_name, app_package, app_icon, app_size, app_type, app_from, app_url, app_desc,platform, create_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.executemany(sql,app_list)
        cur.close()

    def populate(self):
        start_index = 0
        while True:
            print "start to populate apps from %d to %d", %(start_index, start_index + 100)
            app_list = redis_client.lrange('app:data', start_index, start_index + 100)
            app_infos = []
            if len(app_list) == 0: break
            for app in app_list:
                if not app: continue
                app = eval(app)
                if not self._filter(app): continue
                app_info = []
                app_infos.push(app_info)
            #持久化到mysql
            self._save_list_to_mysql(app_infos)




def get_app_info_bycategory(app_total):
    app_infos=[]
    popular_app_num=redis_client.llen('app::mostpopular')
    app_lists = redis_client.lrange('app::mostpopular',popular_app_num-app_total,popular_app_num)
    for app_list in app_lists:
        app_list=eval(app_list)
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
        #下载app_icon_file
        #CommonUtil.download_icon(cover,app_name)
    

    
    return app_infos








#通过category获取app信息，传入起始和终止数，返回一个list
def get_app_info_bycategory(part_start_app_num,part_end_app_num,app_total):
    
    #app_lists = redis_client.lrange('app::data',35,2000)
    app_lists = redis_client.lrange('app::data',part_start_app_num,part_end_app_num)
    app_infos=[]
    for app in app_lists:
        app = eval(app)
        if len(app)==6:
            #通过sort对category重新排序，将app_type存成分类数最大的分类+分类数的和，方便在最后的排序
            
            app_type=app['category'].encode('utf8', 'ignore')
            app_type=app_type.split(',')
            app_type.sort(key=lambda x:int(x.split(':')[1]))
            flag=False
            num=0
            for tmp in app_type:
                tmp=int(tmp.split(':')[1])
                num+=tmp
            if num>=level:
                app_type=app_type[0].split(':')[0]+':'+str(num)
                flag=True
            if len(app['app_detail'])==1 and app['app_detail'][0]['platform']=='googleplay':
                flag=False
            if flag==True:
            

                #app名称
                app_name = app['app_name'].encode('utf8', 'ignore')
                
                #Mysql数据库
                app_info=[app_name,app_type]
                app_infos.append(app_info)
                #下载app_icon_file
                #CommonUtil.download_icon(cover,app_name)
            flag=False
    
        
    
   
   
    return app_infos




#数据迁移
def save_2000apps(app_total=apps_total):
    all_app_num=int(redis_client.get('app::amount'))
    redis_client.delete('app::mostpopular')
    app_num=0
    get_app_info=[]
    for i in range(100):
        print i
        
        part_start_app_num=(all_app_num/100)*(i)
        part_end_app_num=(all_app_num/100)*(i+1)
        app_infos=get_app_info_bycategory(part_start_app_num,part_end_app_num,app_total)
        get_app_info+=app_infos
        app_num+=len(app_infos)
    
    get_app_info.sort(key=lambda x:int(x[1].split(':')[1]))
    for i in range(len(get_app_info)):
        redis_client.rpush('app::mostpopular',i)
        redis_client.lset('app::mostpopular',i,get_app_info[i])




    

if __name__ == "__main__":
    import argparse

    start_time = time.time()
    # 通过argParse进行命令行配置
    parser = argparse.ArgumentParser(description='Populate most hot apps')
    # 设置需要抓取的城市
    parser.add_argument('-m', type=str, dest="app_max", default=2000,
                        help="config the max hot apps number, 2000 by default")
    parser.add_argument('-w', type=int, desct="weight", default=6, help="config the weight to filter apps, 6 by default")
    args = parser.parse_args()

    hot_apps = HotApps(args)
    hot_apps.populate()

    end_time = time.time()
    print "consume time: %s secs" %(end_time - start_time)


