from .Source import Source
#from gevent.queue import Queue
from subprocess import check_output
from Crypto.Cipher import AES
from Crypto import Random

class Emotiv(Source):
    def __init__(self):
        super(Emotiv, self).__init__()

    def setup(self):
        pass

    @staticmethod
    def getAvailableSignals():
        return ['AF3', 'AF4',
                'F3', 'F4', 'F7', 'F8',
                'FC4', 'FC5',
                'T7', 'T8',
                'O1', 'O2',
                'P7', 'P8',
                'O1', 'O2']
