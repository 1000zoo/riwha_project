
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


#encoding='utf-8-sig'
df = pd.read_excel('1227_lane2.xlsx')
df = df.dropna(axis=0)

test1 = df[df.test == 'test1']
test2 = df[df.test == 'test2']
test3 = df[df.test == 'test3']
test4 = df[df.test == 'test4']
test5 = df[df.test == 'test5']
test6 = df[df.test == 'test6']



fig3 = px.scatter(test4[60:80], x ='lane2_err_dist',y ='lng', color ='gps_lane',
                 color_discrete_sequence=["red", "green", "blue"],title='12.27 test4 / 22.6%(19/84) 60-80')
fig3.add_trace(go.Scatter(x = df['line1'],y = df['lng'], mode='lines'))
fig3.add_trace(go.Scatter(x = df['line2'],y = df['lng'], mode='lines'))

fig3.show()

#df.loc[:,'err_round'] = round(df['err_dist'],1)
test1.loc[:,'lane2_err_round'] = round(test1['lane2_err_dist'],1)
test2.loc[:,'lane2_err_round'] = round(test2['lane2_err_dist'],1)
test3.loc[:,'lane2_err_round'] = round(test3['lane2_err_dist'],1)
test4.loc[:,'lane2_err_round'] = round(test4['lane2_err_dist'],1)
test5.loc[:,'lane2_err_round'] = round(test5['lane2_err_dist'],1)
test6.loc[:,'lane2_err_round'] = round(test6['lane2_err_dist'],1)


fig1_1 = px.bar(test4, x ='lane2_err_round',y ='lng', color ='gps_lane',
                 color_discrete_sequence=["red", "green", "blue"])
#fig1_1.show()
