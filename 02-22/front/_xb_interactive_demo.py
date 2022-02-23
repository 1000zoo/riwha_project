from digi.xbee.devices import *
from datetime import datetime
import interface
import xb_util as xu
import drive_info as di

PORT = 'COM6'
BAUD_RATE = 9600
VEHICLE_ID = "97fa1006" #차량 번호

#main
def main():
    global isCallbackOn
    global userInfo
    global broadbee
    
    interface.main_if()
    userInfo = {}
    isCallbackOn = False
    broadbee = XBeeDevice(PORT, BAUD_RATE)

    try:
        broadbee.open()
        init_user()
        
        while True:
            lane_update()
            gps_update()
            azi_update()
            if not isCallbackOn:        #콜백함수가 중복되는 것을 막기위해
                broadbee.add_data_received_callback(data_receive_callback)
                isCallbackOn = True

            if di.is_detected():
                data_broadcast()
            else:
                print("not dectected...")
            input()
            print("end of the function")
            
    except InvalidOperatingModeException as err:
        print(err)

#차량 정보 업데이트, 초기에 한 번
def init_user():
    global userInfo
    userInfo = {
        "vId" : VEHICLE_ID,
        "nId" : broadbee.get_node_id(),
    }

#주행 정보 업데이트, 주기적으로
def lane_update():
    userInfo["lne"] = di.get_lane()
def gps_update():
    userInfo["gps"] = di.get_gps()
def azi_update():
    userInfo["azi"] = di.get_azi()


def data_receive_callback(xbee_message):
    global isCallbackOn
    
    isCallbackOn = False
    interface.data_receive_callback_if()
    dataReceived = xu.string_to_dict(xbee_message.data.decode())
    print(datetime.now())
    print(dataReceived)
    
    try:
        if dataReceived["lne"] == userInfo["lne"]:
            print("same lane")
            if is_my_back(dataReceived["azi"], dataReceived["gps"]):
                print("gps: %s" % dataReceived["gps"])  #받은 정보 처리 추가
                print("my back car")
                data_send_reactive(dataReceived["nId"])
            else:
                print("not my back car")
        else:
            print("diff lane")
    except KeyError as err:
        #예외 추가
        if str(err) == "'azi'" or \
            str(err) == "'gps'":
            #답장이 아니라는 뜻
            pass
        elif str(err) == "'imb'":
            print("Invalid gps data")
        else:
            print("Key '%s' does not exist in data" % err)

def is_my_back(azi, gps):
    myg = di.get_gps()   #my gps
    reg = xu.str_to_flist(gps)          #received gps
    try:
        a = xu.Azimuth(myg[0], myg[1], reg[0], reg[1])
        if abs(di.get_azi() - float(azi)) < 1 and \
            abs(float(a) - float(azi)) > 170:
            return True
        else:
            return False
    except IndexError:
        print("Invalid data")
        raise KeyError("imb")

def data_broadcast():
    data_to_send = make_dict_from("lne", "gps", "nId", "azi")       #보낼 정보를 str로 생성
    broadbee.send_data_broadcast(data_to_send)
    
def data_send_reactive(to): #X
    interface.data_send_reactive_if()
    print("reacting to %s" % to)
    data_to_send = make_dict_from("lne", "vId")       #보낼 정보를 str로 생성
    net = broadbee.get_network()
    reac = net.discover_device(to)
    broadbee.send_data(reac, data_to_send)


def make_dict_from(*labels):
    k = ""
    for l in labels:
        try:
            k += l + ":" + str(userInfo[l]) + "/"
        except KeyError as err:
            print("Key '%s' does not exist in data" % err)
    return k

if __name__ == '__main__':
    main()