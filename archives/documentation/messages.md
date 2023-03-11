Module ready_trader_go.messages
===============================

Classes
-------

`Connection()`
:   A stream-based network connection.
    
    Initialize a new instance of the Connection class.

    ### Ancestors (in MRO)

    * asyncio.protocols.Protocol
    * asyncio.protocols.BaseProtocol

    ### Descendants

    * ready_trader_go.base_auto_trader.BaseAutoTrader
    * ready_trader_go.execution.ExecutionConnection
    * ready_trader_go.heads_up.HudConnection

    ### Methods

    `close(self)`
    :   Close the connection.

    `connection_lost(self, exc: Optional[Exception]) ‑> None`
    :   Callback when a connection has been lost.

    `connection_made(self, transport: asyncio.transports.BaseTransport) ‑> None`
    :   Callback when a connection has been established.

    `data_received(self, data: bytes) ‑> None`
    :   Called when data is received.

    `on_message(self, typ: int, data: bytes, start: int, length: int) ‑> None`
    :   Callback when an individual message has been received.

    `send_message(self, typ: int, data: bytes, length: int) ‑> None`
    :   Send a message.

`MessageType(value, names=None, *, module=None, qualname=None, type=None, start=1)`
:   An enumeration.

    ### Ancestors (in MRO)

    * enum.IntEnum
    * builtins.int
    * enum.Enum

    ### Class variables

    `AMEND_EVENT`
    :

    `AMEND_ORDER`
    :

    `CANCEL_EVENT`
    :

    `CANCEL_ORDER`
    :

    `ERROR`
    :

    `HEDGE_EVENT`
    :

    `HEDGE_FILLED`
    :

    `HEDGE_ORDER`
    :

    `INSERT_EVENT`
    :

    `INSERT_ORDER`
    :

    `LOGIN`
    :

    `LOGIN_EVENT`
    :

    `ORDER_BOOK_UPDATE`
    :

    `ORDER_FILLED`
    :

    `ORDER_STATUS`
    :

    `TRADE_EVENT`
    :

    `TRADE_TICKS`
    :

`Subscription()`
:   A packet-based network receiver.
    
    Initialise a new instance of the Receiver class.

    ### Ancestors (in MRO)

    * asyncio.protocols.DatagramProtocol
    * asyncio.protocols.BaseProtocol

    ### Descendants

    * ready_trader_go.base_auto_trader.BaseAutoTrader

    ### Methods

    `close(self)`
    :   Close the subscription.

    `connection_lost(self, exc: Optional[Exception]) ‑> None`
    :   Callback when the datagram receiver has lost its connection.

    `connection_made(self, transport: asyncio.transports.BaseTransport) ‑> None`
    :   Callback when the datagram receiver is established.

    `datagram_received(self, data: bytes, address: Tuple[str, int]) ‑> None`
    :   Callback when a datagram is received.

    `on_datagram(self, typ: int, data: bytes, start: int, length: int) ‑> None`
    :   Callback when a datagram is received.