#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import json
from src.dao import AppDao


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
		return json.dumps(AppDao.category_statistic())

class PlatformStatistic:
	def GET(self):
		return json.dumps(AppDao.platform_statistic())


class GetAppList:
	def GET(self):
		return json.dumps(AppDao.get_app_list())
app_app = web.application(urls, locals())