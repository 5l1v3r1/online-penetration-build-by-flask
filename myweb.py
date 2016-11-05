# -*- coding:utf-8 -*-
from flask import Flask,render_template,request
import re
import baiduip
import sys
import whois
from check_lib import *
from lib.createpassword import PasswordGenerator

reload(sys)
sys.setdefaultencoding('utf-8') 
app = Flask(__name__)

@app.route('/',methods=["get","post"])
def index():
    return render_template('ip.html')
#把ip.html放在同一个目录会出现not found错误
#解决办法：http://stackoverflow.com/questions/23435150/python-flask-render-template-not-found
 
@app.route('/ip',methods=["post"])
def BaiduIp():
    if request.method == 'POST':
        ip = request.form.get("search")
        if check_ip(ip)==0:
            return render_template('ip.html')
        data = baiduip.search(ip)
        return render_template('ip.html',data=data,title="高精度IP查询")
    else:
        return render_template('ip.html',title="高精度IP查询")
    
#在线密码生成
@app.route('/password',methods=["get","post"])
def password_build():
    if request.method == 'POST':
        fullname = request.form.get("fullname","")
        nickname = request.form.get("nickname","")
        birthday = request.form.get("birthday","")
        phone = request.form.get("phone","")
        oldpasswd = request.form.get("oldpasswd","").split(',')
        keynumbers = request.form.get("keynumbers","").split(',')
        keywords = request.form.get("keywords","").split(',')
        lovername = request.form.get("lovername","")
        company = request.form.get("company","")
        qq = request.form.get("qq","")
        weakpasswd = check_weakpasswd(request.form.get("weakpasswd",""))##逻辑值1,0
        
        pwgen = PasswordGenerator(fullname=fullname,nickname=nickname,birthday=birthday,phone=phone,oldpasswd=oldpasswd, \
                                  keynumbers=keynumbers,keywords=keywords,lovername=lovername,company=company,qq=qq,weakpasswd=weakpasswd)
        wordlist = pwgen.generator()
        return render_template('password.html',data=wordlist,title="社工密码生成")
    else:
        return render_template('password.html',title="社工密码生成")
#Whois 在线查询
@app.route('/whois',methods=["get","post"])
def whoisa():
    if request.method == 'POST':
        url = request.form.get("search")
        data = whois.whois(url).replace("\n","</br>")
        return render_template('whois.html',data=data,title="Whois查询")
    else:
        return render_template('whois.html',title="Whois查询")
 
if __name__ == '__main__':
    #app.run(host='162.243.128.151',debug=True)
    app.run(host='127.0.0.1',debug=False)

    
