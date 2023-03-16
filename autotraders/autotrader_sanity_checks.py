# -*- coding: utf-8 -*-
"""
@author: smell
Definitions overview below, to break the code down into smaller, more easily understood
parts.
Basically, i wanna know where and why it breaks
Many of these defnitions are generalizations that ensure that any of our logical changes to these definitions are applied
throughout the entirety of our code
"""
import numpy as np
import time

def combined_checks(current_time,critical_ON_submit_time,time_cap,instrument, instrument_pos,NET_POSITION,BUY_ACTIVE_ORDER_VOLUME,SELL_ACTIVE_ORDER_VOLUME, MARKET_CAP, BUY_SELL, order_volume,LOT_SIZE,debug_prints,req_limit_check,pos_limit_check):
    req_allowed,time_wasted = req_limit_check(current_time, critical_ON_submit_time, time_cap, debug_prints)
    if req_allowed==True:
        POS_allowed=pos_limit_check(instrument, instrument_pos,NET_POSITION,BUY_ACTIVE_ORDER_VOLUME,SELL_ACTIVE_ORDER_VOLUME, MARKET_CAP, BUY_SELL, order_volume,LOT_SIZE,debug_prints)
        if POS_allowed==True:
            if debug_prints==True:
                print('Time and POS checks completed, order can be placed')
            return True,time_wasted
        elif POS_allowed==False:
            if debug_prints==True:
                print('req limit check succeeded, Position check failed')
            return False,time_wasted
    elif req_allowed == False:
        return False,time_wasted
def req_limit_check(current_time, critical_ON_submit_time, time_cap,debug_prints):
    """Determines if we can place an order by checking if placing an order would breach the rolling order cap.
    returns True if we can place an order without breaching, False if not and a relevant time update.
    Special Scenario: if we somehow went back in time, it tells us by how much and prevents us from ordering
    would need to stop us from ordering for a second, now never lets us place a new order"""
    Delta_time_orders = current_time - critical_ON_submit_time
    if Delta_time_orders > time_cap:
        if debug_prints==True:
            print('Orders per second cap not met, orders can be placed, returning TRUE and the amount of time that passed whilst being allowed to order')
            print('Time since whilst being able to order =', Delta_time_orders-time_cap)
        return True, Delta_time_orders-time_cap
    elif Delta_time_orders < 0:
        if debug_prints == True:
            print('EUREKA! WE TRAVELED BACK IN TIME! maybe the date or year has changed? Returning False, and the difference in time')
            print('Time difference = ', Delta_time_orders)
        return False, Delta_time_orders
    else:
        if debug_prints==True:
            print('Orders per second cap met, no orders can be placed for anorher: %d seconds',Delta_time_orders)
        return False, Delta_time_orders

