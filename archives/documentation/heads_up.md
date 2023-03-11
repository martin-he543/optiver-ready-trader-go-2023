Module ready_trader_go.heads_up
===============================

Classes
-------

`HeadsUpDisplayServer(host: str, port: int, match_events: ready_trader_go.match_events.MatchEvents, competitor_manager: ready_trader_go.competitor.CompetitorManager, controller: ready_trader_go.types.IController)`
:   Initialise a new instance of the HeadsUpDisplayServer class.

    ### Methods

    `start(self)`
    :   Start this Heads Up Display server.

`HudConnection(match_events: ready_trader_go.match_events.MatchEvents, competitor_manager: ready_trader_go.competitor.CompetitorManager, controller: ready_trader_go.types.IController)`
:   A stream-based network connection.
    
    Initialise a new instance of the HudConnection class.

    ### Ancestors (in MRO)

    * ready_trader_go.messages.Connection
    * asyncio.protocols.Protocol
    * asyncio.protocols.BaseProtocol
    * ready_trader_go.types.IExecutionConnection

    ### Methods

    `connection_lost(self, exc: Optional[Exception]) ‑> None`
    :   Called when the connection to the heads-up display is lost.

    `connection_made(self, transport: asyncio.transports.BaseTransport) ‑> None`
    :   Called when a connection from a heads-up display is established.

    `on_competitor_logged_in(self, name: str) ‑> None`
    :   Called when a competitor logs in.

    `on_login(self, name: str, secret: str) ‑> None`
    :   Called when the heads-up display logs in.

    `on_match_event(self, event: ready_trader_go.match_events.MatchEvent) ‑> None`
    :   Called when a match event occurs.

    `on_message(self, typ: int, data: bytes, start: int, length: int) ‑> None`
    :   Callback when a message is received from the Heads-Up Display.

    `send_error(self, client_order_id: int, error_message: bytes) ‑> None`
    :   Send an error message to the heads-up display.

    `send_order_filled(self, client_order_id: int, price: int, volume: int) ‑> None`
    :   Send an order filled message to the heads-up display.

    `send_order_status(self, client_order_id: int, fill_volume: int, remaining_volume: int, fees: int) ‑> None`
    :   Send an order status message to the heads-up display.