Module ready_trader_go.account
==============================

Classes
-------

`AccountFactory(etf_clamp: float, tick_size: float)`
:   A factory class for CompetitorAccounts.
    
    Initialise a new instance of the AccountFactory class.

    ### Methods

    `create(self) ‑> ready_trader_go.account.CompetitorAccount`
    :   Return a new instance of the CompetitorAccount class.

`CompetitorAccount(tick_size: float, etf_clamp: float)`
:   A competitors account.
    
    Initialise a new instance of the CompetitorAccount class.

    ### Methods

    `transact(self, instrument: ready_trader_go.types.Instrument, side: ready_trader_go.types.Side, price: float, volume: int, fee: int) ‑> None`
    :   Update this account with the specified transaction.

    `update(self, future_price: int, etf_price: int) ‑> None`
    :   Update this account using the specified prices.