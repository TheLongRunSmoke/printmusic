import sys
import wave
from collections import deque

from mpl_toolkits.mplot3d import Axes3D
from PyQt5 import QtCore
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from processor import Processor


class MainGUI(QMainWindow):
    processor = None
    view = None

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(800, 800)
        self.center()
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setWindowTitle('PrintableMusic')
        # self.setWindowIcon(QIcon('web.png'))

        self.view = Plot3DCanvas(self, width=8, height=8)
        self.view.move(0, 0)

        self.add_menu()
        self.statusBar()
        self.show()

    def add_menu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu('&File')
        action_load = QAction("&Load...", self)
        action_load.setStatusTip('Load file')
        action_load.triggered.connect(self.load_file)
        file_menu.addAction(action_load)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def load_file(self):
        file_names = QFileDialog.getOpenFileName(self, 'Open file', '', "WAVE files (*.wav)")
        if file_names[0]:
            self.statusBar().showMessage("Open: " + file_names[0])
            self.processor = Processor(file_names[0])
            self.show_3d(self.processor.get_3d())

    def show_3d(self, data):
        self.view.plot(data)
        return 0


class Plot3DCanvas(FigureCanvas):
    def __init__(self, parent=None, width=8, height=8, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111, projection='3d')
        Axes3D.mouse_init(self.axes, rotate_btn=1, zoom_btn=3)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, data):
        wf = self.figure.add_subplot(111, projection='3d')
        wf.set_zlim([0, 120])
        wf.plot(*data, label='test')
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainGUI()
    sys.exit(app.exec_())
