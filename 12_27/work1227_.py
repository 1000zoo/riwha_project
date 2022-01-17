from math import dist
from haversine import haversine
from openpyxl import load_workbook
from openpyxl import Workbook

myExcel = load_workbook('work.xlsx')

for i in range(0, 6):
    m = myExcel.worksheets[i]
    
    lat = m['A']
    lng = m['B']
    side_lat = m['D']
    side_lng = m['E']
    center_lat = m['G']
    center_lng = m['H']
    side_min = m['I']
    cen_min = m['J']
    gps_lane = m['L']
    lane1_mid_lat = m['N']
    lane1_mid_lng = m['O']
    lane1_mid_dist = m['P']
    lane1_err_dist = m['Q']
    lane2_mid_lat = m['R']
    lane2_mid_lng = m['S']
    lane2_err_dist = m['T']
    lane3_mid_lat = m['U']
    lane3_mid_lng = m['V']
    lane3_mid_dist = m['W']
    lane3_err_dist = m['X']

    for j in range(1, len(lat)):
        origin = [lat[j].value, lng[j].value]
        center = [center_lat[j].value, center_lng[j].value]
        side = [side_lat[j].value, side_lng[j].value]
        #lane1
        lane1_mid_lat[j].value = center_lat[j].value - abs(center_lat[j].value - side_lat[j].value) / 6
        lane1_mid_lng[j].value = center_lng[j].value + abs(center_lng[j].value - side_lng[j].value) / 6
        lane1_mid = [lane1_mid_lat[j].value, lane1_mid_lng[j].value]
        lane1_mid_dist[j].value = haversine(center, lane1_mid, unit="m")
        err_dist1 = haversine(lane1_mid, origin, unit="m")
        if gps_lane[j].value == "lane1" and cen_min[j].value < lane1_mid_dist[j].value:
            lane1_err_dist[j].value = -err_dist1
        else:
            lane1_err_dist[j].value = err_dist1

        #lane2
        lane2_mid_lat[j].value = (side_lat[j].value + center_lat[j].value) / 2
        lane2_mid_lng[j].value = (side_lng[j].value + center_lng[j].value) / 2
        lane2_mid = [lane2_mid_lat[j].value, lane2_mid_lng[j].value]
        err_dist2 = haversine(lane2_mid, origin, unit="m")
        if gps_lane[j].value == "lane1" or (gps_lane[j].value == "lane2" and cen_min[j].value < side_min[j].value):
            lane2_err_dist[j].value = -err_dist2
        else:
            lane2_err_dist[j].value = err_dist2
        
        #lane3
        lane3_mid_lat[j].value = side_lat[j].value + abs(center_lat[j].value - side_lat[j].value) / 6
        lane3_mid_lng[j].value = side_lng[j].value + abs(center_lng[j].value - side_lng[j].value) / 6
        lane3_mid = [lane3_mid_lat[j].value, lane3_mid_lng[j].value]
        lane3_mid_dist[j].value = haversine(side, lane3_mid, unit="m")
        err_dist3 = haversine(lane3_mid, origin, unit="m")
        if gps_lane[j].value == "lane1" or gps_lane[j].value == "lane2" or (gps_lane[j].value == "lane3" and side_min[j].value > lane3_mid_dist[j].value):
            lane3_err_dist[j].value = -err_dist3
        else:
            lane3_err_dist[j].value = err_dist3

    
myExcel.save("work1227__.xlsx")

