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

LOT_SIZE = 10; TICK_SIZE_IN_CENTS = 100
POSITION_LIMIT = 100; MESSAGE_LIMIT = 50
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
        self.bids = set()
        self.asks = set()
        self.ask_id = self.ask_price = self.bid_id = self.bid_price = self.etf_position = 0
        self.recent_orders = np.zeros((50)); self.list_of_lists_2 = np.zeros((1, 5))
        self.future_position = 0; self.etf_position = 0
        self.book_of_orders = np.zeros((10, ))

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

    def on_order_book_update_message(self, instrument: int, sequence_number: int, ask_prices: List[int],
                                     ask_volumes: List[int], bid_prices: List[int], bid_volumes: List[int]) -> None:
        """Called periodically to report the status of an order book. The sequence number can be used to detect missed 
        or out-of-order messages. The five best available ask (i.e. sell) and bid (i.e. buy) prices are reported along 
        with the volume available at each of those price levels."""
        if self.etf_position != -self.future_position:
            net_position = self.etf_position + self.future_position                                                     # How many more ETFs we have than FUTURES
            if net_position < 0:                                                                                        # We have more ETFs than Futures to cover - HEDGE
                net_position = np.abs(net_position)
                BEST_BID_PRICE = self.list_of_lists_2[3]                                                                # HEDGE - Uses FUTURE_BP instead of MIN_BID_NEAREST_TICK
                if (current_time - self.recent_orders[0]) > 1:                                                          # CHECK if more than 50 messages in 1 second - STOP!
                    for i in range(0, net_position // 10):
                        self.send_hedge_order(next(self.order_ids), Side.ASK, BEST_BID_PRICE, LOT_SIZE)
                        self.future_position += LOT_SIZE
                        self.recent_orders= np.roll(self.recent_orders, -1)                                             # They see Dirk rolling...
                        self.recent_orders[-1] = current_time                                                           # Change the last value
                    if net_position % 10 != 0:
                        self.send_hedge_order(next(self.order_ids), Side.ASK, BEST_BID_PRICE, net_position % 10)
                        self.future_position += (net_position % 10)
                        self.recent_orders= np.roll(self.recent_orders, -1)                                             # They see Dirk rolling...
                        self.recent_orders[-1] = current_time                                                           # Change the last value
            if net_position > 0:
                BEST_ASK_PRICE = self.list_of_lists_2[1]                                                                # HEDGE - Uses FUTURE_AP instead of MIN_BID_NEAREST_TICK
                if (current_time - self.recent_orders[0]) > 1:                                                          # CHECK if more than 50 messages in 1 second - STOP!
                    for i in range(0, net_position // 10):
                        self.send_hedge_order(next(self.order_ids), Side.BID, BEST_ASK_PRICE, LOT_SIZE)                 # HEDGE - send an order
                        self.future_position -= LOT_SIZE
                        self.recent_orders= np.roll(self.recent_orders, -1)                                             # They see Dirk rolling...
                        self.recent_orders[-1] = current_time                                                           # Change the last value
                    if net_position % 10 != 0:
                        self.send_hedge_order(next(self.order_ids), Side.BID, BEST_ASK_PRICE, net_position % 10)
                        self.future_position -= (net_position % 10)
                        self.recent_orders= np.roll(self.recent_orders, -1)                                             # They see Dirk rolling...
                        self.recent_orders[-1] = current_time                                                           # Change the last value
        
        if instrument == Instrument.ETF:
            FUTURE_AP = self.list_of_lists_2[1]; FUTURE_AV = self.list_of_lists_2[2]                                    # Looks at best (low) FUTURE ask price
            FUTURE_BP = self.list_of_lists_2[3]; FUTURE_BV = self.list_of_lists_2[4]                                    # Looks at best FUTURE bid price
            ETF_AP = ask_prices[0]; ETF_AV = ask_volumes[0]
            ETF_BP = bid_prices[0]; ETF_BV = bid_volumes[0]     
            MAX_ORDERS_BUY_ETF = np.min([(POSITION_LIMIT - self.etf_position)//10, ETF_AV//10 + 1])
            MAX_ORDERS_SELL_ETF = np.min([(self.etf_position + POSITION_LIMIT)//10, ETF_BV//10 + 1])
            
            if (ETF_AP != 0) and (FUTURE_BP * 0.9998 - ETF_AP * 1.0002) > 0 and (self.etf_position < POSITION_LIMIT - 9):
                current_time = time.time() - start_time
                for i in range(MAX_ORDERS_BUY_ETF):
                    if (current_time - self.recent_orders[0]) > 1:                                                      # CHECK if more than 50 messages in 1 second - STOP!
                        self.bid_id = next(self.order_ids)
                        self.send_insert_order(self.bid_id, Side.BUY, ETF_AP, LOT_SIZE, Lifespan.FILL_AND_KILL)
                        self.bids.add(self.bid_id)
                        self.recent_orders= np.roll(self.recent_orders, -1)                                             # They see Dirk rolling...
                        self.recent_orders[-1] = current_time                                                           # Change the last value
                        # print(self.recent_orders)
                    
            if (ETF_BP * 0.9998 - FUTURE_AP * 1.0002) > 0 and (self.etf_position > -(POSITION_LIMIT - 9)):
                current_time = time.time() - start_time
                for i in range(MAX_ORDERS_SELL_ETF):
                    if (current_time - self.recent_orders[0]) > 1:                                                      # CHECK if more than 50 messages in 1 second - STOP!
                        self.ask_id = next(self.order_ids)
                        self.send_insert_order(self.ask_id, Side.SELL, ETF_BP, LOT_SIZE, Lifespan.FILL_AND_KILL)
                        self.asks.add(self.ask_id)
                        self.recent_orders= np.roll(self.recent_orders, -1)                                             # They see Dirk rolling...
                        self.recent_orders[-1] = current_time                                                           # Change the last value

        self.logger.info("received order book for instrument %d with sequence number %d", instrument, sequence_number)
        self.list_of_lists_2 = np.array([instrument, ask_prices[0], ask_volumes[0], bid_prices[0], bid_volumes[0]])                
        
        # Search FUTURE updates for Market-Maker Situation
        # if instrument == Instrument.FUTURE:            
        
        #     price_adjustment = - (self.etf_position // LOT_SIZE) * TICK_SIZE_IN_CENTS
            # new_bid_price = bid_prices[0] - 300 if bid_prices[0] != 0 else 0
            # new_ask_price = ask_prices[0] + 300 if ask_prices[0] != 0 else 0

        #     if self.bid_id != 0 and new_bid_price not in (self.bid_price, 0):
        #         self.send_cancel_order(self.bid_id)
        #         self.bid_id = 0
        #     if self.ask_id != 0 and new_ask_price not in (self.ask_price, 0):
        #         self.send_cancel_order(self.ask_id)
        #         self.ask_id = 0
        
        # 1. Every order is legal (quantity is correct => in last second > 50; ACTIVE ORDERS - the response time between us buying and market response: 0.125s)
        # 2. dont make more market than possible, ie dont offer to buy more ETF when already having too much ETF
                
            # if self.bid_id == 0 and new_bid_price != 0 and self.etf_position < POSITION_LIMIT:  # Are BUYING, position grows
            #     self.bid_id = next(self.order_ids)
            #     self.bid_price = new_bid_price
            #     self.send_insert_order(self.bid_id, Side.BUY, new_bid_price, LOT_SIZE, Lifespan.GOOD_FOR_DAY)
            #     self.bids.add(self.bid_id)
                # current_active_orders.append(now)
                # print(self.bids, ask_volumes, bid_volumes, ask_prices, bid_prices)

            # if self.ask_id == 0 and new_ask_price != 0 and self.etf_position > -POSITION_LIMIT:
            #     self.ask_id = next(self.order_ids)
            #     self.ask_price = new_ask_price
            #     self.send_insert_order(self.ask_id, Side.SELL, new_ask_price, LOT_SIZE, Lifespan.GOOD_FOR_DAY)
            #     self.asks.add(self.ask_id)
            
        # If update for ETF, won't to see if Abitrage for oppo, must check Future market info for checks
        # Otherwise, put some weighting function after, but keep in fundamental situation
        # self.list_of_lists.append([instrument, ask_prices[0], ask_volumes[0], bid_prices[0], bid_volumes[0]])
        # print(list_of_lists[-1])
        # print(self.list_of_lists_2)
        
        # Safety and Stability - Don't EXPLODE
        # if len(order_time) > 50:    order_time = order_time[-50:]
        # print(order_time)

    def on_order_filled_message(self, client_order_id: int, price: int, volume: int) -> None:
        """Called when one of your orders is filled, partially or fully. The price is the price at which the order was 
        (partially) filled, which may be better than the order's limit price. The volume is the number of lots filled at 
        that price."""
        self.logger.info("received order filled for order %d with price %d and volume %d", client_order_id, price, volume)
        current_time = time.time() - start_time
        if client_order_id in self.bids:
            self.etf_position += volume                                                                                 # ETF position increases by update position
            if (current_time - self.recent_orders[0]) > 1:                                                              # CHECK if more than 50 messages in 1 second - STOP!
                self.send_hedge_order(next(self.order_ids), Side.ASK, MIN_BID_NEAREST_TICK, volume)
                self.future_position -= volume
                self.recent_orders= np.roll(self.recent_orders, -1)                                                     # They see Dirk rolling...
                self.recent_orders[-1] = current_time                                                                   # Change the last value
            
        elif client_order_id in self.asks:
            self.etf_position -= volume
            if (current_time - self.recent_orders[0]) > 1:                                                              # CHECK if more than 50 messages in 1 second - STOP!
                self.send_hedge_order(next(self.order_ids), Side.BID, MAX_ASK_NEAREST_TICK, volume)
                self.future_position += volume
                self.recent_orders= np.roll(self.recent_orders, -1)                                                     # They see Dirk rolling...
                self.recent_orders[-1] = current_time                                                                   # Change the last value
    
    def on_order_status_message(self, client_order_id: int, fill_volume: int, remaining_volume: int, fees: int) -> None:
        """Called when the status of one of your orders changes. The fill_volume is the number of lots already traded, 
        remaining_volume is the number of lots yet to be traded and fees is the total fees for this order. Remember that
        you pay fees for being a market taker, but you receive fees for being a market maker, so fees can be negative.
        If an order is cancelled its remaining volume will be zero."""
        
        self.logger.info("received order status for order %d with fill volume %d remaining %d and fees %d",
                         client_order_id, fill_volume, remaining_volume, fees)
        if remaining_volume == 0:
            if client_order_id == self.bid_id:
                self.bid_id = 0
            elif client_order_id == self.ask_id:
                self.ask_id = 0
            self.bids.discard(client_order_id)
            self.asks.discard(client_order_id)

    def on_trade_ticks_message(self, instrument: int, sequence_number: int, ask_prices: List[int],
                               ask_volumes: List[int], bid_prices: List[int], bid_volumes: List[int]) -> None:
        """Called periodically when there is trading activity on the market. The five best ask (i.e. sell) and bid (i.e. 
        buy) prices at which there has been trading activity are reported along with the aggregated volume traded at each
        of those price levels. If there are less than five prices on a side, then zeros will appear at the end of both 
        the prices and volumes arrays."""
        self.logger.info("received trade ticks for instrument %d with sequence number %d", instrument, sequence_number)
