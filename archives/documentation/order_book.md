Module ready_trader_go.order_book
=================================

Classes
-------

`IOrderListener()`
:   

    ### Descendants

    * ready_trader_go.competitor.Competitor
    * ready_trader_go.market_events.MarketEventsReader

    ### Methods

    `on_order_amended(self, now: float, order, volume_removed: int) ‑> None`
    :   Called when the order is amended.

    `on_order_cancelled(self, now: float, order, volume_removed: int) ‑> None`
    :   Called when the order is cancelled.

    `on_order_filled(self, now: float, order, price: int, volume: int, fee: int) ‑> None`
    :   Called when the order is partially or completely filled.

    `on_order_placed(self, now: float, order) ‑> None`
    :   Called when a good-for-day order is placed in the order book.

`Order(client_order_id: int, instrument: ready_trader_go.types.Instrument, lifespan: ready_trader_go.types.Lifespan, side: ready_trader_go.types.Side, price: int, volume: int, listener: Optional[ready_trader_go.order_book.IOrderListener] = None)`
:   A request to buy or sell at a given price.
    
    Initialise a new instance of the Order class.

    ### Instance variables

    `client_order_id`
    :   Return an attribute of instance, which is of type owner.

    `instrument`
    :   Return an attribute of instance, which is of type owner.

    `lifespan`
    :   Return an attribute of instance, which is of type owner.

    `listener`
    :   Return an attribute of instance, which is of type owner.

    `price`
    :   Return an attribute of instance, which is of type owner.

    `remaining_volume`
    :   Return an attribute of instance, which is of type owner.

    `side`
    :   Return an attribute of instance, which is of type owner.

    `total_fees`
    :   Return an attribute of instance, which is of type owner.

    `volume`
    :   Return an attribute of instance, which is of type owner.

`OrderBook(instrument: ready_trader_go.types.Instrument, maker_fee: float, taker_fee: float)`
:   A collection of orders arranged by the price-time priority principle.
    
    Initialise a new instance of the OrderBook class.

    ### Methods

    `amend(self, now: float, order: ready_trader_go.order_book.Order, new_volume: int) ‑> None`
    :   Amend an order in this order book by decreasing its volume.

    `cancel(self, now: float, order: ready_trader_go.order_book.Order) ‑> None`
    :   Cancel an order in this order book.

    `insert(self, now: float, order: ready_trader_go.order_book.Order) ‑> None`
    :   Insert a new order into this order book.

    `last_traded_price(self) ‑> Optional[int]`
    :   Return the last traded price.

    `midpoint_price(self) ‑> Optional[float]`
    :   Return the midpoint price.

    `place(self, now: float, order: ready_trader_go.order_book.Order) ‑> None`
    :   Place an order that does not match any existing order in this order book.

    `remove_volume_from_level(self, price: int, volume: int, side: ready_trader_go.types.Side) ‑> None`
    :

    `top_levels(self, ask_prices: List[int], ask_volumes: List[int], bid_prices: List[int], bid_volumes: List[int]) ‑> None`
    :   Populate the supplied lists with the top levels for this book.

    `trade_ask(self, now: float, order: ready_trader_go.order_book.Order) ‑> None`
    :   Check to see if any existing bid orders match the specified ask order.

    `trade_bid(self, now: float, order: ready_trader_go.order_book.Order) ‑> None`
    :   Check to see if any existing ask orders match the specified bid order.

    `trade_level(self, now: float, order: ready_trader_go.order_book.Order, best_price: int) ‑> None`
    :   Match the specified order with existing orders at the given level.

    `trade_ticks(self, ask_prices: List[int], ask_volumes: List[int], bid_prices: List[int], bid_volumes: List[int]) ‑> bool`
    :   Return True and populate the lists if there have been trades.

    `try_trade(self, side: ready_trader_go.types.Side, limit_price: int, volume: int) ‑> Tuple[int, int]`
    :   Return the volume that would trade and the average price per lot for
        the requested trade without changing the order book.