from PyQt5.QtCore import QObject, pyqtSignal
from .SignalModel import SignalModel
import threading
import time
import numpy as np

class Source(QObject):

    newData = pyqtSignal(object)
    newDataNotify = pyqtSignal()

    def __init__(self):
        super(Source, self).__init__()

        self.setup()

    def setup(self):
        thread = threading.Thread(target=self.activity, daemon=True)
        thread.start()

    def activity(self):
        t = 0
        while True:
            time.sleep(0.2)
            signalNames = self.getAvailableSignals()
            package = {}
            for name in signalNames:
                package.update({name : np.sin(2*t)})
            t += 0.2
            self.sendPackage(package)

    def getSignalModel(self, signalName):
        signal = SignalModel(signalName)
        self.newData.connect(signal.receiveData)
        return signal

    def notify(self, slot):
        self.newDataNotify.connect(slot)

    def sendPackage(self, package):
        self.newData.emit(package)
        self.newDataNotify.emit()

    @staticmethod
    def getAvailableSignals():
        return ['F3', 'F4']