def pos_limit_check(instrument, instrument_pos,NET_POSITION,BUY_ACTIVE_ORDER_VOLUME,SELL_ACTIVE_ORDER_VOLUME, MARKET_CAP, BUY_SELL, order_volume,LOT_SIZE,debug_prints):
    """Instrument = 0 for the futures, 1 for the ETF.
    instrument_pos takes the position of the instrument we are planning to order from.
    BUY_SELL is 0 if we want to buy the instrument, 1 if we want to sell it.
    BUY_ACTIVE_ORDER_VOLUME = total active bids on etf markets
    SELL_ACTIVE_ORDER_VOLUME = total active asks on etf markets
    ARB_MM = 0 for with fill and kill orders and for hedge orders 
    ARB_MM = 1 if we checking for a new GOOD_FOR_DAY order in the ETF_Market 
    order_volume is the total volume of the order we are trying to place
    LOT_SIZE is the max volume allowed"""
    Net_pos_lim_factor=0
    if order_volume>LOT_SIZE:
        if debug_prints== True:
            print('Order_volume is bigger than the LOT_SIZE, check the volume input,returning False')
            print('Position = instrument_pos')
        return False
    if NET_POSITION!=0: #If we are fully Hedged, we would have limits at 100 at both sides defined and the rest should work properly
        "In case we are not fully hedged, we should make sure that we take the Net position into account"
        if instrument==0: #we are in the HEDGE MARKET
            if BUY_SELL==0: #We are buying FUTURES:
                if NET_POSITION>0:
                    print('ATTEMPT TO BUY FUTURES IN ORDER TO HEDGE OUR ETF POS WHILST OWNING MORE Futures THAN NEGATIVE ETF')
                    return False
                else:
                    if NET_POSITION+order_volume <= 0:
                        if debug_prints==True:
                            print('Futures hedge BUY attempt to get back to the neutral position, does not hedge past a net neutral position')
                        return True
                    else:
                        print('ATTEMPT TO OVERHEDGE WAS MADE')
                        return False
            elif BUY_SELL==1:#we are selling futures:
                if NET_POSITION<0:
                    print('ATTEMPT TO SELL FUTURES IN ORDER TO HEDGE OUR ETF POS WHILE OUR NET ETF POSITION IS NEGATIVE, THIS SHOULD NOT HAPPEN')
                    return False
                else:
                    if NET_POSITION+order_volume>=0:
                        if debug_prints==True:
                            print('Futures hedge SELL attempt to get back to the neutral position, does not hedge past a net neutral position')
                        return True
                    else:
                        print('ATTEMPT TO OVERHEDGE WAS MADE')
                        return False
        if instrument == 1: #We are in the ETF markets, we should check that our orders can't exceed our total position.
            "In order to make sure we can't order too much, we need to take both positions into account, we shouldn't place orders outside of our position tolerance"
            "We CAN Have 200 buy orders on the market if our etf pos is -100 and we own 0 futures, but this is not something we are currently implementing."
            "Theoretically speaking, It may be a good idea to not Hedge at all when we know that the market price is wrong, but we can only do that for 1 minute, LOW PRIORITY FEATURE"
            "Discuss the above discription if we have time left, basically we could go Long or Short"
            "This would also require us to change our hedge order checks in such a way that we can't hedge while our active order positions are too high"
            if BUY_SELL==0: #we buy ETF
                if NET_POSITION>0:
                    "Adittional limit NEEDED, NET position can not exceed 100, so we need an extra correction limit"
                    Net_pos_lim_factor=NET_POSITION
                    if debug_prints==True:
                        print('limiting maximum ETF BUY orders by:',Net_pos_lim_factor)
                    if Net_pos_lim_factor>MARKET_CAP:
                        print('We should have been kicked from the servers at this point')
                        return False
            elif BUY_SELL==1: #we SELL ETF
                if NET_POSITION<0:
                    "Adittional limit NEEDED, NET position can not go below -100, so we need an extra correction limit"
                    Net_pos_lim_factor=np.abs(NET_POSITION)
                    if debug_prints==True:
                        print('limiting maximum ETF SELL orders by:',Net_pos_lim_factor)
                    if Net_pos_lim_factor>MARKET_CAP:
                        print('We should have been kicked from the servers at this point')
                        return False
    
    if BUY_SELL == 0: #this means we are buying
        "ORDER INSERTING CHECK"
        if instrument==0:#checks if we're buying from futures AKA HEDGING
            if instrument_pos + order_volume > MARKET_CAP:
                if debug_prints== True:
                    print('A new BUY Hedge order would breach the maximum amount of Futures we can hold')
                    print('Returning False')
                return False
            elif instrument_pos+order_volume <= MARKET_CAP:
                print('Hedge BUY order would not breach the futures cap,returning True')
                return True
        elif instrument==1: #Checks if we're buying from ETF markets
            if instrument_pos + BUY_ACTIVE_ORDER_VOLUME + order_volume +Net_pos_lim_factor> MARKET_CAP:
                if debug_prints==True:
                    if instrument_pos + order_volume <= MARKET_CAP:
                        print('Whilst a new BUY order would not put us over the position limit directly, we have orders pending that could put us over the cap after, Returning FALSE')
                        
                    elif instrument_pos + order_volume +BUY_ACTIVE_ORDER_VOLUME <= MARKET_CAP:
                        print('The NET market position combined with active orders push us over our tolerance in the market.')
                    else:
                        print('New BUY order could push us over our position limit in ETF')
                        print('Returning False')
                return False
            elif instrument_pos + BUY_ACTIVE_ORDER_VOLUME + order_volume <= MARKET_CAP:
                if debug_prints==True:
                    print('The new BUY order at this volume would not breach our market cap,returning True')
                return True
                
    elif BUY_SELL==1:#this would mean we are selling futures
        if instrument==0:
            if instrument_pos - order_volume < -MARKET_CAP:
                "We check to make sure a new, selling, Hedge ORDER would not cause us to breach our limit in the futures"
                if debug_prints==True:
                    print('New Hedge SELL order would Breach our market cap on the negative side, returning False')
                return False
            elif instrument_pos - order_volume >-MARKET_CAP:
                if debug_prints==True:
                    print('New Hedge SELL order would not breach our market cap on the negative side, returning True')
                return True
        elif instrument==1:#selling etf market
            if instrument_pos-order_volume-SELL_ACTIVE_ORDER_VOLUME <-(MARKET_CAP+Net_pos_lim_factor):
                if debug_prints==True:
                    if instrument_pos - order_volume < -(MARKET_CAP+Net_pos_lim_factor):
                        print('Whilst a new SELL order would not put us over the position limit directly, we have orders pending that could put us over the cap after, Returning FALSE')
                    elif instrument_pos - order_volume -SELL_ACTIVE_ORDER_VOLUME >= -(MARKET_CAP):
                        print('The NET market position combined with the active orders push us over our tolerance in the market.')
                    else:
                        print('New SELL order could push us over our position limit in ETF')
                    print('Returning False')
                return False
            elif instrument_pos-SELL_ACTIVE_ORDER_VOLUME-order_volume >=-MARKET_CAP:
                if debug_prints==True:
                    print('New SELL order would not breach our market cap on the negative side, returning True')
                return True
    

