import math
import numpy
from digi.xbee.devices import *
from datetime import datetime
import interface

PORT = 'COM6'
BAUD_RATE = 9600

VEHICLE_ID = "97na1423" #차량 번호

LANE = "lane2"          #주행 차선
DETECTED = False         #차량 감지
GPS = "36.12320100012/123.5321500000"
AZIMUTH_ANGLE = 32.21966388369947

#main
def main():
    global isCallbackOn
    global userInfo
    global broadbee
    interface.main_if()
    userInfo = {}
    broadbee = XBeeDevice(PORT, BAUD_RATE)
    isCallbackOn = False

    try:
        broadbee.open()
        init_user()
        
        while True:
            lane_check()
            if not isCallbackOn:
                broadbee.add_data_received_callback(data_receive_callback)
                isCallbackOn = True

            if is_detected():
                gps_update()
                azi_update()
                data_broadcast()
                
            else:
                print("not dectected...")
            time.sleep(5)
            print("end of the function")
            
    except InvalidOperatingModeException as err:
        print(err)

def lane_check():
    userInfo["lne"] = LANE

def gps_update():
    userInfo["gps"] = get_gps()
    
def get_gps():
    return GPS
    
def azi_update():
    userInfo["azi"] = get_azi()

def get_azi():
    return round(AZIMUTH_ANGLE, 7)

def init_user():
    global userInfo
    userInfo = {
        "vId" : VEHICLE_ID,
        "nId" : broadbee.get_node_id(),
    }

def is_detected():
    return DETECTED

def data_receive_callback(xbee_message):
    global isCallbackOn
    
    isCallbackOn = True
    interface.data_receive_callback_if()
    dataReceived = string_to_dict(xbee_message.data.decode())
    print(datetime.now())
    print(dataReceived)
    
    try:
        if dataReceived["lne"] == userInfo["lne"]:
            print("same lane")
            if is_my_back(dataReceived["azi"], dataReceived["gps"]):
                print("gps: %s" % dataReceived["gps"])  #gps 정보 처리 추가
                print("my back car")
                data_send_reactive(dataReceived)
            else:
                print("not my back car")
        else:
            print("diff lane")
            print(dataReceived["lne"], userInfo["lne"])
    except KeyError as err:
        if str(err) == "'gps'":
            pass
        elif str(err) == "'imb'":
            print("Invalid gps data")
        else:
            print("Key '%s' does not exist in data" % err)

def is_my_back(azi, gps):
    myg = str_to_list(get_gps())    #my gps
    reg = str_to_list(gps)          #received gps
    try:
        a = Azimuth(float(myg[0]), float(myg[1]), float(reg[0]), float(reg[1]))
        if abs(float(a) - float(azi)) > 1:
            return True
        else:
            return False
    except IndexError:
        print("Invalid data")
        raise KeyError("imb")
    

def str_to_list(t):
    return t.split("/")

def data_send_reactive(data):
    interface.data_send_reactive_if()
    print("reacting to %s" % data["nId"])
    net = broadbee.get_network()
    reac = net.discover_device(data["nId"])
    broadbee.send_data(reac, str(userInfo))

def data_broadcast():
    interface.data_braodcast_if()
    broadbee.send_data_broadcast(str(userInfo))

def string_to_dict(s):
    dic = {}
    s = s.strip("{""}")
    ls = s.split(",")
    for w in ls:
        try:    
            w = w.split(":")
            dic[w[0].strip(" '")] = w[1].strip(" '")
        except IndexError as err:
            print(err)
            ed = {}
            return ed
    return dic

# 방위각이 180도 차이나면 뒤차
def Azimuth(lat1, lng1, lat2, lng2):
    Lat1 = math.radians(lat1)
    Lng1 = math.radians(lng1)
    Lat2 = math.radians(lat2)
    Lng2 = math.radians(lng2)
    
    y = math.sin(Lng2 - Lng1) * math.cos(Lat2)
    x = math.cos(Lat1) * math.sin(Lat2) - math.sin(Lat1) * \
        math.cos(Lat2) * math.cos(Lng2 - Lng1)
    z = math.atan2(y, x)
    
    a = numpy.rad2deg(z)
    if(a < 0):
        a = 180 + (180 + a)
    return a

if __name__ == '__main__':
    main()