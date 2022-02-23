LANE = "lane2"          #주행 차선
DETECTED = False         #차량 감지
GPS = (36.12320101012, 123.5321500000)
AZIMUTH_ANGLE = 272.36301252342312

#차선, gps, 방위각, 차량감지 알고리즘 추가
def get_lane():
    return LANE
def get_gps():
    return GPS
def get_azi():
    return round(AZIMUTH_ANGLE, 7)
def is_detected():
    return DETECTED
