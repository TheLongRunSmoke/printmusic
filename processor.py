import wave

from pylab import *


class Processor:
    def __init__(self, file):
        super().__init__()
        self.file_name = file

    def get_specgram(self):
        with wave.open(self.file_name, 'rb') as spf:
            framerate = spf.getframerate()
            sound_info = spf.readframes(-1)
            sound_info = fromstring(sound_info, 'Int16')
            spf.close()
        (a, b, c, d) = specgram(sound_info, Fs=framerate, scale_by_freq=True, sides='default')
        return a

    def get_3d(self):
        data = self.get_specgram()
        (r, p, z) = self.knitting(self.normalize(self.minimize(data)))
        x, y = self.polar_to_cartesian(r, p)
        result = (x, y, z)
        return result

    @staticmethod
    def polar_to_cartesian(r, p):
        return r * np.cos(p), r * np.sin(p)

    @staticmethod
    def minimize(data):
        print("raw data sizes: %d x %d" % (len(data), len(data[0])))
        z_max = 100
        print("z_target_step_count = %d " % (z_max / 0.2))
        step_width = len(data[0]) / (z_max / 0.2)
        print("z_step_width = %d" % step_width)
        minimized_data = []
        for i in range(0, len(data)):
            minimized_data.append([])
            for j in range(0, len(data[0]), int(step_width)):
                minimized_data[i].append(data[i][j])
        print("z_real_step_count = %d" % len(minimized_data[0]))
        print("minimized data sizes: %d x %d" % (len(minimized_data), len(minimized_data[0])))
        return minimized_data

    @staticmethod
    def normalize(data):
        outer_radius = 60
        for i in range(0, len(data)):
            kn = outer_radius / max(data[i])
            print("kn = %f" % kn)
            for j in range(0, len(data[i])):
                if data[i][j] > 60:
                    data[i][j] = 60
        return data

    @staticmethod
    def knitting(data):
        plot(data)
        show()
        r = []
        p = []
        z = []
        p_step = 2 * math.pi / len(data)
        z_step = 0.2 / len(data)
        print("z_step = %f, p_step = %f" % (z_step, p_step))
        for i in range(0, len(data[0])):
            for j in range(0, len(data)):
                r.append(15 + data[j][i])
                p.append(j * p_step)
                z.append((i*len(data) + j) * z_step)
        print(len(r))
        return r, p, z
