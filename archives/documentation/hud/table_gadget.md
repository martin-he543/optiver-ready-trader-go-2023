Module ready_trader_go.hud.table_gadget
=======================================

Classes
-------

`BaseTableGadget(parent: Optional[PySide6.QtWidgets.QWidget] = None, flags: PySide6.QtCore.Qt.WindowFlags = PySide6.QtCore.Qt.WindowType.Widget)`
:   QWidget(self, parent: Union[PySide6.QtWidgets.QWidget, NoneType] = None, f: PySide6.QtCore.Qt.WindowFlags = Default(Qt.WindowFlags)) -> None
    
    Initialise a new instance of the class.

    ### Ancestors (in MRO)

    * PySide6.QtWidgets.QWidget
    * PySide6.QtCore.QObject
    * PySide6.QtGui.QPaintDevice
    * Shiboken.Object

    ### Descendants

    * ready_trader_go.hud.table_gadget.BasicPriceLadderGadget
    * ready_trader_go.hud.table_gadget.PerTeamTableGadget
    * ready_trader_go.hud.table_gadget.ProfitLossTableGadget

    ### Class variables

    `staticMetaObject`
    :

`BasicPriceLadderGadget(parent: Optional[PySide6.QtWidgets.QWidget] = None, flags: PySide6.QtCore.Qt.WindowFlags = PySide6.QtCore.Qt.WindowType.Widget)`
:   QWidget(self, parent: Union[PySide6.QtWidgets.QWidget, NoneType] = None, f: PySide6.QtCore.Qt.WindowFlags = Default(Qt.WindowFlags)) -> None
    
    Initialise a new instance of the class.

    ### Ancestors (in MRO)

    * ready_trader_go.hud.table_gadget.BaseTableGadget
    * PySide6.QtWidgets.QWidget
    * PySide6.QtCore.QObject
    * PySide6.QtGui.QPaintDevice
    * Shiboken.Object

    ### Class variables

    `staticMetaObject`
    :

    ### Methods

    `set_model(self, table_model: ready_trader_go.hud.table_model.BasicPriceLadderModel)`
    :   Set the data model for this price ladder.

    `update_best_ask_row(self, new_best_ask_row: int) ‑> None`
    :   Update the best ask row and ensure it is centered in the display.

`LadderEventFilter(ladder_gadget: PySide6.QtWidgets.QWidget)`
:   QObject(self, parent: Union[PySide6.QtCore.QObject, NoneType] = None) -> None
    
    Initialise a new instance of the class.

    ### Ancestors (in MRO)

    * PySide6.QtCore.QObject
    * Shiboken.Object

    ### Class variables

    `staticMetaObject`
    :

    ### Methods

    `eventFilter(self, source: PySide6.QtCore.QObject, event: PySide6.QtCore.QEvent) ‑> bool`
    :   Handle resize and filter out mouse events.

`PerTeamTableGadget(title: str, parent: Optional[PySide6.QtWidgets.QWidget] = None, flags: PySide6.QtCore.Qt.WindowFlags = PySide6.QtCore.Qt.WindowType.Widget)`
:   QWidget(self, parent: Union[PySide6.QtWidgets.QWidget, NoneType] = None, f: PySide6.QtCore.Qt.WindowFlags = Default(Qt.WindowFlags)) -> None
    
    Initialise a new instance of the class.

    ### Ancestors (in MRO)

    * ready_trader_go.hud.table_gadget.BaseTableGadget
    * PySide6.QtWidgets.QWidget
    * PySide6.QtCore.QObject
    * PySide6.QtGui.QPaintDevice
    * Shiboken.Object

    ### Class variables

    `staticMetaObject`
    :

    ### Methods

    `set_model(self, table_model: PySide6.QtCore.QAbstractTableModel) ‑> None`
    :   Set the table model used for this table gadget.

`ProfitLossTableGadget(parent: Optional[PySide6.QtWidgets.QWidget] = None, flags: PySide6.QtCore.Qt.WindowFlags = PySide6.QtCore.Qt.WindowType.Widget)`
:   QWidget(self, parent: Union[PySide6.QtWidgets.QWidget, NoneType] = None, f: PySide6.QtCore.Qt.WindowFlags = Default(Qt.WindowFlags)) -> None
    
    Initialise a new instance of the class.

    ### Ancestors (in MRO)

    * ready_trader_go.hud.table_gadget.BaseTableGadget
    * PySide6.QtWidgets.QWidget
    * PySide6.QtCore.QObject
    * PySide6.QtGui.QPaintDevice
    * Shiboken.Object

    ### Class variables

    `staticMetaObject`
    :

    ### Methods

    `set_model(self, table_model: ready_trader_go.hud.table_model.ProfitLossTableModel) ‑> None`
    :   Set the data model for this table gadget.