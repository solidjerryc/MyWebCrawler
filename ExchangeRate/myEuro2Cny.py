#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 17:35:41 2020

@author: caiboqin
"""

import requests
import time
import smtplib
from email.mime.text import MIMEText

#设置欧元汇率阈值
THRESHOLD=7.7

#设置发件smtp服务器 
mail_host = 'smtp.163.com'  
#发件邮箱用户名
mail_user = '********@163.com'  
#发件邮箱登陆密码
mail_pass = '********'  
#收件人 
receivers = '********@****.com' 

url=f'https://hq.sinajs.cn/rn={int(time.time()*1000)}list=fx_seurcny'

class ExchangeRate:
    '''
    汇率类，存储相关数据
    '''
    #var hq_str_fx_scnyeur="07:05:00,0.12806,0.12816,0.12804,0,0.12806,0.12806,0.12806,0.12806,人民币兑欧元即期汇率,0.02,2e-05,0,OTC Data Services Editorial Team Calculated Cross Rates. New York,0.13347,0.12541,+***-+++,2020-01-01";
    def __init__(self, name, timeStamp, exchangeRate, authority):
        self.name=name
        self.time=timeStamp
        self.exchangeRate=float(exchangeRate)
        self.authority=authority
    
    def __str__(self):
        return '|'.join([str(self.name), str(self.time), str(self.exchangeRate), str(self.authority)])
        
def getExchangeRate(URL):
    '''
    爬取新浪财经汇率数据，返回ExchangeRate对象
    '''
    header={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'hq.sinajs.cn',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    myText=requests.get(url, headers=header).text
    rateStr=myText.split('"')[1]
    rates=rateStr.split(',')
    t=time.mktime(time.strptime(rates[-1]+' '+rates[0],'%Y-%m-%d %H:%M:%S'))
    exchageRate=ExchangeRate(rates[9],t, rates[1], rates[13])
    return exchageRate

def writeCurrentExchangeRate(exRt):
    '''
    缓存当前汇率
    '''
    with open('log', 'w') as f:
        f.write(str(exRt))
    
def readLoggedExchangeRate():
    '''
    读取缓存的上期汇率
    '''
    try:
        with open('log', 'r') as f:
            s=f.read()
        myExRt = s.split('|')
        return ExchangeRate(myExRt[0],myExRt[1],myExRt[2],myExRt[3])
    except:
        return ExchangeRate('','',100,'')
        
def sentEmail(exRt):
    '''
    发送邮件
    '''
    subject = f'欧元汇率已经比预设值低，北京时间{time.strftime("%Y年%m月%d日 %H:%M:%S",time.localtime(exRt.time))}，当前{exRt.name}为{exRt.exchangeRate}，报价来自{exRt.authority}'
    subject=subject.encode()
    
    sender = mail_user
    
    message = MIMEText(subject,'plain','utf-8')
    message['Subject'] = u'欧元汇率已经比预设值低' 
    message['From'] = sender 
    message['To'] = receivers 
    
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host,25)
        smtpObj.login(mail_user,mail_pass) 
        smtpObj.sendmail(sender,receivers,message.as_string()) 
        smtpObj.quit() 
        print('success')
    except smtplib.SMTPException as e:
        print('error',e) 
        
def compare(exRt, threashold):
    lastExRt=readLoggedExchangeRate()
    # 避免发送垃圾邮件，在汇率低于阈值时，本次汇率比上次低0.05元时才发送邮件，或者上次汇率大于阈值本期汇率小于阈值则发送邮件
    if (lastExRt.exchangeRate - exRt.exchangeRate > 0.05 and exRt.exchangeRate < threashold) or (exRt.exchangeRate < threashold and lastExRt.exchangeRate > threashold):
        sentEmail(a)
    writeCurrentExchangeRate(exRt)
    
if __name__=="__main__":
    threashold=THRESHOLD
    while(True):
        a=getExchangeRate(url)
        compare(a, threashold)
        time.sleep(60*60)
    
