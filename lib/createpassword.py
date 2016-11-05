# -*- coding:utf-8 -*-

import time
import itertools
import re
import os
from lib.oldpasswordAnalyze import AnalyzeGetNumbers
from lib.common import FilterList

class PasswordGenerator(object):
    '''
    Password generator.
    '''
    #常用的密码中关键数字
    _numList = ['123456', '123123', '123123123', '112233', '445566', '456456', \
    '789789', '778899', '321321', '520', '1314', '5201314', '1314520', '147369', \
    '147258', '258', '147', '456', '789', '147258369', '111222', '123', '1234', \
    '12345', '1234567', '12345678', '123456789', '987654321', '87654321', '7654321', \
    '654321', '54321', '4321', '321']

    # 常用前缀列表
    _prefixWords = ['a','qq','yy','aa','abc','qwer','woaini']

    #常用后缀列表,是个镶嵌列表，[0]是英文字符列表,[1]是数字字符列表
    _suffixwords = [['a'],[str(x) for x in xrange(0,10)]]

    #嵌子与嵌子之间，或者嵌子和中心列表的连接字符串
    _connList=['#','*','_','@']

    #伴侣前缀列表
    _partnerPrefixList = ['520','5201314','1314','iloveu','iloveyou']

    def __init__(self,fullname,nickname,birthday,phone,oldpasswd, \
        keynumbers,keywords,lovername,company,qq,weakpasswd):
        '''
        参数:
            传递的参数:
            fullname:    目标全名,每个字的拼音以空格隔开,全小写,最多支持三个字的名字
            nickname:    昵称
            birthday:    生日,格式:19980405
            phone:       电话号码
            oldpasswd:   老密码,是个列表
            keynumbers:  可能出现的数字，是个列表
            keywords:    关键词，是个列表
            lovername:   爱人的姓名,每个字的拼音之间以空格分开，全小写,最多支持三个字的名字
            company:     工作单位全称,每个字的拼音以空格隔开，全小写
            qq:          目标的QQ号
            weakpasswd:  逻辑值，1或者0。1表示在生成的密码前面添加工具内置的弱口令密码
        '''
        self.fullname=fullname
        self.nickname=nickname
        self.birthday=birthday
        self.phone=phone
        self.oldpasswd=oldpasswd   #它里面的数字部分发挥了作用,还需要提取出字符串
        self.keynumbers=keynumbers
        self.keywords=keywords
        self.lovername=lovername
        self.company=company
        self.qq=qq
        self.weakpasswd=weakpasswd  #最后由lastHandlePhase处理

        ###以下是盛放各种需要嵌入其他嵌子和中心列表的词汇的变量
        #推测目标密码可能包含的数字嵌子列表
        self.InnerNumList=[]
        #由一个全名生成的缩写嵌子列表
        self.ShortNameList=[]
        #全名生成的非缩写嵌子列表
        self.FullNameList=[]
        #由公司全名生成的嵌子列表
        self.CompanyList=[]
        #前缀列表嵌子
        self.PrefixList=[]
        #后缀列表嵌子
        self.SuffixList=[]

        #嵌子嵌入的中心列表
        self.MixedKeywordList=[]
        
    
        self.result=[]#最终生成的密码列表

    def __GetBirthNumList(self):#必须把传递过来的生日参数不变化的返回一个
        year = self.birthday[0:4]
        month = self.birthday[4:6]
        day = self.birthday[6:8]
        r =[]
        r += [year+month+day,year,month+day,day,year[2:4],year[2:4]+month+day, \
        day+month+year]
        return r
        
        
        

    def _GetInnerNumList(self):
        r=self._numList#前面的常量
        for i in xrange(0,10):
            r+=[str(i)*x for x in xrange(1,5)]#让每个0至9的数字重复1到4次
        endyear = int(time.strftime("%Y"))
        r += [str(x) for x in range(2000, endyear+1)]#生成年份(2000年至今)
        if self.keynumbers:
            r+=self.keynumbers
        r += self.__GetBirthNumList()
        if self.oldpasswd:  #个人建议从oldpasswd提取出数字内容
            r += AnalyzeGetNumbers(self.oldpasswd)
        return FilterList(r)
    
    def _GetShortNameList(self,fullname=None):
        fullname = fullname if fullname else self.fullname
        if not fullname:
            return []
        else:
            r = []
            func = lambda x:[x, x.title(), x[0].lower(), x[0].upper(), x.upper()]
            nameSplited = fullname.split()
            if len(nameSplited) == 1:
                r += func(nameSplited[0])
            elif len(nameSplited) == 2:
                shortName = nameSplited[0][0].lower() + nameSplited[1][0].lower()
                r += func(shortName)
            else:
                shortName = nameSplited[0][0].lower() + nameSplited[1][0].lower() + nameSplited[2][0].lower()
                r += func(shortName)
                shortNameRS = nameSplited[1][0].lower() + nameSplited[2][0].lower() + nameSplited[0][0].lower()
                shortNameRST = nameSplited[1][0].lower() + nameSplited[2][0].lower() + nameSplited[0][0].title()
                shortNameR = nameSplited[1][0].lower() + nameSplited[2][0].lower() + nameSplited[0]
                shortNameRT = nameSplited[1][0].lower() + nameSplited[2][0].lower() + nameSplited[0].title()
                r += [shortNameRT, shortNameR, shortNameRST, shortNameRS, shortNameRS.upper()]
            return r

    def _GetFullNameList(self,fullname=None):
        fullname = fullname if fullname else self.fullname
        if not fullname:
            return []
        else:
            r = []
            func=lambda x:[x.split(),x.upper().split(),x.title().split()]
            nameSplited=func(fullname)
            if len(nameSplited[0]) == 1:
                r += nameSplited[0]
                r += nameSplited[1]
                r += nameSplited[2]
            elif len(nameSplited[0]) == 2:
                func1=lambda x:[x[0]+x[1],x[1]+x[0]]
                r += func1(nameSplited[0])
                r += func1(nameSplited[1])
                r+= func1(nameSplited[2])
            else:
                r += [''.join(nameSplited[0]),''.join(nameSplited[1]),''.join(nameSplited[2])]
                func2=lambda x:(x[1]+x[2]+x[0])
                r += [func2(nameSplited[0]),func2(nameSplited[1]),func2(nameSplited[2])]
                r += [nameSplited[0][1]+nameSplited[0][2]+nameSplited[1][0]]
            return r
        
    def _GetCompanyList(self,company=None):
        company= company if company else self.company
        if not company:
            return []
        else:
            r=[]
            companySplited=company.split()
            func = lambda x:[x.lower(),x.title(),x.upper(),x[0],x[0].upper()]#5
            for i in xrange(0,len(companySplited)):
                companySplited[i]=func(companySplited[i])
            string=''
            for j in xrange(0,5):
                for i in xrange(0,len(companySplited)):
                    string += companySplited[i][j]
                r.append(string)
            return r

    def _OrderMixed(self, listA, listB):
        if not listA and not listB:
            return []
        r = []
        for a,b in itertools.product(listA, listB):#in后面的部分生成笛卡尔积的元组，这里元组(a,b)
            if len(a+b)>5 and len(a+b)<17:         #设定连接最大长度
                r.append(a+b)
                for j in self._connList:
                    r.append(a+j+b)
        return r

    def _Mixed(self, listA, listB):
        if not listA and not listB:
            return []
        r = []
        for a,b in itertools.product(listA, listB):#in后面的部分生成笛卡尔积的元组，这里元组(a,b)
            if len(a+b)>5 and len(a+b)<17:         #按长度范围筛选密码
                r.append(a+b)
                r.append(b+a)
                for j in self._connList:
                    r.append(a+j+b)
                    r.append(b+j+a)
        return r

    def _DecideAddWhat(self,string):#决定是否添加如果添加，添加数字还是字符，主要用于self.SuffixList注意和self._suffixwords不一样
        #返回2代表不添加
        numlist=re.findall(r"\d+",string)
        i=0
        for stringnumber in numlist:
             i += len(stringnumber)
        j=len(string)-i
        if abs(i-j)<=2:
            return -1
        else:
            if ord(string[-1:])>=48 and ord(string[-1:])<=57:
                return 0
            else:
                return 1
        
            
    def preHandlePhase(self):#生成各种嵌子列表
        self.InnerNumList=self._GetInnerNumList()
        self.ShortNameList=self._GetShortNameList()
        self.FullNameList=self._GetFullNameList()
        self.CompanyList=self._GetCompanyList()
        self.PrefixList=self._prefixWords+[x.upper() for x in self._prefixWords]
        self.SuffixList=self._suffixwords#最后再lastHandlePhase里处理,此处不能做任何加法

    
        self.MixedKeywordList += self.ShortNameList
        self.MixedKeywordList += self.FullNameList
        if self.nickname:
            self.MixedKeywordList.append(self.nickname)
        if self.keywords:
            self.MixedKeywordList += self.keywords

    def mixedPhase(self):
        self.result += self._OrderMixed(self.MixedKeywordList, self.InnerNumList)
        self.result += self._OrderMixed(self.PrefixList,self.MixedKeywordList)
        self.result += self._OrderMixed(self.MixedKeywordList,self.CompanyList)
        self.result += self._Mixed(self.InnerNumList,self.CompanyList)
        
        if self.phone:
            self.result += self._OrderMixed(self.PrefixList+self.MixedKeywordList, [self.phone])
        if self.qq:
            self.result += self._OrderMixed(self.PrefixList+self.MixedKeywordList,[self.qq])
        if self.lovername:
            temlist = self._GetShortNameList(self.lovername)+self._GetFullNameList(self.lovername)
            self.result += self._OrderMixed(self._partnerPrefixList, temlist)

        #可以不和其他密码混合而单独作为密码的处理
        self.MixedKeywordList += self.InnerNumList    
        self.result += self._OrderMixed(self.MixedKeywordList,[''])
        

    def lastHandlePhase(self):#处理self.SuffixList和self.oldpasswd,self.weakpasswd  或者扩展更多智能处理
        PassListWithSuffix=[]
        for i in xrange(0,len(self.result)):
            d=self._DecideAddWhat(self.result[i])
            if d==-1:
                continue
            else:
                for suffixchar in self.SuffixList[d]:
                    PassListWithSuffix.append(self.result[i]+suffixchar)
        SimplePasswordList=[]
        if self.weakpasswd:#数字逻辑型
            f=open('simplepassword','r')#在当前目录打开这个文件
            for p in f.readlines():
                if p.strip("\n")!="":
                    SimplePasswordList.append(p.strip("\n"))
            f.close()
        self.result = SimplePasswordList + self.oldpasswd+self.result + PassListWithSuffix

    
         
    def generator(self):
        self.preHandlePhase()
        self.mixedPhase()
        self.lastHandlePhase()
        
        #可以在这使用过滤函数,不过最好在密码生成流程上尽量不要出现相同密码,这里的建议是为了
        #预防_numList和添加的弱口令密码重复。
        return self.result


if __name__=='__main__':
    pass















        

    
