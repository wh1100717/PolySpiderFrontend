#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import urllib

def item_to_json(item):
    '''
    对数据库中取到的数据进行json格式化处理
    '''
    if isinstance(item, int):
        return str(item)
    elif isinstance(item, str):
        return '"' + item + '"'
    elif isinstance(item, tuple):
        return item_to_json(list(item))
    elif isinstance(item, list):
        result = "["
        for i in item:
            result += item_to_json(i) + ","
        return result[:-1] + "]"
    elif isinstance(item,dict):
        result = '['
        for i in item:
            result += '['+item_to_json(i) + ','+str(item[i])+'],'
        return result[:-1] + ']'
    else:
        return '"'+ str(item) + '"'

def convert_query_to_paras(query):
    if not query or query == "?": return {}
    paras = {}
    queries = query[1:].split("&")
    for q in queries:
        q = q.split("=")
        if len(q)<2: continue
        paras[q[0].encode('utf8')] = q[1]
    return paras

def aoData_map_convert(paras):
    a = urllib.unquote(paras)
    a = eval(a.replace('true','"true"').replace('false','"false"'))
    aoData = {}
    for data in a:
        aoData[data['name']] = data['value']
    return aoData