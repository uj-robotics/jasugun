#! /usr/bin/python3

from PyQt5.QtWidgets import QApplication, QMessageBox
import sys

if __name__ == '__main__':
    from view import MainWindow
    from model import SignalModel, Emotiv, Source
    from controller import ConsoleController, SignalController
    
    with Emotiv() as source:
        app = QApplication(sys.argv)
        signalNames = source.getAvailableSignals()
        window = MainWindow(signalNames)

        source.rememberToNotify(window.signalView.newData)

        signalCtrls = []
        for button in window.signalButtons:
            model = source.getSignalModel(button.getName())
            controller = SignalController(model, button)
            signalCtrls.append(controller)
            window.signalViewConnect(controller)

        welcomeMessage = '''test welcome message\n'''
        consoleController = ConsoleController(window.consoleView, window,
                                              signalCtrls, welcomeMessage)

        window.show()
        sys.exit(app.exec_())
else:
    QMessageBox.about(None, "Error",
                      "This file is standalone program not a module")
    exit()
