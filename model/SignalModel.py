from PyQt5.QtCore import QObject, pyqtSlot

class SignalModel(QObject):
    def __init__(self, name):
        super(SignalModel, self).__init__()

        self.name = name
        self.storedData = []
        self.maxStored = 0
        self.bias = 0

    def getName(self):
        return self.name

    def getStoredData(self):
        return self.storedData

    def setMaxStored(self, maxStored):
        self.maxStored = maxStored

    @pyqtSlot(object)
    def receiveData(self, package):
        if self.maxStored > 0:
            value = package[self.name]
            stored = len(self.storedData)
            self.bias = (self.bias*stored + value)/(stored+1)
            value = value - self.bias
            
            self.storedData.append(value)
            while len(self.storedData) >= self.maxStored:
                self.storedData.pop(0)
