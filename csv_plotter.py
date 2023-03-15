import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fnt
titleFont =     {'fontname': 'C059', 'size': 13}
axesFont =      {'fontname': 'C059', 'size': 9}
ticksFont =     {'fontname': 'SF Mono', 'size': 7}
errorStyle =    {'mew': 1, 'ms': 1, 'capsize': 3, 'color': 'blue', 'ls': ''}
pointStyle =    {'mew': 1, 'ms': 1, 'color': 'blue'}
pointStyleB =   {'mew': 1, 'ms': 1, 'color': 'black'}
pointStyleG =   {'mew': 1, 'ms': 1, 'color': 'green'}
pointStyleO =   {'mew': 1, 'ms': 1, 'color': 'orange'}
pointStyleP =   {'mew': 1, 'ms': 1, 'color': 'purple'}
pointStyleR =   {'mew': 1, 'ms': 1, 'color': 'red'}
pointStyleY =   {'mew': 1, 'ms': 1, 'color': 'yellow'}
pointStyleHP =  {'mew': 1, 'ms': 1, 'color': 'hotpink'}
lineStyle =     {'linewidth': 0.5}
lineStyleBold = {'linewidth': 1}
histStyle =     {'facecolor': 'green', 'alpha': 0.5, 'edgecolor': 'black'}
font = fnt.FontProperties(family='C059', weight='normal', style='normal', size=8)

team_names_96 = ['Jagiellonian5_99816','FiscalFuries_21347','Lzxssx_522213','revitpo_711911','theMoneyMakers_420698','HIMS_1453','Globetrotters_20813']
team_names_176 = ['revitpo_711911', 'Globetrotters_20813', 'GrowmoreAP_772629', 'Hannystars_17', 'Ad2f2marmar_314159', 'ReadyTraderHoe_9698', 'Jagiellonian5_99816','FiscalFuries_21347']

Time,Team,BuyVolume,SellVolume,EtfPosition,FuturePosition,EtfPrice,FuturePrice,TotalFees,AccountBalance,ProfitOrLoss = np.loadtxt("FiscalFuries_21347/match96.csv", delimiter=",", unpack=True, skiprows=1)
Team0, Team1, Team2, Team3, Team4, Team5, Team6, Team7 = [],[],[],[],[],[],[], []
Team0_Time, Team1_Time, Team2_Time, Team3_Time, Team4_Time, Team5_Time, Team6_Time, Team7_Time = [],[],[],[],[],[],[],[]

for i in range(len(Time)):
    if Team[i] == 0:    Team0_Time.append(Time[i])
    elif Team[i] == 1:  Team1_Time.append(Time[i])
    elif Team[i] == 2:  Team2_Time.append(Time[i])
    elif Team[i] == 3:  Team3_Time.append(Time[i])
    elif Team[i] == 4:  Team4_Time.append(Time[i])
    elif Team[i] == 5:  Team5_Time.append(Time[i])
    elif Team[i] == 6:  Team6_Time.append(Time[i])
    elif Team[i] == 7:  Team7_Time.append(Time[i])

for j in range(len(Time)):
    if Team[j] == 0:    Team0.append(ProfitOrLoss[j])
    elif Team[j] == 1:  Team1.append(ProfitOrLoss[j])
    elif Team[j] == 2:  Team2.append(ProfitOrLoss[j])
    elif Team[j] == 3:  Team3.append(ProfitOrLoss[j])
    elif Team[j] == 4:  Team4.append(ProfitOrLoss[j])
    elif Team[j] == 5:  Team5.append(ProfitOrLoss[j])
    elif Team[j] == 6:  Team6.append(ProfitOrLoss[j])
    elif Team[j] == 7:  Team7.append(ProfitOrLoss[j])
    
