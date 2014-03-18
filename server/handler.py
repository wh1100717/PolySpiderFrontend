#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from base import *
from controller import AppController
from controller import StatusController

handlers = []
handlers += AppController.handlers #match url `api/app/`
handlers += StatusController.handlers #matching url `api/stauts/`
handlers += [(r"^/(.*)$", BaseHandler)]
