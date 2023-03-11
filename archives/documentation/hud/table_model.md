Module ready_trader_go.hud.table_model
======================================

Classes
-------

`ActiveOrderTableModel(team: str, parent: Optional[PySide6.QtCore.QObject] = None)`
:   QAbstractTableModel(self, parent: Union[PySide6.QtCore.QObject, NoneType] = None) -> None
    
    Initialise a new instance of the class.

    ### Ancestors (in MRO)

    * ready_trader_go.hud.table_model.BaseTableModel
    * PySide6.QtCore.QAbstractTableModel
    * PySide6.QtCore.QAbstractItemModel
    * PySide6.QtCore.QObject
    * Shiboken.Object

    ### Class variables

    `staticMetaObject`
    :

    ### Methods

    `on_order_amended(self, team: str, _: float, order_id: int, volume_delta: int) ‑> None`
    :   Callback when an order is amended.

    `on_order_cancelled(self, team: str, now: float, order_id: int) ‑> None`
    :   Callback when an order is cancelled.

    `on_order_inserted(self, team: str, now: float, order_id: int, instrument: ready_trader_go.types.Instrument, side: ready_trader_go.types.Side, volume: int, price: int, _: ready_trader_go.types.Lifespan) ‑> None`
    :   Callback when an order is inserted.

    `on_trade_occurred(self, team: str, now: float, order_id: int, side: ready_trader_go.types.Side, volume: int, price: int, fee: int) ‑> None`
    :   Callback when a trade occurs.

`BaseTableModel(parent: Optional[PySide6.QtCore.QObject] = None)`
:   QAbstractTableModel(self, parent: Union[PySide6.QtCore.QObject, NoneType] = None) -> None
    
    __init__(self, parent: Union[PySide6.QtCore.QObject, NoneType] = None) -> None
    
    Initialize self.  See help(type(self)) for accurate signature.

    ### Ancestors (in MRO)

    * PySide6.QtCore.QAbstractTableModel
    * PySide6.QtCore.QAbstractItemModel
    * PySide6.QtCore.QObject
    * Shiboken.Object

    ### Descendants

    * ready_trader_go.hud.table_model.ActiveOrderTableModel
    * ready_trader_go.hud.table_model.BasicPriceLadderModel
    * ready_trader_go.hud.table_model.ProfitLossTableModel
    * ready_trader_go.hud.table_model.TradeHistoryTableModel

    ### Class variables

    `staticMetaObject`
    :

    ### Methods

    `columnCount(self, parent: Optional[PySide6.QtCore.QModelIndex] = None) ‑> int`
    :   Return the number of columns.

    `data(self, index: PySide6.QtCore.QModelIndex, role: int = PySide6.QtCore.Qt.ItemDataRole.DisplayRole) ‑> Any`
    :   Return information about a specified table cell.

    `headerData(self, section: int, orientation: PySide6.QtCore.Qt.Orientation, role: int = PySide6.QtCore.Qt.ItemDataRole.DisplayRole) ‑> Any`
    :   Return information about a specified table header cell.

    `rowCount(self, parent: Optional[PySide6.QtCore.QModelIndex] = None) ‑> int`
    :   Return the number of rows.

`BasicPriceLadderModel(instrument: ready_trader_go.types.Instrument, tick_size: int, parent: Optional[PySide6.QtCore.QObject] = None)`
:   QAbstractTableModel(self, parent: Union[PySide6.QtCore.QObject, NoneType] = None) -> None
    
    Initialise a new instance of the class.

    ### Ancestors (in MRO)

    * ready_trader_go.hud.table_model.BaseTableModel
    * PySide6.QtCore.QAbstractTableModel
    * PySide6.QtCore.QAbstractItemModel
    * PySide6.QtCore.QObject
    * Shiboken.Object

    ### Descendants

    * ready_trader_go.hud.table_model.PriceLadderModel

    ### Class variables

    `staticMetaObject`
    :

    ### Methods

    `best_ask_row_changed(...) ‑> PySide6.QtCore.Signal`
    :

    `data(self, index: PySide6.QtCore.QModelIndex, role: int = PySide6.QtCore.Qt.ItemDataRole.DisplayRole) ‑> Any`
    :   Return the content of a table cell.

    `get_price(self, row: int) ‑> int`
    :   Return the price for a given row.

    `get_row(self, price: int) ‑> int`
    :   Return the row for a given price.

    `update_order_book(self, instrument: ready_trader_go.types.Instrument, _: float, ask_prices: List[int], ask_volumes: List[int], bid_prices: List[int], bid_volumes: List[int]) ‑> None`
    :   Callback when the order book changes.

