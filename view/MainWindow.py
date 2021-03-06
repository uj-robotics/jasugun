from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QAction, QMessageBox,
                             QMainWindow, QWidget, QScrollArea, QSplitter)
from PyQt5.QtCore import Qt
from .ConsoleView import ConsoleView
from .SignalButton import SignalButton
from .SignalView import SignalView

class MainWindow(QMainWindow):
    def __init__(self, signalNames):
        super(MainWindow, self).__init__()

        widget = QWidget()
        self.setCentralWidget(widget)

        self.consoleView = ConsoleView()
        self.signalView = SignalView()
        buttonsWidget = QWidget()

        scroll = QScrollArea()
        scroll.setWidget(self.signalView)
        scroll.setWidgetResizable(True)

        hboxSignalButtons = QHBoxLayout()
        self.signalButtons = self.createSignalButtons(signalNames,
                                                      hboxSignalButtons)
        buttonsWidget.setLayout(hboxSignalButtons)

        splitter = QSplitter(self)
        splitter.setOrientation(Qt.Vertical)
        splitter.addWidget(scroll)
        splitter.addWidget(self.consoleView)
        vbox = QVBoxLayout()
        vbox.addWidget(buttonsWidget)
        vbox.addWidget(splitter)
        

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

    def signalViewConnect(self, controller):
        self.signalView.connect(controller.model,
                                controller.button)

    def createActions(self):
        self.aboutAct = QAction("&About", self,
                                statusTip="learn what it is all about",
                                triggered=self.about)

    def createMenu(self):
        helpMenu = self.menuBar().addMenu("&Help")
        helpMenu.addAction(self.aboutAct)

    def about(self):
        QMessageBox.about(self, "About", "dummy about message")