MARKET_CAP = 100        
order_cap = 50
time_cap = 1
recent_orders = np.zeros((order_cap))
current_time=time.time()
critical_ON_submit_time=time.time()-1.1
current_time=time.time()
debug_prints = True

Trade_Allowed, Delta_t = req_limit_check(current_time, critical_ON_submit_time, time_cap, debug_prints)

positions = np.array(([-91,0,91],[91,0,-91]))

SELL_ACTIVE_ORDER_VOLUME_array=np.array((90,91,10))
BUY_ACTIVE_ORDER_VOLUME_array=np.array((90,91,10))
LOT_SIZE =10
order_volume=10
instrument=[0,1]
debug_prints = True
for h in range(len(instrument)):
    for i in range(len(positions[0,:])):
        for j in (0,1):
            for k in range(len(positions[0,:])):
                instrument=h
                instrument_pos=positions[h,i]
                print('instrument=',instrument)
                print('instrument_pos=',instrument_pos)
                BUY_SELL=j
                print('BUY/SELL=',BUY_SELL)
                NET_POSITION=positions[0,i]+positions[1,i]
                print('NET_position = ',NET_POSITION)
                BUY_ACTIVE_ORDER_VOLUME = BUY_ACTIVE_ORDER_VOLUME_array[k]
                print('active buy orders',BUY_ACTIVE_ORDER_VOLUME)
                SELL_ACTIVE_ORDER_VOLUME = SELL_ACTIVE_ORDER_VOLUME_array[k]
                print('active sell orders:',SELL_ACTIVE_ORDER_VOLUME)
                combined_result,timewaste = combined_checks(current_time,critical_ON_submit_time,time_cap,instrument, instrument_pos,NET_POSITION,BUY_ACTIVE_ORDER_VOLUME,SELL_ACTIVE_ORDER_VOLUME, MARKET_CAP, BUY_SELL, order_volume,LOT_SIZE,debug_prints,req_limit_check,pos_limit_check)

                print(combined_result)
