# -*- coding:utf-8 -*-

def FilterList(alist):#过滤列表相同元素
    return list(set(alist))

def addWord(dic,key,value):
    #存在就天机key:value到字典dic，不存在就新建个字典key
    dic.setdefault(key,value)

if __name__=='__main__':
    d={}
    addWord(d,'1',1)
    print d['1']+1
    
