from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPainter, QPainterPath, QPalette

class SignalView(QWidget):
    def __init__(self):
        super(SignalView, self).__init__()

        self.grapherHeight = 50
        self.graphers = {}

        self.setMinimumSize(200, 200)
        self.setBackgroundRole(QPalette.Base)
        self.setAutoFillBackground(True)


    def connect(self, signal, button):
        grapher = SignalView.Grapher(signal)
        button.clicked.connect(grapher.setActive)
        self.graphers.update({signal.getName() : grapher})

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.translate(0, self.grapherHeight*0.5)
        for grapher in self.graphers.values():
            if grapher.active:
                grapher.paint(painter)
                painter.translate(0, self.grapherHeight)

    def resizeEvent(self, event):
        for (key, grapher) in self.graphers.items():
            size = event.size()
            grapher.resize(size.width(), self.grapherHeight)

    @pyqtSlot()
    def newData(self):
        self.update() 

    class Grapher:
        
        xStep = 3

        def __init__(self, model):
            #width and height is to be set by resize
            self.width = 0
            self.height = 0
            self.model = model
            self.text = self.model.getName()
            self.offset = 50
            self.active = False

        @pyqtSlot()
        def setActive(self, active):
            self.active = active

        def paint(self, painter):
            data = self.model.getStoredData()
            amplitude = self.height/2
            painter.drawText(0, 0, self.text)
            
            path = QPainterPath()
            painter.translate(self.offset, 0)
            #signal introduces bias, which is removed here;
            #TODO: bias should not be removed here, but in model
            painter.translate(0, amplitude)
            startYOffset = data[0]*amplitude
            painter.translate(0,-startYOffset)
            i = 1
            for value in data[1:]:
                path.lineTo(i*SignalView.Grapher.xStep, -value*amplitude+startYOffset)
                i += 1
            painter.drawPath(path)
            painter.translate(0,startYOffset)
            painter.translate(-self.offset, 0)

        def resize(self, width, height):
            self.width = width
            self.height = height
            self.model.setMaxStored(self.width//SignalView.Grapher.xStep)
