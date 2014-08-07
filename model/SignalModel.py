from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

class SignalModel(QObject):
    def __init__(self, name):
        super(SignalModel, self).__init__()

        self.name = name
    
    newData = pyqtSignal()

    def getName(self):
        return self.name

    def processData(self, data):
        pass

    @pyqtSlot(object)
    def receiveData(self, data):
        self.processData(data)
        self.newData.emit()
