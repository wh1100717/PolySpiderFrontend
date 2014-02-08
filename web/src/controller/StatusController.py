#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import json
from src.dao import StatusDao

urls = (
	'/get_today_status', 'GetTodayStatus',
	'/get_today_status_by_platform', 'GetTodayStatusByPlatform',
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

app_status = web.application(urls, locals())