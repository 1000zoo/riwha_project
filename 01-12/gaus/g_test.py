import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd


data = pd.read_excel('test01.xlsx', sheet_name=0)
xMax = 12
xMin = -12
lane1Center = (5*xMin + xMax) / 6
lane2Center = (xMax + xMin) / 2
lane3Center = (xMin + 5*xMax) / 6
laneToCenter = 3.5
dx = 5000
Tx = (xMax - xMin) / dx
x = np.linspace(xMin, xMax, dx)

pdf1 = stats.norm(lane1Center, 2).pdf(x)
pdf2 = stats.norm(lane2Center, 2).pdf(x)
pdf3 = stats.norm(lane3Center, 2).pdf(x)

l1_data = data['lane1']
l2_data = data['lane2']
l3_data = data['lane3']

lane1 = []
lane2 = []
lane3 = []
count = 0
# plt.plot(x,pdf1)
# plt.savefig('pdf1_' + str(count) + '.jpg')
# plt.clf()
for d in l1_data:
    count = count + 1
    mu = d - laneToCenter
    newPdf = stats.norm(mu,8).pdf(x)
    plt.plot(x,newPdf)
    plt.savefig('pdf1_' + str(count) + '.jpg')
    plt.clf()
    
count = 0
# plt.plot(x,pdf2)
# plt.savefig('pdf2_' + str(count) + '.jpg')
# plt.clf()
for d in l2_data:
    count = count + 1
    mu = d
    newPdf = stats.norm(mu,8).pdf(x)
    plt.plot(x,newPdf)
    plt.savefig('pdf2_' + str(count) + '.jpg')
    plt.clf()
    
    
count = 0
# plt.plot(x,pdf3)
# plt.savefig('pdf3_' + str(count) + '.jpg')
# plt.clf()
for d in l3_data:
    count = count + 1
    mu = d + laneToCenter
    newPdf = stats.norm(mu,8).pdf(x)
    plt.savefig('pdf3_' + str(count) + '.jpg')
    plt.clf()
        