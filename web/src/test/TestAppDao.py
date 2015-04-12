#!/usr/bin/env python
# -*- coding: utf-8 -*-

#=======================
#### file: testAppDao.py ####
#=======================

import sys
import os
import nose
from nose import with_setup
c_path = os.getcwd()
base_path = c_path[:c_path.rfind("src")]
sys.path.append(base_path)
from src.dao import AppDao

def setup_module(module):
	print "单元测试开始"

def teardown_func(module):
	print "单元测试结束"

def setup_func():
	print "set up test fixtures"

def teardown_func():
    print "tear down test fixtures"

def test_should_be_implemented():
	print "\n1. 	ShouldBeImpelemented测试开始"
	the_target_result = "Specific result should be outputed using below method"
	assert True
	# assert AppDao.some_method_should_be_implemented_in_the_future(the_input_paras) == the_target_result

def test_get_app_count():
	print "\n2. 	AppCount测试开始"
	app_count = AppDao.get_app_count()
	print "取到的app_count是：", app_count 
	assert app_count >= 0

def Test_get_app_by_app_id():
	print "\n3. 	GetAppByAppId测试开始"
	result =AppDao.get_app_by_app_id(-3)
	print result['app_name']
	assert result['app_name']


if __name__ == "__main__":
	test_get_app_count()