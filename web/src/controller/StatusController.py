#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import json
from src.dao import StatusDao

urls = (
    '/get_status_list','get_status_list',    
    '/get_status_list_by_platform','get_status_list_by_platform',
    '/get_current_status_by_platform','get_current_status_by_platform',
    '/get_current_status','get_current_status',
)


app_status = web.application(urls, locals())