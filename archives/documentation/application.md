Module ready_trader_go.application
==================================

Classes
-------

`Application(name: str, config_validator: Optional[Callable] = None)`
:   Standard application setup.
    
    Initialise a new instance of the Application class.

    ### Methods

    `on_signal(self, signum: int) ‑> None`
    :   Called when a signal is received.

    `run(self) ‑> None`
    :   Start the application's event loop.