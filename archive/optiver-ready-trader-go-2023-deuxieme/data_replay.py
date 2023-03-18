import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)

Time,Competitor,Operation,OrderId,Instrument,Side,Volume,Price,Lifespan,Fee = np.genfromtxt('match61_events.csv', delimiter=',', skip_header=1, unpack=True, dtype=str)
Time_a, Competitor_a, Operation_a, OrderId_a, Instrument_a, Side_a, Volume_a, Price_a, Lifespan_a, Fee_a = ['Time'], ['Competitor'], ['Operation'], ['OrderId'], ['Instrument'], ['Side'], ['Volume'], ['Price'], ['Lifespan'], ['Fee']

for i in range(len(Time)):
    if Competitor[i] == "":    # Add only bot events.
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

np.savetxt("match_bot_new.csv", np.column_stack([Time_a, Competitor_a, Operation_a, OrderId_a, Instrument_a, Side_a, Volume_a, Price_a, Lifespan_a, Fee_a]), fmt='%s', delimiter=",")

# np.savetxt("match_bot_events.csv", np.column_stack([Time_a, Competitor_a, Operation_a, OrderId_a, Instrument_a, Side_a, Volume_a, Price_a, Lifespan_a, Fee_a]), fmt='%s', delimiter=",")

