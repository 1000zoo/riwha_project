import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd


data = pd.read_excel('test01.xlsx', sheet_name=3)
xMax = 5.25
xMin = -5.25
lane1Center = (5*xMin + xMax) / 6
lane2Center = (xMax + xMin) / 2
lane3Center = (xMin + 5*xMax) / 6
laneToCenter = (xMax - xMin) / 6
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
    newPdf = stats.norm(mu,2*abs(d)).pdf(x)
    pdf1 = pdf1 * newPdf
    s = pdf1.sum() * Tx
    pdf1 = pdf1 / s
    if count % 10 == 0:
        lane1.append(abs(-3.5-x[np.argmax(pdf1)]))
        # plt.plot(x,pdf1)
        # plt.savefig('pdf1_' + str(count / 10) + '.jpg')
        # plt.clf()
        pdf1 = stats.norm(lane1Center,2).pdf(x)
    # plt.plot(x,pdf1)
    # plt.savefig('pdf1_' + str(count) + '.jpg')
    
count = 0
# plt.plot(x,pdf2)
# plt.savefig('pdf2_' + str(count) + '.jpg')
# plt.clf()
for d in l2_data:
    count = count + 1
    mu = d
    newPdf = stats.norm(mu,2*abs(d)).pdf(x)
    pdf2 = pdf2 * newPdf
    s = pdf2.sum() * Tx
    pdf2 = pdf2 / s
    if count % 10 == 0:
        lane2.append(abs(x[np.argmax(pdf2)]))
        # plt.plot(x,pdf2)
        # plt.savefig('pdf2_' + str(count / 10) + '.jpg')
        # plt.clf()
        pdf2 = stats.norm(lane2Center,2).pdf(x)
    # plt.plot(x,pdf2)
    # plt.savefig('pdf2_' + str(count) + '.jpg')
        
count = 0
# plt.plot(x,pdf3)
# plt.savefig('pdf3_' + str(count) + '.jpg')
# plt.clf()
for d in l3_data:
    count = count + 1
    mu = d + laneToCenter
    newPdf = stats.norm(mu,2*abs(d)).pdf(x)
    pdf3 = pdf3 * newPdf
    s = pdf3.sum() * Tx
    pdf3 = pdf3 / s
    if count % 10 == 0:
        lane3.append(abs(3.5-x[np.argmax(pdf3)]))
        # plt.plot(x,pdf3)
        # plt.savefig('pdf3_' + str(count / 10) + '.jpg')
        # plt.clf()
        pdf3 = stats.norm(lane3Center,2).pdf(x)
    # plt.plot(x,pdf3)
    # plt.savefig('pdf3_' + str(count) + '.jpg')
        
dataFrame = pd.DataFrame({
    'lane1' : lane1,
    'lane2' : lane2,
    'lane3' : lane3
})

dataFrame.to_excel('test_result.xlsx')