import numpy as np
import matplotlib.pyplot as plt


Time,Team,Operation,BuyVolume,SellVolume,EtfPosition,FuturePosition,EtfPrice,FuturePrice,TotalFees,AccountBalance,ProfitOrLoss,Status = np.loadtxt("score_board.csv", unpack=True, delimiter=",")

plt.plot(EtfPosition, FuturePosition)
plt.show()