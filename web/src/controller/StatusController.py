#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import json
from src.dao import StatusDao

urls = (
	'/get_today_status', 'GetTodayStatus',
	'/get_today_status_by_platform', 'GetTodayStatusByPlatform',
	'/move_staus_patch', 'move_staus_patch',
	'/change_package_location', 'change_package_location',
	'/generate_platform_data', 'generate_platform_data',
)

class GetTodayStatus:
	def GET(self):
		status_json = json.dumps(StatusDao.get_today_status())
		print status_json
		return status_json

class GetTodayStatusByPlatform:
	def GET(self):
		platform = web.ctx.query.get('platform')
		return json.dumps(StatusDao.get_today_status_by_platform(platform))

class move_staus_patch:
	def GET(self):
		StatusDao.move_staus_patch()
		return 1

class change_package_location:
	def GET(self):
		StatusDao.change_package_location()
		return 1

class generate_platform_data:
	def GET(self):
		StatusDao.generate_platform_data()
		return 1

app_status = web.application(urls, locals())