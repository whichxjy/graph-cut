import sys
from cv2 import imread
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np


class CutGUI(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        self.image = imread("./hat.jpg")
        qimage = QImage(
            self.image.data, self.image.shape[1], self.image.shape[0], QImage.Format_RGB888).rgbSwapped()
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), QPixmap(qimage))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = CutGUI()
    gui.show()
    sys.exit(app.exec_())
