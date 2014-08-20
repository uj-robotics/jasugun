from PyQt5.QtCore import QObject, pyqtSlot

class SignalModel(QObject):
    def __init__(self, name):
        super(SignalModel, self).__init__()

        self.name = name
        self.storedData = []
        self.maxLength = 40

    def getName(self):
        return self.name

    def getStoredData(self):
        return self.storedData

    @pyqtSlot(object)
    def receiveData(self, package):
        self.storedData.append(package[self.name])
        if len(self.storedData) >= self.maxLength:
            self.storedData.pop(0)
