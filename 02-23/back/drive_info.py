LANE = "lane2"          #주행 차선
DETECTED = True         #차량 감지
GPS = (36.12320100012, 123.532150300)
AZIMUTH_ANGLE = 272.36307549197693

#차선, gps, 방위각, 차량감지 알고리즘 추가
def get_lane():
    return LANE
def get_gps():
    return GPS
def get_azi():
    return round(AZIMUTH_ANGLE, 7)
def is_detected():
    return DETECTED
