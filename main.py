#! /usr/bin/python3

from PyQt5.QtWidgets import QApplication, QMessageBox
import sys

app = QApplication(sys.argv)

if __name__ == '__main__':
    from view import MainWindow
    from model import SignalModel, Emotiv, Source
    from controller import ConsoleController, signalInit
    
    source = Source()
    signalNames = source.getAvailableSignals()
    signals = []
    for name in signalNames:
        signals.append(source.getSignalModel(name))

    window = MainWindow(signalNames)

    welcomeMessage = '''test welcome message\n'''
    consoleController = ConsoleController(window.consoleView, window,
                                          signals, welcomeMessage)
    signalInit(window.signalView, source, signals, window.signalButtons)

    window.show()
    sys.exit(app.exec_())
else:
    QMessageBox.about(None, "Error",
                      "This file is standalone program not a module")
    exit()
