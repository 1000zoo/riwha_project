from flask import Flask, render_template
import serial
import time
import signal
import threading
from haversine import haversine
import pandas as pd
from pandas import Series
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
import timeit


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
#lat2 = cat1.tolist()
#lng2 = cat2.tolist()
lat = 0
lng = 0

calmin1 = 0
calmin2 = 0


lane = pd.read_csv('0106_lanetest.csv', encoding='cp949')
df = pd.read_csv('0106_lanetest.csv', encoding='cp949')
lane1 = lane['lat']
lane2 = lane['lng']
lanelat = lane1.tolist()
lanelng = lane2.tolist()

center1 = lane['clat']
center2 = lane['clng']
clat = center1.tolist()
clng = center2.tolist()

side1 = lane['lat2']
side2 = lane['lng2']
lat2 = side1.tolist()
lng2 = side2.tolist()

save1 = open("/home/riwha/disconnect.txt","w")
save2 = open("/home/riwha/log.txt","a")



#쓰레드 종료용 시그널 함수
def handler(signum, frame):
     exitThread = True

#데이터 처리할 함수
def parsing_data(data):
    # 리스트 구조로 들어 왔기 때문에
    # 작업하기 편하게 스트링으로 합침
    tmp = ''.join(data)
    #time.sleep(1)
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

#        lat = 36.63458333333
#        lng = 127.3205
        
        
      #  print(lat)
      #  print(lng)

    
    



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



    
def lane(ser):

    # 쓰레드 종료될때까지 계속 돌림
    while not exitThread:
        #데이터가 있있다면
        for c in ser.read():
            #line 변수에 차곡차곡 추가하여 넣는다.
            line.append(chr(c))

            
            if c == 10: #라인의 끝을 만나면..
                #데이터 처리 함수로 호출

                parsing_data(line)
                
                start1 = (lat, lng)
                
                lanelist=[]
                cenlist=[]
                goal1list=[]
                goal2list=[]
                
                latdist = 0.02 * 0.01
                lngdist = 0.02 * 0.015
                
                latmin = lat - latdist
                latmax = lat + latdist
                lngmin = lng - lngdist
                lngmax = lng + lngdist

                
                start = timeit.default_timer()
                
                filter_a = (df['lat'] > latmin) & (df['lat'] < latmax)
                filter_b = (df['lng'] > lngmin) & (df['lng'] < lngmax)
                #result = df.loc[0]
                gps_filter = filter_a & filter_b
                result = df.loc[gps_filter,['lat','lng']]
                df1 = result
                
                
                r_lat = df1['lat'].values.tolist()
                r_lng = df1['lng'].values.tolist()
                
                
                filter1_a = (df['clat'] > latmin) & (df['clat'] < latmax)
                filter1_b = (df['clng'] > lngmin) & (df['clng'] < lngmax)
                gps_filter1 = filter1_a & filter1_b
                result1 = df.loc[gps_filter1,['clat','clng']]
                df2 = result1
                
                r_clat = df2['clat'].values.tolist()
                r_clng = df2['clng'].values.tolist()
                

                filter2_a = (df['lat2'] > latmin) & (df['lat2'] < latmax)
                filter2_b = (df['lng2'] > lngmin) & (df['lng2'] < lngmax)
                gps_filter2 = filter2_a & filter2_b
                result2 = df.loc[gps_filter2,['lat2','lng2']]
                df3 = result2
                
                r_lat2 = df3['lat2'].values.tolist()
                r_lng2 = df3['lng2'].values.tolist()                
                
                total = len(r_lat) + len(r_clat) + len(r_lat2)
                

                    
                print('전체 csv 개수 :', len(lanelat), file = save2)
                print('필터링 구간 개수 :', 'side -', len(r_lat), ', center -', len(r_clat), 'side2 -', len(r_lat2), ', total -', total, file = save2)
                print('전체 csv 개수 :', len(lanelat))
                print('필터링 구간 개수 :', 'side -', len(r_lat), ', center -', len(r_clat), 'side2 -', len(r_lat2), ', total -', total)
                
                


                
                #print(r_clat)
                if len(r_lat) > 0 and len(r_clat) > 0:
                    try:
                        for i in range(len(r_lat)):
                   

                            goal1 = (r_lat[i], r_lng[i])
                    
                            lanedist = haversine(start1, goal1, unit='m')
#                            a.append(dist)
#                            print(dist)

                            lanelist.append(lanedist)
                            goal1list.append(goal1)
                            
                        for i in range(len(r_clat)):
                    
                            goal2 = (r_clat[i], r_clng[i])
                            cendist = haversine(start1, goal2, unit='m')
                            cenlist.append(cendist)
                            goal2list.append(goal2)

                
                        distmin = min(lanelist)
                        cenmin = min(cenlist)
                
#                        distmin1 = round(distmin, 1)
#                        cenmin1 = round(cenmin, 1)
                
                        distindex = lanelist.index(min(lanelist))
                        cenindex = cenlist.index(min(cenlist))
                        #cenmin = cenmin1 - 0.5
                
                        sidegps = goal1list[distindex]
                        cengps = goal2list[cenindex]
                
                        print('lat : ', lat, file = save2)
                        print('lng : ', lng, file = save2)
                        print('lat : ', lat)
                        print('lng : ', lng)
                    

                
                        calmin1 = abs(distmin - cenmin)
                        calmin2 = round(calmin1, 1)
                
                        print('side index : ' , distindex, file = save2)
                        print('side gps : ' , sidegps, file = save2)
                
                        print('center index : ' , cenindex, file = save2)
                        print('center gps : ' , cengps, file = save2)
                
                
                        print('side index : ' , distindex)
                        print('side gps : ' , sidegps)
                
                        print('center index : ' , cenindex)
                        print('center gps : ' , cengps)
                
                 
                        print("sidemin: ", distmin, file = save2)
                        print("cenmin: ", cenmin,  file = save2)
                        print("calmin1: ", calmin1, file = save2)
              
                        print("sidemin: ", distmin)
                        print("cenmin: ", cenmin)
                        print("calmin1: ", calmin1)     
                
                 
                        if cenmin <= 3.5 and cenmin < distmin:
                            print('lane1', file = save2)
                            print('lane1')
                        #lane1 = 1
                    

                        elif distmin <= 3.5 and distmin < cenmin:
                            print('lane3', file = save2)
                            print('lane3')
                            #lane1 = 3            
                
                        elif calmin1 <= 3.5 :
                            print('lane2', file = save2)
                            print('lane2')
                            #lane1 = 2    
                        
                        end = timeit.default_timer()
                        total1 = end - start
                        print('total time = %0.7f'%(total1))
                        print('total time = %0.7f'%(total1), file = save2)
                    
                    
                    
                
                    
                                
                
                
                        print ("----------------------------", file = save2)

                
                        del line[:]
                    except ValueError:
                        pass

		
		





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
    
    
    thread1 = threading.Thread(target=lane, args=(ser,))
    thread1.daemon = True


    #시작!
    thread.start()
    thread1.start()


    app.run()



