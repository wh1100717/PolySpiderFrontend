#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import json
from src.dao import StatusDao

urls = (
	'/get_today_status_by_platform', 'GetTodayStatusByPlatform',
	'/status_today', 'StatusToday',
	'/status_history', 'StatusHistory',
)

class GetTodayStatusByPlatform:
	def GET(self):
		platform = web.ctx.query.get('platform')
		return json.dumps(StatusDao.get_today_status_by_platform(platform))

class StatusToday:
	def GET(self):
		status_json = json.dumps(StatusDao.status_today())
		print status_json
		return status_json

class StatusHistory:
	def GET(self):
		status_history = StatusDao.status_history()
		return json.dumps(status_history)

app_status = web.application(urls, locals())