Module ready_trader_go.unhedged_lots
====================================

Classes
-------

`UnhedgedLots(callback: Callable[[], Any])`
:   Keep track of unhedged lots and call a callback if unhedged lots are held for too long.
    
    Initialise a new instance of the UnhedgedLots class.

    ### Instance variables

    `unhedged_lot_count: int`
    :   Return the number of unhedged lots.

    ### Methods

    `apply_position_delta(self, delta: int) ‑> None`
    :   Apply the given position delta to this unhedged lots instance.

`UnhedgedLotsFactory()`
:   A factory class for UnhedgedLots instances.
    
    Initialise a new instance of the UnhedgedLotsFactory class.

    ### Methods

    `create(self, callback: Callable[[], Any]) ‑> ready_trader_go.unhedged_lots.UnhedgedLots`
    :   Return a new instance of the UnhedgedLots class.