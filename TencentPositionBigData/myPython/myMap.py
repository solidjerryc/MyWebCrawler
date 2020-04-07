# -*- coding: utf-8 -*-
"""
Created on Sun May  5 12:12:19 2019

@author: JerryC
"""

import requests
import json
import numpy as np
import pandas as pd
from retry import retry
import threading
import time,queue

url='https://xingyun.map.qq.com/api/getXingyunPoints'
data='{"count":4,"rank":%s}'

headers={'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '20',
        'Content-Type': 'text/plain;charset=UTF-8'}

@retry(tries=5,delay=2)
def getData(i):
    html=requests.post(url,data%i,headers=headers, timeout=5)
    return json.loads(html.text)

dt=queue.Queue(4)
def getDataThread(data,i):
    dt.put(getData(i))

t=[threading.Thread(target=getDataThread, args=(data,i,)) for i in range(0,4)]
for i in range(0,4):
    t[i].start()

while(t[0].is_alive() or t[1].is_alive() or t[2].is_alive() or t[3].is_alive()):
    time.sleep(1)

out=np.array([])
for i in range(4):
    a=dt.get()
    temp=np.fromstring(a['locs'],sep=',',dtype=np.int16)
    print(temp.shape)
    out=np.append(out,temp)
    
lng=out[::3]/100
lat=out[1::3]/100
data=out[2::3]

df=pd.DataFrame({'lng':lng,'lat':lat,'count':data})
df.to_csv(f'data/{a["time"]}.txt'.replace(':','_'),index=False)
