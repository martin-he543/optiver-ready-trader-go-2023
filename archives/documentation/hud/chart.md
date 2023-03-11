Module ready_trader_go.hud.chart
================================

Classes
-------

`BaseChartGadget(parent: Optional[PySide6.QtWidgets.QWidget] = None, flags: PySide6.QtCore.Qt.WindowFlags = PySide6.QtCore.Qt.WindowType.Widget)`
:   QWidget(self, parent: Union[PySide6.QtWidgets.QWidget, NoneType] = None, f: PySide6.QtCore.Qt.WindowFlags = Default(Qt.WindowFlags)) -> None
    
    Initialise a new instance of the class.

    ### Ancestors (in MRO)

    * PySide6.QtWidgets.QWidget
    * PySide6.QtCore.QObject
    * PySide6.QtGui.QPaintDevice
    * Shiboken.Object

    ### Descendants

    * ready_trader_go.hud.chart.MidpointChartGadget
    * ready_trader_go.hud.chart.ProfitLossChartGadget

    ### Class variables

    `staticMetaObject`
    :

`MidpointChartGadget(parent: Optional[PySide6.QtWidgets.QWidget] = None)`
:   QWidget(self, parent: Union[PySide6.QtWidgets.QWidget, NoneType] = None, f: PySide6.QtCore.Qt.WindowFlags = Default(Qt.WindowFlags)) -> None
    
    Initialise a new instance of the class.

    ### Ancestors (in MRO)

    * ready_trader_go.hud.chart.BaseChartGadget
    * PySide6.QtWidgets.QWidget
    * PySide6.QtCore.QObject
    * PySide6.QtGui.QPaintDevice
    * Shiboken.Object

    ### Class variables

    `staticMetaObject`
    :

    ### Methods

    `on_midpoint_price_changed(self, instrument: ready_trader_go.types.Instrument, time: float, mid_price: float) ‑> None`
    :   Callback when the midpoint price of an instrument changes.

`ProfitLossChartGadget(parent: Optional[PySide6.QtWidgets.QWidget] = None)`
:   QWidget(self, parent: Union[PySide6.QtWidgets.QWidget, NoneType] = None, f: PySide6.QtCore.Qt.WindowFlags = Default(Qt.WindowFlags)) -> None
    
    Initialise a new instance of the class.

    ### Ancestors (in MRO)

    * ready_trader_go.hud.chart.BaseChartGadget
    * PySide6.QtWidgets.QWidget
    * PySide6.QtCore.QObject
    * PySide6.QtGui.QPaintDevice
    * Shiboken.Object

    ### Class variables

    `staticMetaObject`
    :

    ### Methods

    `on_login_occurred(self, team: str) ‑> None`
    :   Callback when a team logs in to the exchange.

    `on_profit_loss_changed(self, team: str, time: float, profit: float, etf_position: int, account_balance: float, total_fees: float) ‑> None`
    :   Callback when the profit of a team changes.