`PriceLadderModel(instrument: ready_trader_go.types.Instrument, tick_size: int, parent: Optional[PySide6.QtCore.QObject] = None)`
:   QAbstractTableModel(self, parent: Union[PySide6.QtCore.QObject, NoneType] = None) -> None
    
    Initialise a new instance of the class.

    ### Ancestors (in MRO)

    * ready_trader_go.hud.table_model.BasicPriceLadderModel
    * ready_trader_go.hud.table_model.BaseTableModel
    * PySide6.QtCore.QAbstractTableModel
    * PySide6.QtCore.QAbstractItemModel
    * PySide6.QtCore.QObject
    * Shiboken.Object

    ### Class variables

    `TEAM_ASK_COLUMN`
    :

    `TEAM_BID_COLUMN`
    :

    `staticMetaObject`
    :

    ### Methods

    `best_ask_row_changed(...) ‑> PySide6.QtCore.Signal`
    :

    `set_competitor_model(self, team_volumes)`
    :

`ProfitLossTableModel(parent: Optional[PySide6.QtCore.QObject] = None)`
:   QAbstractTableModel(self, parent: Union[PySide6.QtCore.QObject, NoneType] = None) -> None
    
    Initialise a new instance of the class.

    ### Ancestors (in MRO)

    * ready_trader_go.hud.table_model.BaseTableModel
    * PySide6.QtCore.QAbstractTableModel
    * PySide6.QtCore.QAbstractItemModel
    * PySide6.QtCore.QObject
    * Shiboken.Object

    ### Class variables

    `ETF_POSITION_COLUMN`
    :

    `FUT_POSITION_COLUMN`
    :

    `NET_PROFIT_COLUMN`
    :

    `TEAM_NAME_COLUMN`
    :

    `staticMetaObject`
    :

    ### Methods

    `data(self, index: PySide6.QtCore.QModelIndex, role: int = PySide6.QtCore.Qt.ItemDataRole.DisplayRole) ‑> Any`
    :   Return information about the specified table cell.

    `on_login_occurred(self, team: str) ‑> None`
    :   Callback when a team logs in.

    `on_profit_loss_changed(self, team: str, _: float, profit: float, etf_position: int, fut_position: int, account_balance: float, total_fees: float) ‑> None`
    :   Callback when the profit for a team changes.

    `on_selection_changed(self, selected: PySide6.QtCore.QItemSelection, _: PySide6.QtCore.QItemSelection) ‑> None`
    :   Callback when the selected team changes.

    `team_changed(...)`
    :

`TeamLadderVolumes(team: str)`
:   A team's ask and bid volumes for each price level.
    
    Initialise a new instance of the class.

    ### Methods

    `clear_model(self) ‑> None`
    :   Clear the price ladder model.

    `on_order_amended(self, team: str, now: float, order_id: int, volume_delta: int) ‑> None`
    :   Callback when an order is amended.

    `on_order_cancelled(self, team: str, now: float, order_id: int) ‑> None`
    :   Callback when an order is cancelled.

    `on_order_inserted(self, team: str, now: float, order_id: int, instrument: ready_trader_go.types.Instrument, side: ready_trader_go.types.Side, volume: int, price: int, lifespan: ready_trader_go.types.Lifespan) ‑> None`
    :   Callback when an order is inserted.

    `on_trade_occurred(self, team: str, now: float, order_id: int, side: ready_trader_go.types.Side, volume: int, price: int, fee: int) ‑> None`
    :   Callback when a trade occurs.

    `set_model(self, model: ready_trader_go.hud.table_model.PriceLadderModel) ‑> None`
    :   Set the price ladder model.

`TradeHistoryTableModel(team: str, parent: Optional[PySide6.QtCore.QObject] = None)`
:   QAbstractTableModel(self, parent: Union[PySide6.QtCore.QObject, NoneType] = None) -> None
    
    Initialise a new instance of the class.

    ### Ancestors (in MRO)

    * ready_trader_go.hud.table_model.BaseTableModel
    * PySide6.QtCore.QAbstractTableModel
    * PySide6.QtCore.QAbstractItemModel
    * PySide6.QtCore.QObject
    * Shiboken.Object

    ### Class variables

    `staticMetaObject`
    :

    ### Methods

    `data(self, index: PySide6.QtCore.QModelIndex, role: int = PySide6.QtCore.Qt.ItemDataRole.DisplayRole) ‑> Any`
    :   Return information about the specified table cell.

    `on_trade_occurred(self, team: str, now: float, order_id: int, side: ready_trader_go.types.Side, volume: int, price: int, fee: int) ‑> None`
    :   Callback when a trade occurs.