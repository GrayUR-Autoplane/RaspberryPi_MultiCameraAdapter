from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread
from picamera import PiCamera  # Use picamera instead of picamera2
import RPi.GPIO as gp
import time
import sys

width = 320
height = 240

class WorkThread(QThread):
    def __init__(self):
        super(WorkThread, self).__init__()
        gp.setwarnings(False)
        gp.setmode(gp.BOARD)
        gp.setup(7, gp.OUT)
        gp.setup(11, gp.OUT)
        gp.setup(12, gp.OUT)
        self.camera = PiCamera()
        self.camera.resolution = (width, height)
        self.camera.start_preview()

    def run(self):
        while True:
            self.capture_image()

    def capture_image(self):
        try:
            gp.output(7, gp.HIGH)
            gp.output(11, gp.LOW)
            gp.output(12, gp.HIGH)
            time.sleep(0.5)
            self.camera.capture('output.jpg')
            image = QImage('output.jpg')
            pixmap = QPixmap.fromImage(image)
            image_label.setPixmap(pixmap)
        except Exception as e:
            print("Capture error: " + str(e))

app = QApplication([])
window = QWidget()
layout_v = QVBoxLayout()
image_label = QLabel()
image_label.setFixedSize(width, height)
window.setWindowTitle("Raspberry Pi Camera Preview")
layout_v.addWidget(image_label)
window.setLayout(layout_v)
window.resize(width, height)
work = WorkThread()

if __name__ == "__main__":
    window.show()
    work.start()
    sys.exit(app.exec_())
