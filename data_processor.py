import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)

Time,Competitor,Operation,OrderId,Instrument,Side,Volume,Price,Lifespan,Fee = np.genfromtxt('match61_events.csv', delimiter=',', skip_header=1, unpack=True, dtype=str)
Time_a, Competitor_a, Operation_a, OrderId_a, Instrument_a, Side_a, Volume_a, Price_a, Lifespan_a, Fee_a = ['Time'], ['Competitor'], ['Operation'], ['OrderId'], ['Instrument'], ['Side'], ['Volume'], ['Price'], ['Lifespan'], ['Fee']

for i in range(len(Time)):
    if Operation[i] != "Cancel":
        Time_a.append(Time[i])
        Competitor_a.append(Competitor[i])
        Operation_a.append(Operation[i])
        OrderId_a.append(OrderId[i])
        Instrument_a.append('0')
        Side_a.append(Side[i])
        Volume_a.append(Volume[i])
        Price_a.append(Price[i])
        Lifespan_a.append(Lifespan[i])
        Fee_a.append(Fee[i])
        
    if Operation[i] == "Cancel" and int(OrderId[i]) < 10000000:
        Time_a.append(Time[i])
        Competitor_a.append(Competitor[i])
        Operation_a.append(Operation[i])
        OrderId_a.append(OrderId[i])
        Instrument_a.append('1')
        Side_a.append(Side[i])
        Volume_a.append(Volume[i])
        Price_a.append(Price[i])
        Lifespan_a.append(Lifespan[i])
        Fee_a.append(Fee[i])
        
    if Operation[i] == "Cancel" and int(OrderId[i]) > 10000000:
        Time_a.append(Time[i])
        Competitor_a.append(Competitor[i])
        Operation_a.append(Operation[i])
        OrderId_a.append(OrderId[i])
        Instrument_a.append('0')
        Side_a.append(Side[i])
        Volume_a.append(Volume[i])
        Price_a.append(Price[i])
        Lifespan_a.append(Lifespan[i])
        Fee_a.append(Fee[i])        

np.savetxt("match_cancel.csv", np.column_stack([Time_a, Instrument_a, Operation_a, OrderId_a, Side_a, Volume_a, Price_a, Lifespan_a]), fmt='%s', delimiter=",")

