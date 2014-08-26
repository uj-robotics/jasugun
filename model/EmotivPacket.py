import code

sensorBits = {
    'F3': [10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7],
    'FC5': [28, 29, 30, 31, 16, 17, 18, 19, 20, 21, 22, 23, 8, 9],
    'AF3': [46, 47, 32, 33, 34, 35, 36, 37, 38, 39, 24, 25, 26, 27],
    'F7': [48, 49, 50, 51, 52, 53, 54, 55, 40, 41, 42, 43, 44, 45],
    'T7': [66, 67, 68, 69, 70, 71, 56, 57, 58, 59, 60, 61, 62, 63],
    'P7': [84, 85, 86, 87, 72, 73, 74, 75, 76, 77, 78, 79, 64, 65],
    'O1': [102, 103, 88, 89, 90, 91, 92, 93, 94, 95, 80, 81, 82, 83],
    'O2': [140, 141, 142, 143, 128, 129, 130, 131, 132, 133, 134, 135, 120, 121],
    'P8': [158, 159, 144, 145, 146, 147, 148, 149, 150, 151, 136, 137, 138, 139],
    'T8': [160, 161, 162, 163, 164, 165, 166, 167, 152, 153, 154, 155, 156, 157],
    'F8': [178, 179, 180, 181, 182, 183, 168, 169, 170, 171, 172, 173, 174, 175],
    'AF4': [196, 197, 198, 199, 184, 185, 186, 187, 188, 189, 190, 191, 176, 177],
    'FC6': [214, 215, 200, 201, 202, 203, 204, 205, 206, 207, 192, 193, 194, 195],
    'F4': [216, 217, 218, 219, 220, 221, 222, 223, 208, 209, 210, 211, 212, 213]
}
quality_bits = [99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112]

class EmotivPacket(object):
    """
    Basic semantics for input bytes.
    """

    def __init__(self, data, sensors):
        self.rawData = data
        self.counter = data[0]
        self.battery = 0
        if(self.counter > 127):
            self.battery = self.counter
            g_battery = self.battery_percent()
            self.counter = 128
        self.sync = self.counter == 0xe9

        # the RESERVED byte stores the least significant 4 bits for gyroX and gyroY
        self.gyroX = data[29] << 4 | data[31] >> 4
        self.gyroY = data[30] << 4 | data[31] & 0x0F
        sensors['X']['value'] = self.gyroX
        sensors['Y']['value'] = self.gyroY

        for name, bits in sensorBits.items():
            value = self.get_level(self.rawData, bits)
            setattr(self, name, (value,))
            sensors[name]['value'] = value
        self.handle_quality(sensors)
        self.sensors = sensors

    def get_level(self, data, bits):
        level = 0
        for i in range(13, -1, -1):
            level <<= 1
            b, o = (bits[i] // 8) + 1, bits[i] % 8
            level |= (data[b] >> o) & 1
        return level

    def handle_quality(self, sensors):
        current_contact_quality = self.get_level(self.rawData, quality_bits) / 540
        sensor = self.rawData[0]
        if sensor == 0:
            sensors['F3']['quality'] = current_contact_quality
        elif sensor == 1:
            sensors['FC5']['quality'] = current_contact_quality
        elif sensor == 2:
            sensors['AF3']['quality'] = current_contact_quality
        elif sensor == 3:
            sensors['F7']['quality'] = current_contact_quality
        elif sensor == 4:
            sensors['T7']['quality'] = current_contact_quality
        elif sensor == 5:
            sensors['P7']['quality'] = current_contact_quality
        elif sensor == 6:
            sensors['O1']['quality'] = current_contact_quality
        elif sensor == 7:
            sensors['O2']['quality'] = current_contact_quality
        elif sensor == 8:
            sensors['P8']['quality'] = current_contact_quality
        elif sensor == 9:
            sensors['T8']['quality'] = current_contact_quality
        elif sensor == 10:
            sensors['F8']['quality'] = current_contact_quality
        elif sensor == 11:
            sensors['AF4']['quality'] = current_contact_quality
        elif sensor == 12:
            sensors['FC6']['quality'] = current_contact_quality
        elif sensor == 13:
            sensors['F4']['quality'] = current_contact_quality
        elif sensor == 14:
            sensors['F8']['quality'] = current_contact_quality
        elif sensor == 15:
            sensors['AF4']['quality'] = current_contact_quality
        elif sensor == 64:
            sensors['F3']['quality'] = current_contact_quality
        elif sensor == 65:
            sensors['FC5']['quality'] = current_contact_quality
        elif sensor == 66:
            sensors['AF3']['quality'] = current_contact_quality
        elif sensor == 67:
            sensors['F7']['quality'] = current_contact_quality
        elif sensor == 68:
            sensors['T7']['quality'] = current_contact_quality
        elif sensor == 69:
            sensors['P7']['quality'] = current_contact_quality
        elif sensor == 70:
            sensors['O1']['quality'] = current_contact_quality
        elif sensor == 71:
            sensors['O2']['quality'] = current_contact_quality
        elif sensor == 72:
            sensors['P8']['quality'] = current_contact_quality
        elif sensor == 73:
            sensors['T8']['quality'] = current_contact_quality
        elif sensor == 74:
            sensors['F8']['quality'] = current_contact_quality
        elif sensor == 75:
            sensors['AF4']['quality'] = current_contact_quality
        elif sensor == 76:
            sensors['FC6']['quality'] = current_contact_quality
        elif sensor == 77:
            sensors['F4']['quality'] = current_contact_quality
        elif sensor == 78:
            sensors['F8']['quality'] = current_contact_quality
        elif sensor == 79:
            sensors['AF4']['quality'] = current_contact_quality
        elif sensor == 80:
            sensors['FC6']['quality'] = current_contact_quality
        else:
            sensors['Unknown']['quality'] = current_contact_quality
            sensors['Unknown']['value'] = sensor
        return current_contact_quality

    def battery_percent(self):
        if self.battery > 248:
            return 100
        elif self.battery == 247:
            return 99
        elif self.battery == 246:
            return 97
        elif self.battery == 245:
            return 93
        elif self.battery == 244:
            return 89
        elif self.battery == 243:
            return 85
        elif self.battery == 242:
            return 82
        elif self.battery == 241:
            return 77
        elif self.battery == 240:
            return 72
        elif self.battery == 239:
            return 66
        elif self.battery == 238:
            return 62
        elif self.battery == 237:
            return 55
        elif self.battery == 236:
            return 46
        elif self.battery == 235:
            return 32
        elif self.battery == 234:
            return 20
        elif self.battery == 233:
            return 12
        elif self.battery == 232:
            return 6
        elif self.battery == 231:
            return 4
        elif self.battery == 230:
            return 3
        elif self.battery == 229:
            return 2
        elif self.battery == 228:
            return 2
        elif self.battery == 227:
            return 2
        elif self.battery == 226:
            return 1
        else:
            return 0
