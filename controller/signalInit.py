

def signalInit(signalView, source, signals, buttons):
    source.connectSlot(signalView.newData)

    for signal in signals:
        signalView.connectSignal(signal)

    for button in buttons:
        signalView.connectButton(button)
