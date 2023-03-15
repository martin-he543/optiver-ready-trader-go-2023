# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 18:30:57 2023

@author: smell
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 12:20:21 2023

@author: yx200
"""
import time
import numpy as np
import scipy.stats as ss

class myclass():
    
    def __init__(self):
        self.variable = 10
        self.debug_prints = True
        self.critical_ON_submit_time=time.time()-1.1
        self.order_volume = 1
        self.lot_size = 1
        self.time_cap = 1
        self.SELL_ACTIVE_ORDER_VOLUME = 50
        self.BUY_ACTIVE_ORDER_VOLUME = 50
        self.LOT_SIZE =10
        self.MARKET_CAP=10
        self.NET_POSITION=0
    def action(self):
        self.variable += 1
        self.reaction()

    def reaction(self):
        self.variable -= 1
        print('reaction')
    def req_limit_check(self):
        """Determines if we can place an order by checking if placing an order would breach the rolling order cap.
        returns True if we can place an order without breaching, False if not and a relevant time update.
        Special Scenario: if we somehow went back in time, it tells us by how much and prevents us from ordering
        would need to stop us from ordering for a second, now never lets us place a new order"""
        current_time=time.time()
        Delta_time_orders = current_time - self.critical_ON_submit_time
        if Delta_time_orders > self.time_cap:
            if self.debug_prints==True:
                print('Orders per second cap not met, orders can be placed, returning TRUE and the amount of time that passed whilst being allowed to order')
                print('Time since whilst being able to order =', Delta_time_orders-self.time_cap)
            return True, Delta_time_orders-self.time_cap
        elif Delta_time_orders < 0:
            if self.debug_prints == True:
                print('EUREKA! WE TRAVELED BACK IN TIME! maybe the date or year has changed? Returning False, and the difference in time')
                print('Time difference = ', Delta_time_orders)
            return False, Delta_time_orders
        else:
            if self.debug_prints==True:
                print('Orders per second cap met, no orders can be placed for anorher: %d seconds',Delta_time_orders)
            return False, Delta_time_orders
    
    def pos_limit_check(self,instrument, instrument_pos,order_volume,BUY_SELL):
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
        if order_volume>self.LOT_SIZE:
            if self.debug_prints== True:
                print('Order_volume is bigger than the LOT_SIZE, check the volume input,returning False')
                print('Position = instrument_pos')
            return False
        if self.NET_POSITION!=0: #If we are fully Hedged, we would have limits at 100 at both sides defined and the rest should work properly
            "In case we are not fully hedged, we should make sure that we take the Net position into account"
            if instrument==0: #we are in the HEDGE MARKET
                if BUY_SELL==0: #We are buying FUTURES:
                    if self.NET_POSITION>0:
                        print('ATTEMPT TO BUY FUTURES IN ORDER TO HEDGE OUR ETF POS WHILST OWNING MORE Futures THAN NEGATIVE ETF')
                        return False
                    else:
                        if self.NET_POSITION+order_volume <= 0:
                            if self.debug_prints==True:
                                print('Futures hedge BUY attempt to get back to the neutral position, does not hedge past a net neutral position')
                            return True
                        else:
                            print('ATTEMPT TO OVERHEDGE WAS MADE')
                            return False
                elif BUY_SELL==1:#we are selling futures:
                    if self.NET_POSITION<0:
                        print('ATTEMPT TO SELL FUTURES IN ORDER TO HEDGE OUR ETF POS WHILE OUR NET ETF POSITION IS NEGATIVE, THIS SHOULD NOT HAPPEN')
                        return False
                    else:
                        if self.NET_POSITION+order_volume>=0:
                            if self.debug_prints==True:
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
                    if self.NET_POSITION>0:
                        "Adittional limit NEEDED, NET position can not exceed 100, so we need an extra correction limit"
                        Net_pos_lim_factor=self.NET_POSITION
                        if self.debug_prints==True:
                            print('limiting maximum ETF BUY orders by:',Net_pos_lim_factor)
                        if Net_pos_lim_factor>self.MARKET_CAP:
                            print('We should have been kicked from the servers at this point')
                            return False
                elif BUY_SELL==1: #we SELL ETF
                    if self.NET_POSITION<0:
                        "Adittional limit NEEDED, NET position can not go below -100, so we need an extra correction limit"
                        Net_pos_lim_factor=np.abs(self.NET_POSITION)
                        if self.debug_prints==True:
                            print('limiting maximum ETF SELL orders by:',Net_pos_lim_factor)
                        if Net_pos_lim_factor>self.MARKET_CAP:
                            print('We should have been kicked from the servers at this point')
                            return False
        
        if BUY_SELL == 0: #this means we are buying
            "ORDER INSERTING CHECK"
            if instrument==0:#checks if we're buying from futures AKA HEDGING
                if instrument_pos + order_volume > self.MARKET_CAP:
                    if self.debug_prints== True:
                        print('A new BUY Hedge order would breach the maximum amount of Futures we can hold')
                        print('Returning False')
                    return False
                elif instrument_pos+order_volume <= self.MARKET_CAP:
                    print('Hedge BUY order would not breach the futures cap,returning True')
                    return True
            elif instrument==1: #Checks if we're buying from ETF markets
                if instrument_pos + self.BUY_ACTIVE_ORDER_VOLUME + order_volume +Net_pos_lim_factor> self.MARKET_CAP:
                    if self.debug_prints==True:
                        if instrument_pos + order_volume <= self.MARKET_CAP:
                            print('Whilst a new BUY order would not put us over the position limit directly, we have orders pending that could put us over the cap after, Returning FALSE')
                            
                        elif instrument_pos + order_volume +self.BUY_ACTIVE_ORDER_VOLUME <= self.MARKET_CAP:
                            print('The NET market position combined with active orders push us over our tolerance in the market.')
                        else:
                            print('New BUY order could push us over our position limit in ETF')
                            print('Returning False')
                    return False
                elif instrument_pos + self.BUY_ACTIVE_ORDER_VOLUME + order_volume <= self.MARKET_CAP:
                    if self.debug_prints==True:
                        print('The new BUY order at this volume would not breach our market cap,returning True')
                    return True
                    
        elif BUY_SELL==1:#this would mean we are selling futures
            if instrument==0:
                if instrument_pos - order_volume < -self.MARKET_CAP:
                    "We check to make sure a new, selling, Hedge ORDER would not cause us to breach our limit in the futures"
                    if self.debug_prints==True:
                        print('New Hedge SELL order would Breach our market cap on the negative side, returning False')
                    return False
                elif instrument_pos - order_volume >-self.MARKET_CAP:
                    if self.debug_prints==True:
                        print('New Hedge SELL order would not breach our market cap on the negative side, returning True')
                    return True
            elif instrument==1:#selling etf market
                if instrument_pos-order_volume-self.SELL_ACTIVE_ORDER_VOLUME <-(self.MARKET_CAP+Net_pos_lim_factor):
                    if self.debug_prints==True:
                        if instrument_pos - order_volume < -(self.MARKET_CAP+Net_pos_lim_factor):
                            print('Whilst a new SELL order would not put us over the position limit directly, we have orders pending that could put us over the cap after, Returning FALSE')
                        elif instrument_pos - order_volume -self.SELL_ACTIVE_ORDER_VOLUME >= -(self.MARKET_CAP):
                            print('The NET market position combined with the active orders push us over our tolerance in the market.')
                        else:
                            print('New SELL order could push us over our position limit in ETF')
                        print('Returning False')
                    return False
                elif instrument_pos-self.SELL_ACTIVE_ORDER_VOLUME-order_volume >=-self.MARKET_CAP:
                    if self.debug_prints==True:
                        print('New SELL order would not breach our market cap on the negative side, returning True')
                    return True
    def combined_checks(self,instrument,instrument_pos,order_volume,BUY_SELL):
        req_allowed,time_wasted = self.req_limit_check()
        if req_allowed==True:
            POS_allowed=self.pos_limit_check(instrument,instrument_pos,order_volume,BUY_SELL)
            if POS_allowed==True:
                if self.debug_prints==True:
                    print('Time and POS checks completed, order can be placed')
                return True,time_wasted
            elif POS_allowed==False:
                if self.debug_prints==True:
                    print('req limit check succeeded, Position check failed')
                return False,time_wasted
        elif req_allowed == False:
            return False,time_wasted
    def price_estimate(self):
        "simple estimate, could be better, please discuss"
        'just the last traded price'
        return
    def volatility(self):
        "equal to the standard deviation"
        return
    def Black_Scholes_prices(self,BUY_SELL,vol,current_price):
        "Last traded price_futures=input"
        "Standard_deviation ==Volatility"
        "T=Time to exp, in our case, if we put something ON the market, we would have T=2 before a cancel order could take it from the market"
        "but we also have a little lag causing quicker algorithms to be able to buy from us so I'll start at T=3*update ticks"
        "so delta T=3"
        "value of call ="
        deltaT=3
        
        Price_range=np.array([0,1,2,3,4,5])
        d1=(1/(vol*(deltaT)))*(np.log(current_price/(current_price+Price_range)+(vol**2/2)*deltaT))
        d2=d1-vol*deltaT
        Call_value=ss.norm.cdf(d1)*(current_price+Price_range)-ss.norm.cdf(-d1)*(current_price+Price_range)
        Put_value=ss.norm.cdf(d2)*(current_price+Price_range)-ss.norm.cdf(-d2)*(current_price+Price_range)
        return
    
    def BL_SHder(self):
        
        return   
    
    def priority_market_making(self,ETF_market_info):
        "Checks to determine the most profitable and most likely places to insert orders"
        "We need to determine the likelyhood of an order getting sold, if there are other orders"
        "Those orders would get priority at the same price"
        "If the optimal price is fully filled with orders, check the volume at tighter or bigger marigins"
        "tighter than  optimal might lower our profit, but it becomes much more likely to get sold"
        "broader is unlikely to get sold now, but results in priority if the market moves 1 a tick (either up or down)"
        "basically, the integral over the range that you would make money off of a trade"
object_ = myclass()

#object_.action()
#object_.req_limit_check()
instrument=1
order_volume=10
instrument_pos = np.array([20,-25])
BUY_SELL=0
#object_.pos_limit_check(instrument,instrument_pos[instrument],order_volume,BUY_SELL)

object_.combined_checks(instrument,instrument_pos[instrument],order_volume,BUY_SELL)
deltaT=3
vol=0.005
current_price=1500
Price_range=np.array([-5,-4,-3,-2,-1,0,1,2,3,4,5])
d1=(1/(vol*(deltaT)**0.5))*(np.log(current_price/(current_price+Price_range))+(vol**2/2)*deltaT)
print('d1',d1)

d2=d1-vol*deltaT**0.5
print('d2',d2)
Call_value=ss.norm.cdf(d1)*(current_price)-ss.norm.cdf(d2)*(current_price+Price_range)
#Call options are only good if the stock price rices above the current stock price
#if the value becomes less than 0, it's worthless.
#for US, our ask prices will determine the strike price. We must make sure that we sell stocks
#We must make money on all trades, and offering at current prices puts us at risk
Put_value = ss.norm.cdf(-d2)*(current_price+Price_range)-ss.norm.cdf(-d1)*(current_price)
print('call value',Call_value)
print('put value',Put_value)
#Additional_costs=strike_price*0.0001-Hedge_costs
