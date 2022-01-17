from flask import Flask, render_template
import serial
import time
import signal
import threading
from haversine import haversine
import pandas as pd
import sys
import numpy as np
import requests
from queue import Queue
from socket import *
from bs4 import BeautifulSoup
import timeit
import os
import webbrowser
import datetime
import random
import hashlib



#save = open("/home/riwha/출력결과/webid저장시간.txt","a")

app = Flask(__name__)
line = [] #라인 단위로 데이터 가져올 리스트 변수
csv3 = 0
port = '/dev/ttyUSB0' # 시리얼 포트
baud = 4800 # 시리얼 보드레이트(통신속도)

exitThread = False   # 쓰레드 종료용 변수
dist1 = 0
csv = pd.read_csv('camera.csv', encoding='cp949')
cat1 = csv['lat']
cat2 = csv['lng']
dist = 0
lat2 = cat1.tolist()
lng2 = cat2.tolist()
lat = 0
lng = 0
save1 = open("/home/riwha/disconnect.txt","w")



#쓰레드 종료용 시그널 함수
def handler(signum, frame):
     exitThread = True

#데이터 처리할 함수
def parsing_data(data):
    # 리스트 구조로 들어 왔기 때문에
    # 작업하기 편하게 스트링으로 합침
    tmp = ''.join(data)

    #출력!
    if '$GPGGA' in tmp:
        global gps
        global lat
        global lng

        gps = tmp.split(',')
        latsol1=gps[2][0:2]
        latsol2=gps[2][2:8]
        latsol3=float(latsol2)/60
        latsol4=float(latsol1)
        lat=latsol4+latsol3
       
        lngsol1=gps[4][0:3]
        lngsol2=gps[4][3:8]
        lngsol3=float(lngsol2)/60
        lngsol4=float(lngsol1)
        lng=lngsol4+lngsol3
        
#        print(lat)
#        print(lng)

    



#본 쓰레드

def readThread(ser):
    global line
    global exitThread
    global csv2
    global csv3
    global dist

    # 쓰레드 종료될때까지 계속 돌림
    while not exitThread:
        #데이터가 있있다면
        for c in ser.read():
            #line 변수에 차곡차곡 추가하여 넣는다.
            line.append(chr(c))

            if c == 10: #라인의 끝을 만나면..
                #데이터 처리 함수로 호출
                parsing_data(line)
                
                start = (lat, lng)
		 
		
		

                a=[]		
                for i in range(len(lat2)):
                    global csv2

                    goal = (lat2[i], lng2[i])
                    
                    dist = haversine(start, goal, unit='m')
#                    a.append(dist)
#                    print(dist)

                        
                    if dist <= 200.0:

                        csv1=csv.loc[csv["lat"]==lat2[i]]
                        csv2=csv1['webserver']
                        csv2=str(csv2)[5:]

                        qqq = 'https://28no8114.cns-link.net:8443/profile/card%23me'
                        
                        
                        #sys.stdout = open('/home/riwha/disconnect.txt','w')
                        #print(csv2)
                        #print(dist1)


		
                        if csv3 != csv2:
                            try:
                                #sys.stdout = open('/home/riwha/출력결과/전송시간.txt', 'a')                            
                                r = requests.get("http://riwha.com/giveinfo.php?webid="+qqq)
                                print(r.text)
                                csv3 = csv2
                            except:
                                pass



                        if dist < 10.0:
                            disconnect = '1'
                            try:
                                sys.stdout = open('/home/riwha/disconnect.txt','w')
                                print(disconnect)
                            except:
                                pass

                        if dist >= 10.0:
                            connect = '0'
                            try:
                                sys.stdout = open('/home/riwha/disconnect.txt','w')
                                print(connect)
                            except:
                                pass
                #dist1 = dist
                             
                #line 변수 초기화
                del line[:]




@app.route('/senddata')
def senddata():
    return render_template('map.html', data1=lat, data2= lng)

if __name__ == '__main__':

    #종료 시그널 등록
    signal.signal(signal.SIGINT, handler)
    
    q = Queue()

    #시리얼 열기
    ser = serial.Serial(port, baud, timeout=0)

    #시리얼 읽을 쓰레드 생성
    thread = threading.Thread(target=readThread, args=(ser,))
    thread.daemon = True
    

    #시작!
    thread.start()


    app.run()



