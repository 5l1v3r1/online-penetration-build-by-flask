#!/usr/bin/env python
# -*- coding: cp936 -*-

"""
Function: BaiDuIP地址定位
Author:   Saferman
Time:     2016年10月28日 12:26
"""
import urllib2
import json
 
ak = 'VvSaWxFAHVXhbTpQ9pOKPC7pcRSjZnMw'
#IP为空默认本机IP
def search(ip=""):
    url = "https://api.map.baidu.com/highacciploc/v1?qcip=%s&ak=%s&qterm=pc&extensions=1&coord=bd09ll&callback_type=json" % (ip,ak)
    response = urllib2.urlopen(url)
    html = response.read()
    s = json.loads(html)
    data={}
    data["radius"] = s["content"]["radius"] #定位半径
    data["lng"] = s["content"]["location"]["lng"] #经度
    data["lat"] = s["content"]["location"]["lat"] #纬度
    data["formatted_address"] = s["content"]["formatted_address"] #详细地址
    data["admin_area_code"] = s["content"]["address_component"]["admin_area_code"]#行政区划代码（身份证前6位）
    data["map"] = getmap(data["lng"],data["lat"])
    return data
 
def getmap(lng,lat):
    url = "http://api.map.baidu.com/staticimage/v2?ak=%s&width=600&height=400&zoom=11&center=%s,%s" % (ak,lng,lat)
    return url
 
if __name__ == "__main__":
    #print search('')
    pass
