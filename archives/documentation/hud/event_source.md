Module ready_trader_go.hud.event_source
=======================================

Classes
-------

`EventSource(etf_clamp: float, tick_size: float, parent: Optional[PySide6.QtCore.QObject] = None)`
:   QObject(self, parent: Union[PySide6.QtCore.QObject, NoneType] = None) -> None
    
    Initialise a new instance of the class.

    ### Ancestors (in MRO)

    * PySide6.QtCore.QObject
    * Shiboken.Object

    ### Descendants

    * ready_trader_go.hud.event_source.LiveEventSource
    * ready_trader_go.hud.event_source.RecordedEventSource

    ### Class variables

    `staticMetaObject`
    :

    ### Methods

    `event_source_error_occurred(...)`
    :

    `login_occurred(...)`
    :

    `match_over(...)`
    :

    `midpoint_price_changed(...)`
    :

    `order_amended(...)`
    :

    `order_book_changed(...)`
    :

    `order_cancelled(...)`
    :

    `order_inserted(...)`
    :

    `profit_loss_changed(...)`
    :

    `start(self) ‑> None`
    :   Start the event source.

    `trade_occurred(...)`
    :

`LiveEventSource(host: str, port: int, etf_clamp: float, tick_size: float, parent: Optional[PySide6.QtCore.QObject] = None)`
:   QObject(self, parent: Union[PySide6.QtCore.QObject, NoneType] = None) -> None
    
    Initialise a new instance of the class.

    ### Ancestors (in MRO)

    * ready_trader_go.hud.event_source.EventSource
    * PySide6.QtCore.QObject
    * Shiboken.Object

    ### Class variables

    `staticMetaObject`
    :

    ### Methods

    `on_amend_event_message(self, now: float, competitor_id: int, order_id: int, volume_delta: int) ‑> None`
    :   Callback when an amend event message is received.

    `on_cancel_event_message(self, now: float, competitor_id: int, order_id: int) ‑> None`
    :   Callback when an cancel event message is received.

    `on_connected(self) ‑> None`
    :   Callback when a connection to the exchange is established.

    `on_data_received(self) ‑> None`
    :   Callback when data is received from the exchange simulator.

    `on_disconnected(self) ‑> None`
    :   Callback when the connection to the exchange is lost.

    `on_error_message(self, client_order_id: int, error_message: bytes)`
    :   Callback when an error message is received.

    `on_error_occurred(self, error: PySide6.QtNetwork.QAbstractSocket.SocketError) ‑> None`
    :   Callback when there is a problem with the exchange connection.

    `on_hedge_event_message(self, now: float, competitor_id: int, side: int, instrument: int, volume: int, price: float) ‑> None`
    :   Callback when an hedge event message is received.

    `on_insert_event_message(self, now: float, competitor_id: int, order_id: int, instrument: int, side: int, volume: int, price: int, lifespan: int) ‑> None`
    :   Callback when an insert event message is received.

    `on_login_event_message(self, name: str, competitor_id: int) ‑> None`
    :   Callback when an login event message is received.

    `on_message(self, typ: int, data: bytes, length: int)`
    :   Process a message.

    `on_trade_event_message(self, now: float, competitor_id: int, order_id: int, side: int, instrument: int, volume: int, price: int, fee: int) ‑> None`
    :   Callback when an trade event message is received.

    `start(self) ‑> None`
    :   Start this live event source.

`RecordedEventSource(etf_clamp: float, tick_size: float, parent: Optional[PySide6.QtCore.QObject] = None)`
:   QObject(self, parent: Union[PySide6.QtCore.QObject, NoneType] = None) -> None
    
    Initialise a new instance of the class.

    ### Ancestors (in MRO)

    * ready_trader_go.hud.event_source.EventSource
    * PySide6.QtCore.QObject
    * Shiboken.Object

    ### Class variables

    `staticMetaObject`
    :

    ### Static methods

    `from_csv(file_object: <class 'TextIO'>, etf_clamp: float, tick_size: float, parent: Optional[PySide6.QtCore.QObject] = None)`
    :   Create a new RecordedEventSource instance from a CSV file.

    ### Methods

    `start(self) ‑> None`
    :   Start this recorded event source.