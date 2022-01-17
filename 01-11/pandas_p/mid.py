from haversine import haversine
from openpyxl import load_workbook
from openpyxl import Workbook
import pandas as pd


for i in range(0, 5):
    
    df = pd.read_excel('work.xlsx', sheet_name=i)
    lat = df['lat']
    lng = df['lng']
    side_index = df['side_index']
    side_lat = df['side_lat']
    side_lng = df['side_lng']
    center_index = df['center_index']
    center_lat = df['center_lat']
    center_lng = df['center_lng']
    side_min = df['side_min']
    cen_min = df['cen_min']
    calmin = df['calmin']
    gps_lane = df['gps_lane']
        
    
    lane1_mid_lat = []
    lane1_mid_lng = []
    lane1_mid_dist = []
    lane1_err_dist = []
    
    lane2_mid_lat = []
    lane2_mid_lng = []
    lane2_err_dist = []
    
    lane3_mid_lat = []
    lane3_mid_lng = []
    lane3_mid_dist = []
    lane3_err_dist = []
    
    for j in range(0, len(lat)):
        origin = [lat[j], lng[j]]
        center = [center_lat[j], center_lng[j]]
        side = [side_lat[j], side_lng[j]]
        #lane1
        lane1_mid_lat.append(center_lat[j] - abs(center_lat[j] - side_lat[j]) / 6)
        lane1_mid_lng.append(center_lng[j] + abs(center_lng[j] - side_lng[j]) / 6)
        lane1_mid = [lane1_mid_lat[j], lane1_mid_lng[j]]
        lane1_mid_dist.append(haversine(center, lane1_mid, unit="m"))
        err_dist1 = haversine(lane1_mid, origin, unit="m")
        if gps_lane[j] == "lane1" and cen_min[j] < lane1_mid_dist[j]:
            lane1_err_dist.append(-err_dist1)
        else:
            lane1_err_dist.append(err_dist1)

        #lane2
        lane2_mid_lat.append((side_lat[j] + center_lat[j]) / 2)
        lane2_mid_lng.append((side_lng[j] + center_lng[j]) / 2)
        lane2_mid = [lane2_mid_lat[j], lane2_mid_lng[j]]
        err_dist2 = haversine(lane2_mid, origin, unit="m")
        if gps_lane[j] == "lane1" or (gps_lane[j] == "lane2" and cen_min[j] < side_min[j]):
            lane2_err_dist.append(-err_dist2)
        else:
            lane2_err_dist.append(err_dist2)
        
        #lane3
        lane3_mid_lat.append(side_lat[j] + abs(center_lat[j] - side_lat[j]) / 6)
        lane3_mid_lng.append(side_lng[j] + abs(center_lng[j] - side_lng[j]) / 6)
        lane3_mid = [lane3_mid_lat[j], lane3_mid_lng[j]]
        lane3_mid_dist.append(haversine(side, lane3_mid, unit="m"))
        err_dist3 = haversine(lane3_mid, origin, unit="m")
        if gps_lane[j] == "lane1" or gps_lane[j] == "lane2" or (gps_lane[j] == "lane3" and side_min[j] > lane3_mid_dist[j]):
            lane3_err_dist.append(-err_dist3)
        else:
            lane3_err_dist.append(err_dist3)

    result = {
        'lane1_mid_lat' : lane1_mid_lat,
        'lane1_mid_lng' : lane1_mid_lng,
        'lane1_mid_dist' : lane1_mid_dist,
        'lane1_err_dist' : lane1_err_dist,
        'lane2_mid_lat' : lane2_mid_lat,
        'lane2_mid_lng' : lane2_mid_lng,
        'lane2_err_dist' : lane2_err_dist,
        'lane3_mid_lat' : lane3_mid_lat,
        'lane3_mid_lng' : lane3_mid_lng,
        'lane3_mid_dist' : lane3_mid_dist,
        'lane3_err_dist' : lane3_err_dist      
    }
    newData = pd.DataFrame(result)
    newData.to_excel('test_result_' + str(i) + '.xlsx')
    