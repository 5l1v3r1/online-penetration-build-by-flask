#!/usr/bin/env python
# -*- coding: cp936 -*-

"""
Function: BaiDuIP��ַ��λ
Author:   Saferman
Time:     2016��10��28�� 12:26
"""
import urllib2
import json
 
ak = 'VvSaWxFAHVXhbTpQ9pOKPC7pcRSjZnMw'
#IPΪ��Ĭ�ϱ���IP
def search(ip=""):
    url = "https://api.map.baidu.com/highacciploc/v1?qcip=%s&ak=%s&qterm=pc&extensions=1&coord=bd09ll&callback_type=json" % (ip,ak)
    response = urllib2.urlopen(url)
    html = response.read()
    s = json.loads(html)
    data={}
    data["radius"] = s["content"]["radius"] #��λ�뾶
    data["lng"] = s["content"]["location"]["lng"] #����
    data["lat"] = s["content"]["location"]["lat"] #γ��
    data["formatted_address"] = s["content"]["formatted_address"] #��ϸ��ַ
    data["admin_area_code"] = s["content"]["address_component"]["admin_area_code"]#�����������루���֤ǰ6λ��
    data["map"] = getmap(data["lng"],data["lat"])
    return data
 
def getmap(lng,lat):
    url = "http://api.map.baidu.com/staticimage/v2?ak=%s&width=600&height=400&zoom=11&center=%s,%s" % (ak,lng,lat)
    return url
 
if __name__ == "__main__":
    #print search('')
    pass
