# -*- coding: utf-8 -*-

import datetime
import os,time

while(True):
    if(datetime.datetime.now().minute%5==0):
        os.system('python myMap.py')
        print(str(datetime.datetime.now()))
        time.sleep(70)
    time.sleep(2)
