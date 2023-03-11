Module ready_trader_go.hud.main_window.main_window
==================================================

Classes
-------

`MainWindow(icon: PySide6.QtGui.QIcon, event_source: ready_trader_go.hud.event_source.EventSource, parent: Optional[PySide6.QtWidgets.QWidget] = None)`
:   QMainWindow(self, parent: Union[PySide6.QtWidgets.QWidget, NoneType] = None, flags: PySide6.QtCore.Qt.WindowFlags = Default(Qt.WindowFlags)) -> None
    
    Initialise a new instance of the class.

    ### Ancestors (in MRO)

    * ready_trader_go.hud.main_window.ui_main_window.Ui_main_window
    * PySide6.QtWidgets.QMainWindow
    * PySide6.QtWidgets.QWidget
    * PySide6.QtCore.QObject
    * PySide6.QtGui.QPaintDevice
    * Shiboken.Object

    ### Class variables

    `staticMetaObject`
    :

    ### Methods

    `show(self) ‑> None`
    :   Show the window.

`SubWindowEventFilter(callback: Callable, parent: Optional[PySide6.QtCore.QObject] = None)`
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
    :   Capture close events and call a callback.