# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 16:52:34 2023

@author: smell
"""
"""ONLY HEDGE IF OUR POS >=10, this stops 1 vol trades from eating our message limit"""

# Copyright 2021 Optiver Asia Pacific Pty. Ltd.
#
# This file is part of Ready Trader Go.
#
#     Ready Trader Go is free software: you can redistribute it and/or
#     modify it under the terms of the GNU Affero General Public License
#     as published by the Free Software Foundation, either version 3 of
#     the License, or (at your option) any later version.
#
#     Ready Trader Go is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public
#     License along with Ready Trader Go.  If not, see
#     <https://www.gnu.org/licenses/>.
import asyncio
import itertools
from typing import List
from ready_trader_go import BaseAutoTrader, Instrument, Lifespan, MAXIMUM_ASK, MINIMUM_BID, Side
import numpy as np; import time
import scipy.stats as ss

LOT_SIZE = 200; TICK_SIZE_IN_CENTS = 100
POSITION_LIMIT = 100; MESSAGE_LIMIT = 50
MARKET_CAP = 100
MIN_BID_NEAREST_TICK = (MINIMUM_BID + TICK_SIZE_IN_CENTS) // TICK_SIZE_IN_CENTS * TICK_SIZE_IN_CENTS
MAX_ASK_NEAREST_TICK = MAXIMUM_ASK // TICK_SIZE_IN_CENTS * TICK_SIZE_IN_CENTS
start_time = time.time()

class AutoTrader(BaseAutoTrader):
    """Example Auto-trader. When it starts this auto-trader places ten-lot bid and ask orders at the current best-bid and 
    best-ask prices respectively. Thereafter, if it has a long position (it has bought more lots than it has sold) it 
    reduces its bid and ask prices. Conversely, if it has a short position (it has sold more lots than it has bought) 
    then it increases its bid and ask prices."""
    def __init__(self, loop: asyncio.AbstractEventLoop, team_name: str, secret: str):
        """Initialise a new instance of the AutoTrader class."""
        super().__init__(loop, team_name, secret)
        self.order_ids = itertools.count(1)
        self.bids = set(); self.asks = set()
        self.ask_id = self.ask_price = self.bid_id = self.bid_price = self.etf_position = 0
        self.recent_orders = np.zeros((50)) 
        self.market_info = np.zeros((1, 5))
        self.future_position = 0 
        self.etf_position = 0
        self.NET_POSITION = 0
        self.market_prices = np.array([])
        self.TOTAL_ASK_VOLUME = 0
        self.TOTAL_BID_VOLUME = 0
        self.time_cap=0
        self.debug_prints=True
        self.market_book=np.zeros((2,2,2,5))
        # ORDER BOOK: [ASK_ID, ASK_PRICE, ASK_VOLUME], [BID_ID, BID_PRICE, BID_VOLUME]
        self.active_ask_orders = np.zeros((3, 200),dtype=int) 
        self.active_bid_orders = np.zeros((3, 200),dtype=int)
        #self.active_total_orders=np.sum(se)
        self.active_hedge_orders= np.zeros((2,3,200),dtype=int)
        # Discussion, do we track time? older orders could be more valuable, long term optimisation problem
    def market_orders_update(self,current_market_book,ask_prices,ask_volumes,bid_prices,bid_volumes):
        #current_market_prices=np.zeros((2,2,2,5))
        current_market_book[0,0,:] = ask_prices
        current_market_book[0,1,:] = ask_volumes
        current_market_book[1,0,:] = bid_prices
        current_market_book[1,1,:] = bid_volumes
        return current_market_book[:,:,:]
    
    def price_estimate(self,best_future_ask_price,best_future_ask_volume,best_future_bid_price,best_future_bid_volume):
        spread=best_future_ask_price-best_future_bid_price
        weight=best_future_ask_volume/(best_future_bid_volume+best_future_ask_volume)
        price_prediction=best_future_bid_price+spread*weight
        return price_prediction
    
    def fair_prices(self,current_price,vol,BestFA,BestFB):
        vol2=vol/100
        vol=vol/current_price
        print('BestFA',BestFA)
        print('BestFB',BestFB)
        deltaT=2
        Strike_price_call=BestFA+np.array([1,2,3,4,5,6])*100
        Strike_price_put=BestFB-np.array([1,2,3,4,5,6])*100
        d1=(1/(vol*(deltaT)**0.5))*(np.log(current_price/(Strike_price_call))+(vol**2/2)*deltaT)
        d2=d1-vol*deltaT**0.5
        Call_value= ss.norm.cdf(d1)*(current_price)-ss.norm.cdf(d2)*(Strike_price_call)
        d1_put =(1/(vol*(deltaT)**0.5))*(np.log(current_price/(Strike_price_put))+(vol**2/2)*deltaT)
        d2_put = d1_put-vol*deltaT**0.5
        Put_value = ss.norm.cdf(-d2_put)*(Strike_price_put)-ss.norm.cdf(-d1_put)*(current_price)
        print('Call_value',Call_value)
        print('Put_value',Put_value)
        'We can make markets if our profits on sales are greater than our losses on trade'
        Call_profit=-Call_value+Strike_price_call*1.0001-BestFA*1.0002
        Put_profit=-Put_value+BestFB*0.9998-Strike_price_put*0.9999
        print('Call_profit',Call_profit)
        print('Put_profit',Put_profit)
        
        Call_ex_profit=Call_profit*(1-ss.norm.cdf(np.array([0,1,2,3,4,5])/vol2))
        Put_ex_profit=Put_profit*(1-ss.norm.cdf(np.array([0,1,2,3,4,5])/vol2))
        print('Call_ex_profit',Call_ex_profit)
        print('Put_ex_profit',Put_ex_profit)
        Profitable_ask = np.where(Call_ex_profit>0)[0]
        Profitable_bid = np.where(Put_ex_profit>0)[0]
        min_price_ask = Profitable_ask[0]*100+100+BestFA
        max_price_bid = Profitable_bid[0]*(-100)-100+BestFB
        Best_price_ask = np.argmax(Call_ex_profit)*100+100+BestFA
        Best_price_bid = np.argmax(Put_ex_profit)*(-100)-100+BestFB
        print('min_price_ask',min_price_ask)
        print('max_price_bid',max_price_bid)
        print('Best_price_ask',Best_price_ask)
        print('Best_price_bid',Best_price_bid)
        return Best_price_ask,Best_price_bid,min_price_ask,max_price_bid
    
    def arbitrage_check(self):
        if self.market_book[1,1,0,0]*0.9998- self.market_book[0,0,0,0]*1.0002>0:
            print('arbitrage found, buying ETF, Selling Future')
            arb_volume = np.minimum(self.market_book[1,1,1,0],self.market_book[0,0,1,0])
            if arb_volume>0:
                print('arbitrage found, buying ETF, Selling Future')
                arb_price = self.market_book[1,1,0,0]
                BUY_SELL=1
                return BUY_SELL,arb_price,arb_volume
        elif -self.market_book[1,0,0,0]*1.0002+self.market_book[0,1,0,0]*0.9998>0:
            print('arbitrage found, selling ETF, buying Future')
            arb_volume = np.minimum(self.market_book[1,0,1,0],self.market_book[0,1,1,0])
            if arb_volume>0:
                print('arbitrage found, selling ETF, buying Future')
                arb_price = self.market_book[1,0,0,0]
                BUY_SELL=0
                return BUY_SELL,arb_price,arb_volume
        else:
            return 3,0,0
    def req_limit_check(self):
        """Determines if we can place an order by checking if placing an order would breach the rolling order cap.
        returns True if we can place an order without breaching, False if not and a relevant time update.
        Special Scenario: if we somehow went back in time, it tells us by how much and prevents us from ordering
        would need to stop us from ordering for a second, now never lets us place a new order"""
        current_time=time.time()
        Delta_time_orders = current_time - self.recent_orders[0]
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
    def place_order_etf(self, offer, volume,BUY_SELL):
        print('Placing ETF order',BUY_SELL)
        print('volume',volume)
        print('price',offer)
        if BUY_SELL == 0:
            self.bid_id = next(self.order_ids)
            self.send_insert_order(self.bid_id, Side.BUY, int(offer), int(volume), Lifespan.FILL_AND_KILL)
            self.bids.add(self.bid_id)
            self.recent_orders = np.roll(self.recent_orders, -1)                                            # They see Dirk rolling...
            self.recent_orders[-1] = time.time()  
        elif BUY_SELL == 1:
            self.ask_id = next(self.order_ids)
            self.send_insert_order(self.ask_id, Side.SELL, int(offer), int(volume), Lifespan.FILL_AND_KILL)
            self.asks.add(self.ask_id)
            self.recent_orders = np.roll(self.recent_orders, -1)                                            # They hatin'...
            self.recent_orders[-1] = time.time()
    """
    def place_order_future(self, offer, volume,BUY_SELL):
        if BUY_SELL==0:
            self.send_hedge_order(next(self.order_ids), Side.BID, MAX_ASK_NEAREST_TICK, volume)
            self.future_position += volume
            self.recent_orders = np.roll(self.recent_orders, -1)                                                    # They see Dirk rolling...
            self.recent_orders[-1] = current_time   
    """
    def max_volume(self,volume,instrument_pos,BUY_SELL):
        if BUY_SELL==0:
            if volume>LOT_SIZE:
                volume=LOT_SIZE
            if volume +instrument_pos>POSITION_LIMIT:
                volume=POSITION_LIMIT-instrument_pos
        elif BUY_SELL==1:
            if volume>LOT_SIZE:
                volume=LOT_SIZE
            if instrument_pos-volume<-POSITION_LIMIT:
                volume=instrument_pos+POSITION_LIMIT
        return volume
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
        if order_volume>LOT_SIZE:
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
                        if Net_pos_lim_factor>MARKET_CAP:
                            print('We should have been kicked from the servers at this point')
                            return False
                elif BUY_SELL==1: #we SELL ETF
                    if self.NET_POSITION<0:
                        "Adittional limit NEEDED, NET position can not go below -100, so we need an extra correction limit"
                        Net_pos_lim_factor=np.abs(self.NET_POSITION)
                        if self.debug_prints==True:
                            print('limiting maximum ETF SELL orders by:',Net_pos_lim_factor)
                        if Net_pos_lim_factor>MARKET_CAP:
                            print('We should have been kicked from the servers at this point')
                            return False
        
        if BUY_SELL == 0: #this means we are buying
            "ORDER INSERTING CHECK"
            if instrument==0:#checks if we're buying from futures AKA HEDGING
                if instrument_pos + order_volume > MARKET_CAP:
                    if self.debug_prints== True:
                        print('A new BUY Hedge order would breach the maximum amount of Futures we can hold')
                        print('Returning False')
                    return False
                elif instrument_pos+order_volume <= MARKET_CAP:
                    print('Hedge BUY order would not breach the futures cap,returning True')
                    return True
            elif instrument==1: #Checks if we're buying from ETF markets
                if instrument_pos + np.sum(self.active_bid_orders[2,:]) + order_volume +Net_pos_lim_factor> MARKET_CAP:
                    if self.debug_prints==True:
                        if instrument_pos + order_volume <= MARKET_CAP:
                            print('Whilst a new BUY order would not put us over the position limit directly, we have orders pending that could put us over the cap after, Returning FALSE')
                            
                        elif instrument_pos + order_volume + np.sum(self.active_bid_orders[2,:]) <= MARKET_CAP:
                            print('The NET market position combined with active orders push us over our tolerance in the market.')
                        else:
                            print('New BUY order could push us over our position limit in ETF')
                            print('Returning False')
                    return False
                elif instrument_pos + np.sum(self.active_bid_orders[2,:]) + order_volume <= MARKET_CAP:
                    if self.debug_prints==True:
                        print('The new BUY order at this volume would not breach our market cap,returning True')
                    return True
                    
        elif BUY_SELL==1:#this would mean we are selling futures
            if instrument==0:
                if instrument_pos - order_volume < -MARKET_CAP:
                    "We check to make sure a new, selling, Hedge ORDER would not cause us to breach our limit in the futures"
                    if self.debug_prints==True:
                        print('New Hedge SELL order would Breach our market cap on the negative side, returning False')
                    return False
                elif instrument_pos - order_volume >-MARKET_CAP:
                    if self.debug_prints==True:
                        print('New Hedge SELL order would not breach our market cap on the negative side, returning True')
                    return True
            elif instrument==1:#selling etf market
                if instrument_pos-order_volume-np.sum(self.active_ask_orders[2,:]) <-(MARKET_CAP+Net_pos_lim_factor):
                    if self.debug_prints==True:
                        if instrument_pos - order_volume < -(MARKET_CAP+Net_pos_lim_factor):
                            print('Whilst a new SELL order would not put us over the position limit directly, we have orders pending that could put us over the cap after, Returning FALSE')
                        elif instrument_pos - order_volume -np.sum(self.active_ask_orders[2,:]) >= -(MARKET_CAP):
                            print('The NET market position combined with the active orders push us over our tolerance in the market.')
                        else:
                            print('New SELL order could push us over our position limit in ETF')
                        print('Returning False')
                    return False
                elif instrument_pos-np.sum(self.active_ask_orders[2,:])-order_volume >=-MARKET_CAP:
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
    
    def on_error_message(self, client_order_id: int, error_message: bytes) -> None:
        """Called when the exchange detects an error.If the error pertains to a particular order, then the 
        client_order_id will identify that order, otherwise the client_order_id will be zero."""
        self.logger.warning("error with order %d: %s", client_order_id, error_message.decode())
        if client_order_id != 0 and (client_order_id in self.bids or client_order_id in self.asks):
            self.on_order_status_message(client_order_id, 0, 0, 0)

    def on_hedge_filled_message(self, client_order_id: int, price: int, volume: int) -> None:
        """Called when one of your hedge orders is filled. The price is the average price at which the order was 
        (partially) filled, which may be better than the order's limit price. The volume is the number of lots filled at 
        that price."""
        self.logger.info("received hedge filled for order %d with average price %d and volume %d", client_order_id, price, volume)
        "remove hedges from active orders"
        
    def on_order_book_update_message(self, instrument: int, sequence_number: int, ask_prices: List[int],
                                     ask_volumes: List[int], bid_prices: List[int], bid_volumes: List[int]) -> None:
        """Called periodically to report the status of an order book. The sequence number can be used to detect missed 
        or out-of-order messages. The five best available ask (i.e. sell) and bid (i.e. buy) prices are reported along 
        with the volume available at each of those price levels."""
        
        """We update our books properly"""
        self.market_book[instrument,:,:,:]= self.market_orders_update(self.market_book[instrument,:,:,:],ask_prices,ask_volumes,bid_prices,bid_volumes)
        print('future_position: ', self.future_position, 'etf_position: ', self.etf_position)
        if self.etf_position != -self.future_position:
            #self.market_book[instrument,:,:,:]= self.market_orders_update(self.market_book[instrument,:,:,:],ask_prices,ask_volumes,bid_prices,bid_volumes)
            print('hedge checking remainder')
            
        if instrument == Instrument.ETF:
            buy_sell,Price,Volume = self.arbitrage_check()
            if buy_sell==0:
                Volume=self.max_volume(Volume,self.etf_position,buy_sell)
                if Volume>0:
                    combined_check,time_wasted = self.combined_checks(instrument,self.etf_position,Volume,buy_sell)
                    print(time_wasted)
                    if combined_check==True:
                        self.place_order_etf(Price,Volume,buy_sell)
            if buy_sell==1:
                Volume=self.max_volume(Volume,self.etf_position,buy_sell)
                if Volume>0:
                    combined_check,time_wasted = self.combined_checks(instrument,self.etf_position,Volume,buy_sell)
                    print(time_wasted)
                    if combined_check==True:
                        self.place_order_etf(Price,Volume,buy_sell)
            #update the books
            
        if instrument == Instrument.FUTURE:     
            # Search FUTURE updates for Market-Maker Situation
            print('future')
            market_price=self.price_estimate(self.market_book[0,0,0,0],self.market_book[0,0,1,0],self.market_book[0,1,0,0],self.market_book[0,1,1,0])
            print('market_price: ', market_price)
            self.market_prices=np.append(self.market_prices,market_price)
            vol=np.nanstd(self.market_prices)
            print('vol: ', vol)
            if vol!=np.nan and vol!=0 and market_price!=np.nan:
                if(self.market_book[0,0,0,0]!=0 and self.market_book[0,1,0,0]!=0):
                    Best_ask_price,Best_bid_price,min_bid_price,max_ask_price=self.fair_prices(market_price,vol,self.market_book[0,0,0,0],self.market_book[0,1,0,0])
                    locations_bid=np.argwhere(self.active_bid_orders[:,1]>0)
                    if len(locations_bid)>0:
                        min_bid=np.minimum(self.active_bid_orders[locations_bid,1])
                        min_bid_id = np.argwhere(self.active_bid_orders[min_bid])
                        print('min_bid_id: ', min_bid_id)
                        if min_bid_price>min_bid or min_bid < Best_bid_price:
                            self.send_cancel_order(self,min_bid_id)
                            self.etf_position = self.etf_position - self.active_bid_orders[min_bid_id,2]
                    locations_ask=np.argwhere(self.active_ask_orders[:,1]>0)
                    if len(locations_ask)>0:
                        max_ask=np.maximum(self.active_ask_orders[locations_ask,1])
                        max_ask_id = np.argwhere(self.active_ask_orders[max_ask])
                        if max_ask_price<max_ask or max_ask < max_ask_price:
                            self.send_cancel_order(self,max_ask_id)
                            self.etf_position = self.etf_position + self.active_ask_orders[max_ask_id,2]
                    volume=self.max_volume(LOT_SIZE,self.etf_position,0)
                    combined_check,time_wasted = self.combined_checks(1,self.etf_position,volume,0)
                    if combined_check==True:
                        self.bid_id = next(self.order_ids); self.bid_price = Best_bid_price
                        self.send_insert_order(self.bid_id, Side.BUY, int(Best_bid_price), int(volume), Lifespan.GOOD_FOR_DAY)
                        self.bids.add(self.bid_id)
                        self.active_bid_orders = np.roll(self.active_bid_orders, -1, axis=1)
                        self.active_bid_orders[:,-1] = [self.bid_id, Best_bid_price, volume]
                        self.recent_orders = np.roll(self.recent_orders, -1)                                                        # They see Dirk rolling...
                        current_time = time.time()
                        self.recent_orders[-1] = current_time
                    combined_check2,time_wasted2 = self.combined_checks(1,self.etf_position,volume,1)
                    if combined_check2==True:
                        self.ask_id = next(self.order_ids); self.ask_price = Best_ask_price
                        self.send_insert_order(self.ask_id, Side.SELL, int(Best_ask_price), int(volume), Lifespan.GOOD_FOR_DAY)
                        self.asks.add(self.ask_id)
                        self.active_ask_orders = np.roll(self.active_ask_orders, -1, axis=1)
                        self.active_ask_orders[:,-1] = [self.ask_id, Best_ask_price, volume]
                        self.recent_orders = np.roll(self.recent_orders, -1)                                                        # They see Dirk rolling...
                        current_time = time.time()
                        self.recent_orders[-1] = current_time
    def on_order_filled_message(self, client_order_id: int, price: int, volume: int) -> None:
        """Called when one of your orders is filled, partially or fully. The price is the price at which the order was 
        (partially) filled, which may be better than the order's limit price. The volume is the number of lots filled at 
        that price."""
        self.logger.info("received order filled for order %d with price %d and volume %d", client_order_id, price, volume)
        print('POSITIONS:',self.etf_position, self.future_position)
        
        if client_order_id in self.bids:
            self.etf_position += volume                                                                                 # ETF position increases by update position            
            
            print("ALIVE STILL",client_order_id)
            #print(self.active_bid_orders[0,:])
            #print(self.active_bid_orders[1,:])
            #print(np.argwhere(self.active_bid_orders[0,:] == client_order_id)[0,0])
            if len(np.argwhere(self.active_bid_orders[0,:] == client_order_id)) > 0:
                INDEX = np.argwhere(self.active_bid_orders[0,:] == client_order_id)[0,0]
                print("INDEX", INDEX)
                self.active_bid_orders[2, INDEX] -= volume
                if self.active_bid_orders[2, INDEX] == 0:                                                                   # CHECK if this order has been filled -> CLEAR.
                    print('pre slicing orders',self.active_bid_orders[0,-5:])
                    self.active_bid_orders= np.delete(self.active_bid_orders,INDEX,axis=1)
                    print('post deleting arr',self.active_bid_orders[:,-5:])
                    self.active_bid_orders=np.insert(self.active_bid_orders,0,np.array([0,0,0]),axis=1)
                    #self.active_bid_orders[:,1:INDEX+1] = self.active_ask_orders[:,0:INDEX]
                    print('post slicing orders',self.active_bid_orders[0,-5:])
            
            current_time = time.time() - start_time
            if (current_time - self.recent_orders[0]) > 1 and self.future_position > -90:                                                              # CHECK if more than 50 messages in 1 second - STOP!
                self.send_hedge_order(next(self.order_ids), Side.ASK, MIN_BID_NEAREST_TICK, volume)
                self.future_position -= volume
                self.recent_orders = np.roll(self.recent_orders, -1)                                                    # They see Dirk rolling...
                self.recent_orders[-1] = current_time                                                                   # Change the last value
            
        elif client_order_id in self.asks:
            self.etf_position -= volume
            
            print("ALIVE STILL",client_order_id)
            #print(self.active_bid_orders[0,:])
            #print(self.active_bid_orders[1,:])
            #print(np.argwhere(self.active_bid_orders[0,:] == client_order_id)[0,0])
            if len(np.argwhere(self.active_ask_orders[0,:] == client_order_id)) > 0:
                INDEX = np.argwhere(self.active_ask_orders[0,:] == client_order_id)[0,0]
                print("INDEX", INDEX)
                self.active_ask_orders[2, INDEX] -= volume
                if self.active_ask_orders[2, INDEX] == 0:                                                                   # CHECK if this order has been filled -> CLEAR.
                    print('pre slicing orders',self.active_ask_orders[0,-5:])
                    self.active_ask_orders= np.delete(self.active_ask_orders,INDEX,axis=1)
                    print('post deleting arr',self.active_ask_orders[:,-5:])
                    self.active_ask_orders=np.insert(self.active_ask_orders,0,np.array([0,0,0]),axis=1)
                    #self.active_bid_orders[:,1:INDEX+1] = self.active_ask_orders[:,0:INDEX]
                    print('post slicing orders',self.active_ask_orders[0,-5:])
            
            current_time = time.time() - start_time
            if (current_time - self.recent_orders[0]) > 1 and self.future_position < 90:                                                              # CHECK if more than 50 messages in 1 second - STOP!
                self.send_hedge_order(next(self.order_ids), Side.BID, MAX_ASK_NEAREST_TICK, volume)
                self.future_position += volume
                self.recent_orders = np.roll(self.recent_orders, -1)                                                    # They see Dirk rolling...
                self.recent_orders[-1] = current_time                                                                   # Change the last value
    
    def on_order_status_message(self, client_order_id: int, fill_volume: int, remaining_volume: int, fees: int) -> None:
        """Called when the status of one of your orders changes. The fill_volume is the number of lots already traded, 
        remaining_volume is the number of lots yet to be traded and fees is the total fees for this order. Remember that
        you pay fees for being a market taker, but you receive fees for being a market maker, so fees can be negative.
        If an order is cancelled its remaining volume will be zero."""
        
        self.logger.info("received order status for order %d with fill volume %d remaining %d and fees %d",
                         client_order_id, fill_volume, remaining_volume, fees)
        #check where this id is in our book and adjust the volume accordingly
        
        #remove the order from our book if the id=0
        if remaining_volume == 0:
            if client_order_id == self.bid_id:
                self.bid_id = 0
            elif client_order_id == self.ask_id:
                self.ask_id = 0
            self.bids.discard(client_order_id)
            self.asks.discard(client_order_id)
        #basically change our volume based on the change in the market

    def on_trade_ticks_message(self, instrument: int, sequence_number: int, ask_prices: List[int],
                               ask_volumes: List[int], bid_prices: List[int], bid_volumes: List[int]) -> None:
        """Called periodically when there is trading activity on the market. The five best ask (i.e. sell) and bid (i.e. 
        buy) prices at which there has been trading activity are reported along  with the aggregated volume traded at each
        of those price levels. If there are less than five prices on a side, then zeros will appear at the end of both 
        the prices and volumes arrays."""
        self.market_book[instrument,:,:,:]= self.market_orders_update(self.market_book[instrument,:,:,:],ask_prices,ask_volumes,bid_prices,bid_volumes)
        market_price=self.price_estimate(self.market_book[0,0,0,0],self.market_book[0,0,1,0],self.market_book[0,1,0,0],self.market_book[0,1,1,0])
        """CHECK IF THERE ARE ORDERS THAT NEED TO BE PLACED. AMENDED OR UPDATED"""
        #schould we make out trades here instead of on update?
        #YES, MARKET UPDATE GOES HERE AS WELL, WE SHOULD ABSOLUTELY CHECK AND TRACK EVERYTHING HERE WTF
        self.logger.info("received trade ticks for instrument %d with sequence number %d", instrument, sequence_number)