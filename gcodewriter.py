class GCodeWriter:

    START = ('G90',
             'M82',
             'M106 S0',
             'M140 S60',
             'M190 S60',
             'M104 S200 T0',
             'M109 S200 T0',
             'G29',
             'G92 E0')

    END = ('M104 S0 ; turn off extruder',
           'M140 S0 ; turn off bed',
           'M106 S0',
           'G28 X Y ; go to X and Y home',
           'M84 ; disable motors')


    def __init__(self):
        self.workfile = None

    def open(self,file):
        self.workfile = open(file +'.gcode', 'w')
        self.workfile.write('\n'.join(self.START)+'\n')

    def close(self):
        if (self.workfile is not None):
            self.workfile.write('\n'.join(self.END))
            self.workfile.close()
        
