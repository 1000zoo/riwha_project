from haversine import haversine

#test1 / raw : 10

origin = (36.63595,	127.3166667)

center_lat = 36.63599792
center_lng = 127.3166771
center = (center_lat, center_lng)
side_lat = 36.63587083
side_lng = 127.3166458
side = (side_lat, side_lng)
lane1_mid_lat = center_lat - abs(center_lat - side_lat) / 6
lane1_mid_lng = center_lng + abs(center_lng - side_lng) / 6
lane1_mid = (lane1_mid_lat, lane1_mid_lng)
dist1 = haversine(lane1_mid, center, unit="m")
err1 = haversine(lane1_mid, origin, unit="m")
err1_bool = 5.409179945 < dist1


lane2_mid_lat = (side_lat + center_lat) / 2
lane2_mid_lng = (side_lng + center_lng) / 2
lane2_mid = (lane2_mid_lat, lane2_mid_lng)
err2 = haversine(lane2_mid, origin, unit="m")
err2_bool = 5.409179945 < 8.998053527

lane3_mid_lat = side_lat + abs(center_lat - side_lat) / 6
lane3_mid_lng = side_lng + abs(center_lng - side_lng) / 6
lane3_mid = (lane3_mid_lat, lane3_mid_lng)
dist3 = haversine(side, lane3_mid, unit="m")
err3 = haversine(lane3_mid, origin, unit="m")
err3_bool = 8.998053527 < dist3

print("lane1")
print(dist1)
print(err1)
print(err1_bool)
print("lane2")
print(err2)
print(err2_bool)
print("lane3")
print(dist3)
print(err3)
print(err3_bool)




