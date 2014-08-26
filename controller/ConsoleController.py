from PyQt5.QtCore import pyqtSlot, Qt, QObject
from code import InteractiveConsole
import sys

class ConsoleController(QObject):
    def __init__(self, consoleView, app, signals, welcomeMessage=''):
        super(ConsoleController, self).__init__()
        #TODO: capturing output of InteractiveConsole in that way
        #is pretty much overkill
        #sys.stdout = sys.stderr = consoleView

        self.consoleView = consoleView
        self.consoleView.keyPressed.connect(self.keyPressEvent)

        self.namespace = self.populateNamespace(signals)
        self.console = InteractiveConsole(locals=self.namespace)

        self.app = app
        self.ps1 = '>>> '
        self.ps2 = '... '
        self.consoleView.prompt = self.ps1
        self.history = []
        self.historyIndex = 0

        self.consoleView.write(welcomeMessage)
        self.consoleView.write(self.consoleView.prompt)

    def populateNamespace(self, signals):
        namespace = dict()
        for signal in signals:
            name = signal.getName()
            namespace.update({name : signal})
        return namespace

    def addToHistory(self, entry):
        if entry:
            if self.history and self.history[-1] == entry:
                return
            self.history.append(entry)
            self.historyIndex = len(self.history)

    def nextHistoryEntry(self):
        if self.history:
            historyLength = len(self.history)
            self.historyIndex = min(historyLength, self.historyIndex+1)
            if self.historyIndex < historyLength:
                return self.history[self.historyIndex]
        else:
            return ''

    def prevHistoryEntry(self):
        if self.history:
            self.historyIndex = max(0, self.historyIndex-1)
            return self.history[self.historyIndex]
        else:
            return ''

    @pyqtSlot(object)
    def keyPressEvent(self, event):
        key = event.key()
        if key in (Qt.Key_Enter, Qt.Key_Return):
            command = self.consoleView.getCommand()
            self.addToHistory(command)
            requireMore = self.console.push(command)
            
            if requireMore:
                self.consoleView.prompt = self.ps2
            else:
                self.consoleView.prompt = self.ps1
            
            self.consoleView.write(self.consoleView.prompt)
            return
        elif key in (Qt.Key_Left, Qt.Key_Backspace):
            if self.consoleView.getCursorPos() == 0:
                return
        elif key == Qt.Key_Home:
            self.consoleView.setCursorPosBegin()
            return
        elif key == Qt.Key_End:
            self.consoleView.setCursorPosEnd()
            return
        elif key == Qt.Key_Up:
            self.consoleView.setCommand(self.prevHistoryEntry())
            return
        elif key == Qt.Key_Down:
            self.consoleView.setCommand(self.nextHistoryEntry())
            return
        elif key == Qt.Key_D and event.modifiers() == Qt.ControlModifier:
            self.app.close()
        self.consoleView.stdKeyPressEvent(event)
