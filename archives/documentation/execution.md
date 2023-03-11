Module ready_trader_go.execution
================================

Classes
-------

`ExecutionConnection(competitor_manager: ready_trader_go.competitor.CompetitorManager, frequency_limiter: ready_trader_go.limiter.FrequencyLimiter, controller: ready_trader_go.types.IController)`
:   A stream-based network connection.
    
    Initialise a new instance of the ExecutionChannel class.

    ### Ancestors (in MRO)

    * ready_trader_go.messages.Connection
    * asyncio.protocols.Protocol
    * asyncio.protocols.BaseProtocol
    * ready_trader_go.types.IExecutionConnection

    ### Methods

    `close(self)`
    :   Close the connection associated with this ExecutionChannel instance.

    `connection_lost(self, exc: Optional[Exception]) ‑> None`
    :   Called when the connection to the auto-trader is lost.

    `connection_made(self, transport: asyncio.transports.BaseTransport) ‑> None`
    :   Called when the connection is established.

    `on_login(self, name: str, secret: str) ‑> None`
    :   Called when a login message is received.

    `on_message(self, typ: int, data: bytes, start: int, length: int) ‑> None`
    :   Called when a message is received from the auto-trader.

`ExecutionServer(host: str, port: int, competitor_manager: ready_trader_go.competitor.CompetitorManager, limiter_factory: ready_trader_go.limiter.FrequencyLimiterFactory)`
:   A server for execution connections.
    
    Initialise a new instance of the ExecutionServer class.

    ### Methods

    `close(self)`
    :   Close the server without affecting existing connections.

    `start(self) ‑> None`
    :   Start the server.