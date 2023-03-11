Module ready_trader_go.base_auto_trader
=======================================

Classes
-------

`BaseAutoTrader(loop: asyncio.events.AbstractEventLoop, team_name: str, secret: str)`
:   Base class for an auto-trader.
    
    Initialise a new instance of the BaseTraderProtocol class.

    ### Ancestors (in MRO)

    * ready_trader_go.messages.Connection
    * asyncio.protocols.Protocol
    * ready_trader_go.messages.Subscription
    * asyncio.protocols.DatagramProtocol
    * asyncio.protocols.BaseProtocol

    ### Methods

    `connection_lost(self, exc: Optional[Exception]) ‑> None`
    :   Called when the connection is lost on the execution channel.

    `connection_made(self, transport: asyncio.transports.BaseTransport) ‑> None`
    :   Called twice, when the execution connection and the information channel are established.

    `on_datagram(self, typ: int, data: bytes, start: int, length: int) ‑> None`
    :   Called when an information message is received from the matching engine.

    `on_error_message(self, client_order_id: int, error_message: bytes)`
    :   Called when the matching engine detects an error.

    `on_hedge_filled_message(self, client_order_id: int, price: int, volume: int) ‑> None`
    :   Called when one of your hedge orders is filled, partially or fully.
        
        The price is the average price at which the order was (partially) filled,
        which may be better than the order's limit price. The volume is
        the number of lots filled at that price.

    `on_message(self, typ: int, data: bytes, start: int, length: int) ‑> None`
    :   Called when an execution message is received from the matching engine.

    `on_order_book_update_message(self, instrument: int, sequence_number: int, ask_prices: List[int], ask_volumes: List[int], bid_prices: List[int], bid_volumes: List[int]) ‑> None`
    :   Called periodically to report the status of the order book.
        
        The sequence number can be used to detect missed messages. The five
        best available ask (i.e. sell) and bid (i.e. buy) prices are reported
        along with the volume available at each of those price levels. If
        there are less than five prices on a side, then zeros will appear at
        the end of both the prices and volumes lists on that side so that
        there are always five entries in each list.

    `on_order_filled_message(self, client_order_id: int, price: int, volume: int) ‑> None`
    :   Called when one of your orders is filled, partially or fully.
        
        The price is the price at which the order was (partially) filled,
        which may be better than the order's limit price. The volume is
        the number of lots filled at that price.

    `on_order_status_message(self, client_order_id: int, fill_volume: int, remaining_volume: int, fees: int) ‑> None`
    :   Called when the status of one of your orders changes.
        
        The fill_volume is the total number of lots already traded,
        remaining_volume is the number of lots yet to be traded and fees is
        the total fees paid or received for this order.
        
        Remaining volume will be set to zero if the order is cancelled.

    `on_trade_ticks_message(self, instrument: int, sequence_number: int, ask_prices: List[int], ask_volumes: List[int], bid_prices: List[int], bid_volumes: List[int]) ‑> None`
    :   Called when there is trading activity on the market.
        
        The five best ask (i.e. sell) and bid (i.e. buy) prices at which there
        has been trading activity are reported along with the volume traded at
        each of those price levels. If there are less than five prices on a
        side, then zeros will appear at the end of both the prices and volumes
        lists on that side so that there are always five entries in each list.

    `send_amend_order(self, client_order_id: int, volume: int) ‑> None`
    :   Amend the specified order with an updated volume.
        
        The specified volume must be no greater than the original volume for
        the order. If the order has already completely filled or been
        cancelled this request has no effect and no order status message will
        be received.

    `send_cancel_order(self, client_order_id: int) ‑> None`
    :   Cancel the specified order.
        
        If the order has already completely filled or been cancelled this
        request has no effect and no order status message will be received.

    `send_hedge_order(self, client_order_id: int, side: ready_trader_go.types.Side, price: int, volume: int) ‑> None`
    :   Order lots in the future to hedge a position.

    `send_insert_order(self, client_order_id: int, side: ready_trader_go.types.Side, price: int, volume: int, lifespan: ready_trader_go.types.Lifespan) ‑> None`
    :   Insert a new order into the market.