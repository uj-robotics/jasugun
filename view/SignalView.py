from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPainter, QPainterPath, QPalette

class SignalView(QWidget):
    def __init__(self):
        super(SignalView, self).__init__()

        self.grapherHeight = 100
        self.graphers = {}

        self.setMinimumSize(200, 200)
        self.setBackgroundRole(QPalette.Base)
        self.setAutoFillBackground(True)


    def connect(self, signal, button):
        grapher = SignalView.Grapher(self.width, self.grapherHeight, signal)
        button.clicked.connect(grapher.setActive)
        self.graphers.update({signal.getName() : grapher})

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.translate(0, self.grapherHeight*0.5)
        for grapher in self.graphers.values():
            if grapher.active:
                grapher.paint(painter)
                painter.translate(0, self.grapherHeight)

    @pyqtSlot()
    def newData(self):
        self.update() 

    class Grapher:
        
        xStep = 10

        def __init__(self, width, height, signal):
            self.width = width
            self.height = height
            self.signal = signal
            self.text = self.signal.getName()
            self.offset = 50
            self.active = False

        @pyqtSlot()
        def setActive(self, active):
            self.active = active

        def paint(self, painter):
            data = self.signal.getStoredData()
            amplitude = self.height/2
            painter.drawText(0, 0, self.text)
            
            path = QPainterPath()
            painter.translate(self.offset, 0)
            startYOffset = data[0]*amplitude
            painter.translate(0,-startYOffset)
            i = 1
            for value in data[1:]:
                path.lineTo(i*SignalView.Grapher.xStep, -value*amplitude+startYOffset)
                i += 1
            painter.drawPath(path)
            painter.translate(0,startYOffset)
            painter.translate(-self.offset, 0)
