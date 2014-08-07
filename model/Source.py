from PyQt5.QtCore import QObject, pyqtSignal
from .SignalModel import SignalModel

class Source(QObject):
    def __init__(self):
        super(Source, self).__init__()

    newData = pyqtSignal(object)

    def getSignalModel(self, signalName):
        signal = SignalModel(signalName)
        self.newData.connect(signal.receiveData)
        return signal

    def setup(self):
        pass

    def sendPackage(self, package):
        self.newData.emit(package)

    @staticmethod
    def getAvailableSignals():
        return []
