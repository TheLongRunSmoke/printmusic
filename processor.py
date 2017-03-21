import sys
import wave
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
from pylab import *
from gcodewriter import GCodeWriter
from math import pi


class Processor:
    def __init__(self, file):
        super().__init__()
        self.file_name = file

    async def get_waveform(self):
        spf = wave.open(self.file_name, 'rb')
        framerate = spf.getframerate()
        sound_info = spf.readframes(-1)
        sound_info = fromstring(sound_info, 'Int16')
        spf.close()
        subplot(211)
        specgram(sound_info, Fs=framerate, scale_by_freq=True, sides='default')
        show()
        return sound_info

    def get_3d(self):
        spf = wave.open(self.file_name, 'rb')
        spf.setpos(15 * spf.getframerate())
        sound_info = spf.readframes(-1)
        spf.close()
        sound_info = fromstring(sound_info, 'Int16')

        r = self.process_list(sound_info)
        p = []
        z = []
        for i in range(0, len(r)):
            p.append(i * 2 * math.pi / 10 + i * 0.2)
            z.append(i * 0.2)
        x, y = r * np.cos(p), r * np.sin(p)
        result = (x, y, z)
        return result

    def process_list(self, data):
        result = []
        radius = 60
        k = max(data) / radius
        for i in range(0, len(data)):
            if abs(data[i]) > 25000:
                if i % 2 is 0:
                    result.append(data[i] / k)
                else:
                    result.append(-data[i] / k)
        return result

# fil = sys.argv[1]
# fil = "test.wav"
#
# gcode = GCodeWriter()
# gcode.open('try')
# gcode.close()
#
# show_wave_n_spec(fil)
