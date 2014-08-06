from PyQt5.QtWidgets import QPlainTextEdit, QApplication
from PyQt5 import QtGui, QtCore
from code import InteractiveConsole
import sys

class Console(QPlainTextEdit):
    def __init__(self, parent, locals=locals(), welcomeMessage=''):
        QPlainTextEdit.__init__(self)
        #TODO: capturing output of InteractiveConsole in that way
        #is pretty much overkill
        sys.stdout = sys.stderr = self

        self.parent = parent
        self.console = InteractiveConsole(locals=locals)
        self.ps1 = '>>> '
        self.ps2 = '... '
        self.prompt = self.ps1
        self.history = []
        self.historyIndex = 0

        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        self.setWordWrapMode(QtGui.QTextOption.WrapAnywhere)
        self.setUndoRedoEnabled(False)
        self.document().setDefaultFont(QtGui.QFont("monospace", 10, QtGui.QFont.Normal))

        self.write(welcomeMessage)
        self.write(self.prompt)

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

    def getCursorPos(self):
        return self.textCursor().columnNumber()-len(self.prompt)

    def setCursorPos(self, pos):
        self.moveCursor(QtGui.QTextCursor.StarOfLine)
        for i in range(len(self.prompt)+pos):
            self.moveCursor(QtGui.QTextCursor.Right)

    def setCursorPosBegin(self):
        self.moveCursor(QtGui.QTextCursor.StarOfLine)
        for i in range(len(self.prompt)):
            self.moveCursor(QtGui.QTextCursor.Right)

    def setCursorPosEnd(self, pos):
        self.moveCursor(QtGui.QTextCursor.EndOfLine)

    def getCommand(self):
        doc = self.document()
        line = str(doc.findBlockByLineNumber(doc.lineCount()-1).text())
        line = line.rstrip()
        line = line[len(self.prompt):]
        return line

    def setCommand(self, command):
        self.moveCursor(QtGui.QTextCursor.EndOfLine)
        self.moveCursor(QtGui.QTextCursor.StartOfLine, QtGui.QTextCursor.KeepAnchor)

        for i in range(len(self.prompt)):
            self.moveCursor(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor)

        self.textCursor().removeSelectedText()
        self.textCursor().insertText(command)
        self.moveCursor(QtGui.QTextCursor.EndOfLine)

    def write(self, data):
        self.appendPlainText(data.rstrip('\n'))
        QtCore.QCoreApplication.processEvents()

    def keyPressEvent(self, event):
        key = event.key()
        if key in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
            command = self.getCommand()
            self.addToHistory(command)
            requireMore = self.console.push(command)
            
            if requireMore:
                self.prompt = self.ps2
            else:
                self.prompt = self.ps1
            
            self.write(self.prompt)
            return
        elif key in (QtCore.Qt.Key_Left, QtCore.Qt.Key_Backspace):
            if self.getCursorPos() == 0:
                return
        elif key == QtCore.Qt.Key_Home:
            self.setCursorPosBegin()
            return
        elif key == QtCore.Qt.Key_End:
            self.setCursorPosEnd()
            return
        elif key == QtCore.Qt.Key_Up:
            self.setCommand(self.prevHistoryEntry())
            return
        elif key == QtCore.Qt.Key_Down:
            self.setCommand(self.nextHistoryEntry())
            return
        elif key == QtCore.Qt.Key_D and event.modifiers() == QtCore.Qt.ControlModifier:
            self.parent.close()
        super(Console, self).keyPressEvent(event)
