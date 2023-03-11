Module ready_trader_go.match_events
===================================

Classes
-------

`MatchEvent(time: float, competitor: str, operation: ready_trader_go.match_events.MatchEventOperation, order_id: int, instrument: Optional[ready_trader_go.types.Instrument], side: Optional[ready_trader_go.types.Side], volume: int, price: Union[int, float, None], lifespan: Optional[ready_trader_go.types.Lifespan], fee: Optional[int])`
:   

    ### Class variables

    `OPERATION_NAMES`
    :

    ### Instance variables

    `competitor`
    :   Return an attribute of instance, which is of type owner.

    `fee`
    :   Return an attribute of instance, which is of type owner.

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

`MatchEventOperation(value, names=None, *, module=None, qualname=None, type=None, start=1)`
:   An enumeration.

    ### Ancestors (in MRO)

    * enum.IntEnum
    * builtins.int
    * enum.Enum

    ### Class variables

    `AMEND`
    :

    `CANCEL`
    :

    `HEDGE`
    :

    `INSERT`
    :

    `TRADE`
    :

`MatchEvents()`
:   A clearing house of match events.
    
    Initialise a new instance of the MatchEvents class.

    ### Methods

    `amend(self, now: float, name: str, order_id: int, diff: int) ‑> None`
    :   Create a new amend event.

    `cancel(self, now: float, name: str, order_id: int, diff: int) ‑> None`
    :   Create a new cancel event.

    `fill(self, now: float, name: str, order_id: int, instrument: ready_trader_go.types.Instrument, side: ready_trader_go.types.Side, price: int, diff: int, fee: int) ‑> None`
    :   Create a new fill event.

    `hedge(self, now: float, name: str, order_id: int, instrument: ready_trader_go.types.Instrument, side: ready_trader_go.types.Side, price: float, volume: int) ‑> None`
    :   Create a new fill event.

    `insert(self, now: float, name: str, order_id: int, instrument: ready_trader_go.types.Instrument, side: ready_trader_go.types.Side, volume: int, price: int, lifespan: ready_trader_go.types.Lifespan) ‑> None`
    :   Create a new insert event.

`MatchEventsWriter(match_events: ready_trader_go.match_events.MatchEvents, filename: str, loop: asyncio.events.AbstractEventLoop)`
:   A processor of match events that it writes to a file.
    
    Initialise a new instance of the MatchEvents class.

    ### Methods

    `finish(self) ‑> None`
    :   Indicate the the series of events is complete.

    `on_writer_done(self, num_events: int) ‑> None`
    :   Called when the match event writer thread is done.

    `start(self)`
    :   Start the match events writer thread

    `writer(self, match_events_file: <class 'TextIO'>) ‑> None`
    :   Fetch match events from a queue and write them to a file