Module ready_trader_go.timer
============================

Classes
-------

`Timer(tick_interval: float, speed: float)`
:   A timer.
    
    Initialise a new instance of the timer class.

    ### Methods

    `advance(self) ‑> float`
    :   Advance the timer.

    `shutdown(self, now: float, reason: str) ‑> None`
    :   Shut down this timer.

    `start(self) ‑> None`
    :   Start this timer.