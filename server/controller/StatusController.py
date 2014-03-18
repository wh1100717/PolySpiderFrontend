#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import *

class GetCountHandler(BaseHandler):
	def get(self):
		self.write('Status Count:')
		self.write('1000')

handlers = [
	(r"/api/status/get_count", GetCountHandler),
]