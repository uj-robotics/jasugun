from PyQt5.QtWidgets import QWidget

class SignalView(QWidget):
    def __init__(self):
        super(SignalView, self).__init__()

    def connectButtonClicked(self, buttonName, button):
        pass

    def connectNewData(self, signalName, signal):
        pass
