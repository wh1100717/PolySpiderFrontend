#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import json
from src.dao import AppDao
from src.util import CategoryUtil
from src.util import StringUtil


urls = (
	'/get_app_by_app_name', 'GetAppByAppName',
	'/get_app_by_app_id', 'GetAppByAppId',
	'/get_app_count', 'GetAppCount',
	'/app_list/(.*)','AppList',
	'/get_app_list','GetAppList',
	'/get_app_list_by_default', 'GetAppListByDefault',
	'/get_app_list_by_platform/(.*)','GetAppListByPlatform',
	'/get_app_list_by_category/(.*)','GetAppListByCategory',
	'/category_statistic', 'CategoryStatistic',
	'/platform_statistic', 'PlatformStatistic',
)
class GetAppByAppName:
	def GET(self):
		paras = StringUtil.convert_query_to_paras(web.ctx.query)
		app_name = paras['app_name']
		app = AppDao.get_app_by_app_name(app_name)
		return json.dumps(app)

class GetAppByAppId:
	def GET(self):
		paras = StringUtil.convert_query_to_paras(web.ctx.query)
		app_id = paras['app_id']
		app = AppDao.get_app_by_app_id(app_id)
		return json.dumps(app)

class GetAppCount:
	def GET(self):
		count = AppDao.get_app_count()
		return json.dumps([{'count':count}])

class CategoryStatistic:
	def GET(self):
                categorys=AppDao.category_statistic()
                result = '['
                for i in categorys:
                    result += '["'+unicode(str(CategoryUtil.get_category_name_by_id(i))) + '",'+str(categorys[i])+'],'
                result=result[:-1] + ']'
		return result

class PlatformStatistic:
	def GET(self):
                platform_App_counts=AppDao.platform_statistic()
                platform_list={
                    "muzhiwan":"拇指玩",
                    "googleplay":"Google市场",
                    "baiduapp":"百度应用市场",
                    "xiaomi":"小米应用市场",
                    "appchina":"应用汇",
                    "hiapk":"安卓市场"
                }
                result = '['
                for i in platform_App_counts:
                    result += '["'+unicode(str(platform_list[i])) + '",'+str(platform_App_counts[i])+'],'
                result=result[:-1] + ']'
                print result
		return result

class AppList:
	def GET(self,page_index):
                paras = StringUtil.convert_query_to_paras(web.ctx.query)
                data = paras['data'].split(':')
                if data[0]=='category':
                    page_index = int(page_index)
                    if page_index == 1:
                            app_list = AppDao.get_app_list_by_categroy(data[1], row_number=1000)
                    else:
                            app_list = AppDao.get_app_list_by_categroy(data[1], page_index=page_index, row_number=5000)
                else:
                    page_index = int(page_index)
                    if data[1] == 'total':
                        if page_index == 1:
                                app_list = AppDao.app_list(row_number=1000)
                        else:
                                app_list = AppDao.app_list(page_index=page_index, row_number=5000)
                    else:
                        if page_index == 1:
                                app_list = AppDao.get_app_list_by_platform(data[1], row_number=1000)
                        else:
                                app_list = AppDao.get_app_list_by_platform(data[1], page_index=page_index, row_number=5000)
                                
                return json.dumps({'aaData':app_list})

class GetAppList:
	def GET(self):
		paras = StringUtil.convert_query_to_paras(web.ctx.query)
		aoData = paras['aoData']
		aoData = StringUtil.aoData_map_convert(aoData)
		print aoData
		iColumns = aoData['iColumns'] #列数
		iDisplayLength = aoData['iDisplayLength'] #展示的行数
		iDisplayStart = aoData['iDisplayStart'] #起始页数
		page_index = iDisplayStart / iDisplayLength + 1
		print page_index
		app_list = AppDao.get_app_list(page_index=page_index, row_number=iDisplayLength)
		iTotalRecords = AppDao.get_app_count()
		iTotalDisplayRecords = iTotalRecords

		return json.dumps({
			'aaData':app_list,
			'iTotalRecords':iTotalRecords,
			'iTotalDisplayRecords':iTotalDisplayRecords,
			'sEcho':aoData['sEcho']})
		# return '{"sEcho":1,"iTotalRecords":67,"iTotalDisplayRecords":67,"aaData": [["QQ", "com.tencent.mobileqq", "\u901a\u8baf", "<a href=\'baidu.com\'>1</a>"]]}'

class GetAppListByDefault:
	def GET(self):
		app_list = AppDao.get_app_list(row_number = 5000)
		iTotalRecords = AppDao.get_app_count()
		iTotalDisplayRecords = iTotalRecords
		return json.dumps({'aaData':app_list,})

class GetAppListByPlatform:
	def GET(self,platform):
		app_list = AppDao.get_app_list_by_platform(platform)
		return json.dumps({'aaData':AppDao.get_app_list_by_platform(platform)})
            
class GetAppListByCategory:
	def GET(self,categroy):
		app_list = AppDao.get_app_list_by_categroy(categroy)
		return json.dumps({'aaData':AppDao.get_app_list_by_categroy(categroy)})

app_app = web.application(urls, locals())
