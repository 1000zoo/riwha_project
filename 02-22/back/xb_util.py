import math
import numpy as np

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
    
    a = np.rad2deg(z)
    if(a < 0):
        a = 180 + (180 + a)
    return a

def string_to_dict(s):
    dic = {}
    ls = s.split("/")
    for w in ls:
        if w != "":
            try:
                w_ = w.split(":")
                dic[w_[0]] = w_[1]
            except IndexError as err:
                print(err)
                dic = {}
                return dic
    return dic
        


def str_to_flist(t):
    t = t.strip("("")")
    if not t.__contains__(","):
        raise IndexError
    k = t.split(",")
    k[0] = float(k[0])
    k[1] = float(k[1])
    return k

