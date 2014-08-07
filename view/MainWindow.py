from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QAction, QMessageBox,
                             QMainWindow, QWidget)
from .ConsoleView import ConsoleView
from .SignalButton import SignalButton
from .SignalView import SignalView

class MainWindow(QMainWindow):
    def __init__(self, signalNames):
        super(MainWindow, self).__init__()

        widget = QWidget()
        self.setCentralWidget(widget)

        self.consoleView = ConsoleView()
        signalView = SignalView()
        signalButtons = QWidget()

        hboxSignalButtons = QHBoxLayout()
        self.buttons = self.createSignalButtons(signalNames, hboxSignalButtons)
        signalButtons.setLayout(hboxSignalButtons)

        vbox = QVBoxLayout()
        vbox.addWidget(signalButtons)
        vbox.addWidget(signalView)
        vbox.addWidget(self.consoleView)

        self.createActions()
        self.createMenu()

        widget.setLayout(vbox)
        self.setWindowTitle("kit")

    def createSignalButtons(self, signalNames, buttonsPanel):
        buttons = []
        for name in signalNames:
            button = SignalButton(name)
            buttonsPanel.addWidget(button)
            buttons.append(button)
        return buttons

    def createActions(self):
        self.aboutAct = QAction("&About", self,
                                statusTip="learn what it is all about",
                                triggered=self.about)

    def createMenu(self):
        helpMenu = self.menuBar().addMenu("&Help")
        helpMenu.addAction(self.aboutAct)

    def about(self):
        QMessageBox.about(self, "About", "dummy about message")
