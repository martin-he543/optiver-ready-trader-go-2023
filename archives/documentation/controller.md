Module ready_trader_go.controller
=================================

Classes
-------

`Controller(market_open_delay: float, exec_server: ready_trader_go.execution.ExecutionServer, info_publisher: ready_trader_go.information.InformationPublisher, market_events_reader: ready_trader_go.market_events.MarketEventsReader, match_events_writer: ready_trader_go.match_events.MatchEventsWriter, score_board_writer: ready_trader_go.score_board.ScoreBoardWriter, market_timer: ready_trader_go.timer.Timer, tick_timer: ready_trader_go.timer.Timer)`
:   Controller for the Ready Trader Go matching engine.
    
    Initialise a new instance of the Controller class.

    ### Ancestors (in MRO)

    * ready_trader_go.types.IController

    ### Methods

    `cleanup(self) ‑> None`
    :   Ensure the controller shuts down gracefully

    `on_market_timer_ticked(self, timer: ready_trader_go.timer.Timer, now: float, _: int)`
    :   Called when it is time to process market events.

    `on_task_complete(self, task: Any) ‑> None`
    :   Called when a reader or writer task is complete

    `on_tick_timer_stopped(self, timer: ready_trader_go.timer.Timer, now: float) ‑> None`
    :   Shut down the match.

    `on_tick_timer_ticked(self, timer: ready_trader_go.timer.Timer, now: float, _: int) ‑> None`
    :   Called when it is time to send an order book update and trade ticks.

    `start(self) ‑> None`
    :   Start running the match.