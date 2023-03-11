Module ready_trader_go.limiter
==============================

Classes
-------

`FrequencyLimiter(interval: float, limit: int)`
:   Limit the frequency of events in a specified time interval.
    
    Initialise a new instance of the FrequencyLimiter class.

    ### Methods

    `check_event(self, now: float) ‑> bool`
    :   Return True if the new event breaches the limit, False otherwise.
        
        This method should be called with a monotonically increasing sequence
        of times.

`FrequencyLimiterFactory(interval: float, limit: int)`
:   A factory class for FrequencyLimiters.
    
    Initialise a new instance of the FrequencyLimiterFactory class.

    ### Methods

    `create(self) ‑> ready_trader_go.limiter.FrequencyLimiter`
    :   Return a new FrequencyLimiter instance.