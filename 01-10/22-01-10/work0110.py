import pandas as pd
from haversine import haversine

data = pd.read_csv('0106_lanetest_opp.csv')


center_lat = data['center_lat']
center_lng = data['center_lng']
lat = data['lat']
lng = data['lng']
clat=[]
clng=[]
dist=[]


haversine

for i in range(0, len(center_lat)):
    clat_ = center_lat[i] - (abs(center_lat[i] - lat[i]) / 7)
    clng_ = center_lng[i] + (abs(center_lng[i] - lng[i]) / 7)
    clat.append(clat_)
    clng.append(clng_)
    cPoint = [clat_, clng_]
    point = [lat[i], lng[i]]
    dist.append(haversine(cPoint, point, unit='m'))
    
result = {
    'center_lat' : center_lat,
    'center_lng' : center_lng,
    'lat' : lat,
    'lng' : lng,
    'clat' : clat,
    'clng' : clng,
    'dist' : dist
}
    
dataFrame = pd.DataFrame(result)
dataFrame.to_csv('result0110_.csv')