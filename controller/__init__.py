"""
controllers
"""

from .ConsoleController import ConsoleController

def signalInit(signalView, signalButtons, signals):
    for button in signalButtons:
        name = button.getName()
        signalView.connectButtonClicked(name, button)

    for signal in signals:
        name = signal.getName()
        signalView.connectNewData(name, signal)
