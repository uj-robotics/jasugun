from PyQt5.QtWidgets import QPlainTextEdit
from code import InteractiveConsole
import threading

class Console(QPlainTextEdit, InteractiveConsole):
    def __init__(self, parent, locals=locals(), welcomeMessage=''):
        super(QPlainTextEdit, self).__init__()
        super(InteractiveConsole, self).__init__(locals=locals)

        self.parent = parent
        self.history = []
        self.historyIndex = 0
        self.prompt = ''
        self.queue = threading.Queue()

        self.setWordWrapMode(QtGui.QTextOption.WrapAnywhere)
        self.setUndoRedoEnabled(False)
        self.document().setDefaultFont(QtGui.QFont("monospace", 10, GtGui.QFont.Normal))

        super(InteractiveConsole, self).interact(welcomeMessage)

    def addToHistory(self, entry):
        if entry and self.history and history[-1] != entry:
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
        line = doc.findBlockByLineNumber(doc.lineCount()-1).text
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
        self.appendPlainText(data)

    def raw_input(self, prompt=''):
        self.prompt = prompt
        self.appendPlainText(self.prompt)
        return self.queue.get()

    def keyPressEvent(self, event):
        key = event.key()
        if key in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
            self.queue.put(self.getCommand())
        elif key == QtCore.Qt.Key_Home:
            self.setCursorPosBegin()
        elif key == QtCore.Qt.Key_End:
            self.setCursorPosEnd()
        elif key == QtCore.Qt.Key_Up:
            self.setCommand(self.prevHistoryEntry())
        elif key == QtCore.Qt.Key_Down:
            self.setCommand(self.nextHistoryEntry())
        elif key == QtCore.Qt.Key_D and event.modifiers() == QtCore.Qt.ControlMidifier:
            self.parent.close()
        else:
            super(QPlainTextEdit, self).keyPressEvent(event)
