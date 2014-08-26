from .Source import Source
from .EmotivPacket import EmotivPacket
from subprocess import check_output
from Crypto.Cipher import AES
from Crypto import Random
import threading 
import os
import code

class Emotiv(Source):
    def __init__(self, headsetId=0, research_headset=True):
        self.battery = 0
        self.headsetId = headsetId
        self.research_headset = research_headset
        self.sensors = {
            'F3': {'value': 0, 'quality': 0},
            'FC6': {'value': 0, 'quality': 0},
            'P7': {'value': 0, 'quality': 0},
            'T8': {'value': 0, 'quality': 0},
            'F7': {'value': 0, 'quality': 0},
            'F8': {'value': 0, 'quality': 0},
            'T7': {'value': 0, 'quality': 0},
            'P8': {'value': 0, 'quality': 0},
            'AF4': {'value': 0, 'quality': 0},
            'F4': {'value': 0, 'quality': 0},
            'AF3': {'value': 0, 'quality': 0},
            'O2': {'value': 0, 'quality': 0},
            'O1': {'value': 0, 'quality': 0},
            'FC5': {'value': 0, 'quality': 0},
            'X': {'value': 0, 'quality': 0},
            'Y': {'value': 0, 'quality': 0},
            'Unknown': {'value': 0, 'quality': 0}
        }

        super(Emotiv, self).__init__()

    def __enter__(self):
        return self

    def __exit__(self):
        self.hidraw.close()

    def setup(self):
        self.setupPosix()

    @staticmethod
    def getAvailableSignals():
        return ['AF3', 'AF4',
                'F3', 'F4', 'F7', 'F8',
                'FC5', 'FC6',
                'T7', 'T8',
                'O1', 'O2',
                'P7', 'P8']

    def setupCrypto(self, sn):
        type = 0 # feature[5]
        type &= 0xF
        type = 0
        # I believe type == True is for the Dev headset, I'm not using that. That's the point of this library in the first place I thought.
        k = ['\0'] * 16
        k[0] = sn[-1]
        k[1] = '\0'
        k[2] = sn[-2]
        if type:
            k[3] = 'H'
            k[4] = sn[-1]
            k[5] = '\0'
            k[6] = sn[-2]
            k[7] = 'T'
            k[8] = sn[-3]
            k[9] = '\x10'
            k[10] = sn[-4]
            k[11] = 'B'
        else:
            k[3] = 'T'
            k[4] = sn[-3]
            k[5] = '\x10'
            k[6] = sn[-4]
            k[7] = 'B'
            k[8] = sn[-1]
            k[9] = '\0'
            k[10] = sn[-2]
            k[11] = 'H'
        k[12] = sn[-3]
        k[13] = '\0'
        k[14] = sn[-4]
        k[15] = 'P'
        key = ''.join(k)
        iv = Random.new().read(AES.block_size)
        self.cipher = AES.new(key, AES.MODE_ECB, iv)

    def decryptPacket(self, task):
        data = self.cipher.decrypt(task[:16]) + self.cipher.decrypt(task[16:])
        packet = EmotivPacket(data, self.sensors)
        return packet

    def setupPosix(self):
        _os_decryption = False
        if os.path.exists('/dev/eeg/raw'):
            # The decrpytion is handled by the Linux epoc daemon. We don't need to handle it there.
            _os_decryption = True
            self.hidraw = open("/dev/eeg/raw")
        else:
            setup = self.getLinuxSetup()
            self.serialNum = setup[0]
            if os.path.exists("/dev/" + setup[1]):
                self.hidraw = open("/dev/" + setup[1], 'rb')
            else:
                self.hidraw = open("/dev/hidraw4", 'rb')
            self.setupCrypto(self.serialNum)
            thread = threading.Thread(target=self.read, daemon=True)
            thread.start()
        return True

    def read(self):
        while True:
            data = self.hidraw.read(32)
            if data != "":
                packet = self.decryptPacket(data)
                self.sendPackage(packet)

    def getLinuxSetup(self):
        rawinputs = []
        for filename in os.listdir("/sys/class/hidraw"):
            realInputPath = check_output(["realpath", "/sys/class/hidraw/" + filename])
            realInputPath = realInputPath.decode()
            sPaths = realInputPath.split('/')
            s = len(sPaths)
            s = s - 4
            i = 0
            path = ""
            while s > i:
                path = path + sPaths[i] + "/"
                i += 1
            rawinputs.append([path, filename])
        hiddevices = []
        # TODO: Add support for multiple USB sticks? make a bit more elegant
        for input in rawinputs:
            try:
                with open(input[0] + "/manufacturer", 'r') as f:
                    manufacturer = f.readline()
                    f.close()
                if ("Emotiv Systems Inc." in manufacturer) or ("Emotiv Systems Pty Ltd" in manufacturer) :
                    with open(input[0] + "/serial", 'r') as f:
                        serial = f.readline().strip()
                        f.close()
                    print("Serial: " + serial + " Device: " + input[1])
                    # Great we found it. But we need to use the second one...
                    hidraw = input[1]
                    id_hidraw = int(hidraw[-1])
                    # The dev headset might use the first device, or maybe if more than one are connected they might.
                    id_hidraw += 1
                    hidraw = "hidraw" + id_hidraw.__str__()
                    print("Serial: " + serial + " Device: " + hidraw + " (Active)")
                    return [serial, hidraw, ]
            except IOError as e:
                print("Couldn't open file: %s" % e)
