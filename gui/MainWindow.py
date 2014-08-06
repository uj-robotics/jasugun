from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QAction, QMessageBox,
                             QMainWindow, QWidget)
from .Console import Console
from .SignalButton import SignalButton
from .SignalView import SignalView

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        widget = QWidget()
        self.setCentralWidget(widget)

        vbox = QVBoxLayout()
        hboxSignalButtons = QHBoxLayout()

        welcomeMessage = '''test welcome message\n'''

        console = Console(self, welcomeMessage=welcomeMessage)
        signalView = SignalView()

        widgetSignalButtons = QWidget()
        self.createSignalButtons(hboxSignalButtons)
        widgetSignalButtons.setLayout(hboxSignalButtons)

        vbox.addWidget(widgetSignalButtons)
        vbox.addWidget(signalView)
        vbox.addWidget(console)

        self.createActions()
        self.createMenu()

        widget.setLayout(vbox)
        self.setWindowTitle("kit")

    def createSignalButtons(self, buttonsPanel):
        pass

    def createActions(self):
        self.aboutAct = QAction("&About", self,
                                statusTip="learn what it is all about",
                                triggered=self.about)

    def createMenu(self):
        helpMenu = self.menuBar().addMenu("&Help")
        helpMenu.addAction(self.aboutAct)

    def about(self):
        QMessageBox.about(self, "About", "dummy about message")
