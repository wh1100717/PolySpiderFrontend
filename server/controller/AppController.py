#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import *

class GetCountHandler(BaseHandler):
	def get(self):
		self.write('App Count:')
		self.write('1000')

handlers = [
	(r"/api/app/get_count", GetCountHandler),
]
