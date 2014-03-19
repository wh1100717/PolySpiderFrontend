#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
reload(sys)
c_path = os.getcwd()
base_path=c_path[:c_path.rfind("src")]
sys.path.append(base_path)
import urllib
from src.util import RedisUtil
redis_client = RedisUtil.RedisClient()
#下载app_icon文件 用appid作为文件名
def download_icon(url,appname):
	icon_id=redis_client.hget('app::index', appname.encode('utf-8'))
	if not os.path.exists('icon/'): os.makedirs('icon/')
	urllib.urlretrieve(url,'icon/'+icon_id)
	print filename+'的icon下载完成'