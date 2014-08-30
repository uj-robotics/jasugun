from PyQt5 import QtGui
from PyQt5.QtWidgets import QPlainTextEdit, QApplication
from PyQt5.QtCore import pyqtSignal

class ConsoleView(QPlainTextEdit):
    def __init__(self):
        super(ConsoleView, self).__init__()

        self.prompt = ''

        self.setWordWrapMode(QtGui.QTextOption.WrapAnywhere)
        self.setUndoRedoEnabled(False)
        self.document().setDefaultFont(QtGui.QFont("monospace", 10, QtGui.QFont.Normal))

    keyPressed = pyqtSignal(object)

    def getCursorPos(self):
        return self.textCursor().columnNumber()-len(self.prompt)

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
        QApplication.processEvents()

    def keyPressEvent(self, event):
        self.keyPressed.emit(event)

    def stdKeyPressEvent(self, event):
        super(ConsoleView, self).keyPressEvent(event)
