Module ready_trader_go.information
==================================

Classes
-------

`InformationPublisher(loop: asyncio.events.AbstractEventLoop, publisher_factory: ready_trader_go.pubsub.PublisherFactory, order_books: Iterable[ready_trader_go.order_book.OrderBook], timer: ready_trader_go.timer.Timer)`
:   A publisher of exchange information.
    
    Initialize a new instance of the InformationChannel class.

    ### Ancestors (in MRO)

    * asyncio.protocols.DatagramProtocol
    * asyncio.protocols.BaseProtocol

    ### Methods

    `connection_made(self, transport: asyncio.transports.WriteTransport) ‑> None`
    :   Called when the datagram endpoint is created.

    `on_timer_tick(self, timer: ready_trader_go.timer.Timer, now: float, tick_number: int) ‑> None`
    :   Called each time the timer ticks.

    `on_trade(self, book: ready_trader_go.order_book.OrderBook) ‑> None`
    :   Called when a trade occurs in one of the order books.

    `start(self) ‑> None`
    :   Start this publisher.