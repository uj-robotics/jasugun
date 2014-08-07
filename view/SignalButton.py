from PyQt5.QtWidgets import QPushButton

class SignalButton(QPushButton):
    def __init__(self, name):
        super(SignalButton, self).__init__()
        self.setCheckable(True)
