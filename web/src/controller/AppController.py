#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import json
from src.dao import AppDao
from src.util import CategoryUtil


urls = (
	'/get_app_by_app_name', 'GetAppByAppName',
	'/get_app_by_app_id', 'GetAppByAppId',
	'/get_app_count', 'GetAppCount',
	'/get_app_list','GetAppList',
	'/category_statistic', 'CategoryStatistic',
	'/platform_statistic', 'PlatformStatistic',
)
class GetAppByAppName:
	def GET(self):
		app_name = web.ctx.query.get('app_name')
		app = AppDao.get_app_by_app_name(app_name)
		return json.dumps(app)

class GetAppByAppId:
	def GET(self):
		app_id = web.ctx.query.get('app_id')
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
                    "baidu":"百度应用市场",
                    "xiaomi":"小米应用市场",
                    "appchina":"应用汇",
                    "hiapk":"安卓市场"
                }
                result = '['
                for i in categorys:
                    result += '["'+unicode(str(platform_list[i])) + '",'+str(platform_App_counts[i])+'],'
                result=result[:-1] + ']'
		return result


class GetAppList:
	def GET(self):
		return json.dumps(AppDao.get_app_list())
app_app = web.application(urls, locals())