Module ready_trader_go.market_events
====================================

Classes
-------

`MarketEvent(time: float, instrument: ready_trader_go.types.Instrument, operation: ready_trader_go.market_events.MarketEventOperation, order_id: int, side: Optional[ready_trader_go.types.Side], volume: int, price: int, lifespan: Optional[ready_trader_go.types.Lifespan])`
:   A market event.
    
    Initialise a new instance of the MarketEvent class.

    ### Instance variables

    `instrument`
    :   Return an attribute of instance, which is of type owner.

    `lifespan`
    :   Return an attribute of instance, which is of type owner.

    `operation`
    :   Return an attribute of instance, which is of type owner.

    `order_id`
    :   Return an attribute of instance, which is of type owner.

    `price`
    :   Return an attribute of instance, which is of type owner.

    `side`
    :   Return an attribute of instance, which is of type owner.

    `time`
    :   Return an attribute of instance, which is of type owner.

    `volume`
    :   Return an attribute of instance, which is of type owner.

`MarketEventOperation(value, names=None, *, module=None, qualname=None, type=None, start=1)`
:   An enumeration.

    ### Ancestors (in MRO)

    * enum.IntEnum
    * builtins.int
    * enum.Enum

    ### Class variables

    `AMEND`
    :

    `Amend`
    :

    `CANCEL`
    :

    `Cancel`
    :

    `INSERT`
    :

    `Insert`
    :

`MarketEventsReader(filename: str, loop: asyncio.events.AbstractEventLoop, future_book: ready_trader_go.order_book.OrderBook, etf_book: ready_trader_go.order_book.OrderBook, match_events: ready_trader_go.match_events.MatchEvents)`
:   A processor of market events read from a file.
    
    Initialise a new instance of the MarketEvents class.

    ### Ancestors (in MRO)

    * ready_trader_go.order_book.IOrderListener

    ### Methods

    `on_reader_done(self, num_events: int) ‑> None`
    :   Called when the market data reader thread is done.

    `process_market_events(self, elapsed_time: float) ‑> None`
    :   Process market events from the queue.

    `reader(self, market_data: <class 'TextIO'>) ‑> None`
    :   Read the market data file and place order events in the queue.

    `start(self)`
    :   Start the market events reader thread