plt.plot(Team0_Time, Team0, 'x', label = team_names_96[0] + ", Profit or Loss", **pointStyleR)
plt.plot(Team1_Time, Team1, 'x', label = team_names_96[1] + ", Profit or Loss", **pointStyleO)
plt.plot(Team2_Time, Team2, 'x', label = team_names_96[2] + ", Profit or Loss", **pointStyleY)
plt.plot(Team3_Time, Team3, 'x', label = team_names_96[3] + ", Profit or Loss", **pointStyleG)
plt.plot(Team4_Time, Team4, 'x', label = team_names_96[4] + ", Profit or Loss", **pointStyle)
plt.plot(Team5_Time, Team5, 'x', label = team_names_96[5] + ", Profit or Loss", **pointStyleP)
plt.plot(Team6_Time, Team6, 'x', label = team_names_96[6] + ", Profit or Loss", **pointStyleB)

Time,Team,BuyVolume,SellVolume,EtfPosition,FuturePosition,EtfPrice,FuturePrice,TotalFees,AccountBalance,ProfitOrLoss = np.loadtxt("FiscalFuries_21347/match176.csv", delimiter=",", unpack=True, skiprows=1)
Team0, Team1, Team2, Team3, Team4, Team5, Team6, Team7 = [],[],[],[],[],[],[], []
Team0_Time, Team1_Time, Team2_Time, Team3_Time, Team4_Time, Team5_Time, Team6_Time, Team7_Time = [],[],[],[],[],[],[],[]

plt.title("Profit or Loss, Match 96", **titleFont)
plt.xlabel('Time', **axesFont)
plt.ylabel('Profit or Loss', **axesFont)
plt.xticks(**ticksFont)
plt.yticks(**ticksFont)
plt.ticklabel_format(useMathText=True)
plt.legend(loc='upper left', prop=font)
plt.show()

for i in range(len(Time)):
    if Team[i] == 0:    Team0_Time.append(Time[i])
    elif Team[i] == 1:  Team1_Time.append(Time[i])
    elif Team[i] == 2:  Team2_Time.append(Time[i])
    elif Team[i] == 3:  Team3_Time.append(Time[i])
    elif Team[i] == 4:  Team4_Time.append(Time[i])
    elif Team[i] == 5:  Team5_Time.append(Time[i])
    elif Team[i] == 6:  Team6_Time.append(Time[i])
    elif Team[i] == 7:  Team7_Time.append(Time[i])

for j in range(len(Time)):
    if Team[j] == 0:    Team0.append(ProfitOrLoss[j])
    elif Team[j] == 1:  Team1.append(ProfitOrLoss[j])
    elif Team[j] == 2:  Team2.append(ProfitOrLoss[j])
    elif Team[j] == 3:  Team3.append(ProfitOrLoss[j])
    elif Team[j] == 4:  Team4.append(ProfitOrLoss[j])
    elif Team[j] == 5:  Team5.append(ProfitOrLoss[j])
    elif Team[j] == 6:  Team6.append(ProfitOrLoss[j])
    elif Team[j] == 7:  Team7.append(ProfitOrLoss[j])

plt.title("Profit or Loss, Match 176", **titleFont)
plt.plot(Team0_Time, Team0, 'x', label = team_names_176[0] + ", Profit or Loss", **pointStyleR)
plt.plot(Team1_Time, Team1, 'x', label = team_names_176[1] + ", Profit or Loss", **pointStyleO)
plt.plot(Team2_Time, Team2, 'x', label = team_names_176[2] + ", Profit or Loss", **pointStyleY)
plt.plot(Team3_Time, Team3, 'x', label = team_names_176[3] + ", Profit or Loss", **pointStyleG)
plt.plot(Team4_Time, Team4, 'x', label = team_names_176[4] + ", Profit or Loss", **pointStyle)
plt.plot(Team5_Time, Team5, 'x', label = team_names_176[5] + ", Profit or Loss", **pointStyleP)
plt.plot(Team6_Time, Team6, 'x', label = team_names_176[6] + ", Profit or Loss", **pointStyleB)
plt.plot(Team7_Time, Team7, 'x', label = team_names_176[7] + ", Profit or Loss", **pointStyleHP)

plt.xlabel('Time', **axesFont)
plt.ylabel('Profit or Loss', **axesFont)
plt.xticks(**ticksFont)
plt.yticks(**ticksFont)
plt.ticklabel_format(useMathText=True)
plt.legend(loc='upper left', prop=font)
plt.show()
