Module ready_trader_go.score_board
==================================

Classes
-------

`ScoreBoardWriter(filename: str, loop: asyncio.events.AbstractEventLoop)`
:   A processor of score records that it writes to a file.
    
    Initialise a new instance of the MatchEvents class.

    ### Methods

    `breach(self, now: float, name: str, account: ready_trader_go.account.CompetitorAccount, etf_price: Optional[int], future_price: Optional[int]) ‑> None`
    :   Create a new disconnect event.

    `disconnect(self, now: float, name: str, account: ready_trader_go.account.CompetitorAccount, etf_price: Optional[int], future_price: Optional[int]) ‑> None`
    :   Create a new disconnect event.

    `finish(self) ‑> None`
    :   Indicate the the series of events is complete.

    `on_writer_done(self, num_events: int) ‑> None`
    :   Called when the match event writer thread is done.

    `start(self)`
    :   Start the score board writer thread

    `tick(self, now: float, name: str, account: ready_trader_go.account.CompetitorAccount, etf_price: Optional[int], future_price: Optional[int], status: Optional[str] = None) ‑> None`
    :   Create a new tick event

    `writer(self, score_records_file: <class 'TextIO'>) ‑> None`
    :   Fetch score records from a queue and write them to a file

`ScoreRecord(time: float, team: str, operation: str, buy_volume: int, sell_volume: int, etf_position: int, future_position, etf_price: Optional[int], future_price: Optional[int], total_fees: int, balance: int, profit_loss: int, status: Optional[str] = None)`
:   

    ### Instance variables

    `balance`
    :   Return an attribute of instance, which is of type owner.

    `buy_volume`
    :   Return an attribute of instance, which is of type owner.

    `etf_position`
    :   Return an attribute of instance, which is of type owner.

    `etf_price`
    :   Return an attribute of instance, which is of type owner.

    `future_position`
    :   Return an attribute of instance, which is of type owner.

    `future_price`
    :   Return an attribute of instance, which is of type owner.

    `operation`
    :   Return an attribute of instance, which is of type owner.

    `profit_loss`
    :   Return an attribute of instance, which is of type owner.

    `sell_volume`
    :   Return an attribute of instance, which is of type owner.

    `status`
    :   Return an attribute of instance, which is of type owner.

    `team`
    :   Return an attribute of instance, which is of type owner.

    `time`
    :   Return an attribute of instance, which is of type owner.

    `total_fees`
    :   Return an attribute of instance, which is of type owner.