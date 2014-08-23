

class SignalController:
    def __init__(self, model, button):
        self.model = model
        self.button = button

    def getName(self):
        return self.model.getName()

    def enable(self):
        self.button.setChecked(True)
        self.button.clicked.emit(True)

    def disable(self):
        self.button.setChecked(False)
        self.button.clicked.emit(False)
