Module ready_trader_go.demo_client
==================================

Classes
-------

`DemoClient(name: str, secret: str)`
:   A Ready Trader Go exchange client for Jupyter Notebooks.
    
    Initialise a new instance of the class.

    ### Static methods

    `display_error(message: str) ‑> None`
    :   Display an error message.

    ### Methods

    `connect(self, host: str = '127.0.0.1', port: int = 12345) ‑> None`
    :   Connect to the exchange simulator.
        
        The arguments specify the network address of the exchange simulator.

    `get_order(self, order_id: int) ‑> ready_trader_go.demo_client.Order`
    :   Return the specified order.
        
        Raises a KeyError if the order does not exist.

    `send_amend_order(self, order_id: int, new_volume: int) ‑> None`
    :   Amend the specified order.
        
        The new volume must be less than or equal to the original volume.

    `send_cancel_order(self, order_id: int) ‑> None`
    :   Cancel the specified order.

    `send_insert_order(self, order_id: int, side: ready_trader_go.types.Side, price_in_cents: int, volume: int, lifespan: ready_trader_go.types.Lifespan) ‑> ready_trader_go.demo_client.Order`
    :   Insert a new order and return an Order instance.
        
        The order_id should be a unique order identifier, the side should be
        either Side.BUY or Side.SELL, the price should be the limit price for
        the order, the volume should be the number of lots to trade and
        lifespan should be either Lifespan.GOOD_FOR_DAY or
        Lifespan.FILL_AND_KILL.

    `update_orders(self) ‑> None`
    :   Process messages from the exchange and update orders.

`Fill(price: int, volume: int)`
:   Initialise a new instance of the class.

`Order(order_id: int, side: ready_trader_go.types.Side, price_in_cents: int, volume: int, lifespan: ready_trader_go.types.Lifespan)`
:   Initialise a new instance of the class.