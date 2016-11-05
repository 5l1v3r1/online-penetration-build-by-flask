# -*- coding:utf-8 -*-
def check_ip(ip):
    ip_list = ip.split(".")
    if len(ip_list)==4:
        for x in ip_list:
            for s in x:
                try:
                    if ord(s)<=57 and ord(s)>=48:
                        pass
                    else:
                        return 0
                except:
                    return 0
        return 1
    else:
        return 0


def check_weakpasswd(s=''):
    if s=='1':
        return 1
    else:
        return 0
