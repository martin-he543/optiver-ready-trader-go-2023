Module ready_trader_go.competitor
=================================

Classes
-------

`Competitor(name: str, exec_channel: ready_trader_go.types.IExecutionConnection, etf_book: ready_trader_go.order_book.OrderBook, future_book: ready_trader_go.order_book.OrderBook, account: ready_trader_go.account.CompetitorAccount, match_events: ready_trader_go.match_events.MatchEvents, score_board: ready_trader_go.score_board.ScoreBoardWriter, position_limit: int, order_count_limit: int, active_volume_limit: int, tick_size: float, unhedged_lots_factory: ready_trader_go.unhedged_lots.UnhedgedLotsFactory, controller: ready_trader_go.types.IController)`
:   A competitor in the Ready Trader Go competition.
    
    Initialise a new instance of the Competitor class.

    ### Ancestors (in MRO)

    * ready_trader_go.types.ICompetitor
    * ready_trader_go.order_book.IOrderListener

    ### Methods

    `hard_breach(self, now: float, client_order_id: int, message: bytes) ‑> None`
    :   Handle a hard breach by this competitor.

    `on_connection_lost(self, now: float) ‑> None`
    :   Called when the connection to the matching engine is lost.

    `on_order_amended(self, now: float, order: ready_trader_go.order_book.Order, volume_removed: int) ‑> None`
    :   Called when an order is amended.

    `on_order_cancelled(self, now: float, order: ready_trader_go.order_book.Order, volume_removed: int) ‑> None`
    :   Called when an order is cancelled.

    `on_order_filled(self, now: float, order: ready_trader_go.order_book.Order, price: int, volume: int, fee: int) ‑> None`
    :   Called when an order is partially or completely filled.

    `on_timer_tick(self, now: float, future_price: int, etf_price: int) ‑> None`
    :   Called on each timer tick to update the auto-trader.

    `on_unhedged_lots_expiry(self)`
    :   Called when unhedged lots have been held for too long.

    `send_error(self, now: float, client_order_id: int, message: bytes) ‑> None`
    :   Send an error message to the auto-trader and shut down the match.

    `send_error_and_close(self, now: float, client_order_id: int, message: bytes) ‑> None`
    :   Send an error message to the auto-trader and shut down the match.

`CompetitorManager(limits_config: Dict[str, Any], traders_config: Dict[str, str], account_factory: ready_trader_go.account.AccountFactory, etf_book: ready_trader_go.order_book.OrderBook, future_book: ready_trader_go.order_book.OrderBook, match_events: ready_trader_go.match_events.MatchEvents, score_board_writer: ready_trader_go.score_board.ScoreBoardWriter, tick_size: float, timer: ready_trader_go.timer.Timer, unhedged_lots_factory: ready_trader_go.unhedged_lots.UnhedgedLotsFactory)`
:   A manager of competitors.
    
    Initialise a new instance of the CompetitorManager class.

    ### Methods

    `get_competitors(self) ‑> Iterable[ready_trader_go.competitor.Competitor]`
    :   Return an iterable of the competitors managed by this CompetitorManager.

    `login_competitor(self, name: str, secret: str, exec_channel: ready_trader_go.types.IExecutionConnection) ‑> Optional[ready_trader_go.types.ICompetitor]`
    :   Return the competitor object for the given name.

    `on_competitor_connect(self) ‑> None`
    :   Notify this competitor manager that a competitor has connected.

    `on_competitor_disconnect(self) ‑> None`
    :   Notify this competitor manager that a competitor has disconnected.

    `on_timer_started(self, _: ready_trader_go.timer.Timer, start_time: float) ‑> None`
    :   Called when the market opens.

    `on_timer_stopped(self, _: ready_trader_go.timer.Timer, end_time: float) ‑> None`
    :   Called when the market closes.

    `on_timer_tick(self, timer: ready_trader_go.timer.Timer, now: float, _: int) ‑> None`
    :   Called on each timer tick.