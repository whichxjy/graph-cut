from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import numpy as np

from cut import GraphMaker


class CutGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.graph_maker = GraphMaker()
        self.display_image = self.graph_maker.image

    def paintEvent(self, event):
        weight = self.display_image.shape[1]
        height = self.display_image.shape[0]
        qimage = QImage(
            self.display_image.data, weight, height, QImage.Format_RGB888).rgbSwapped()
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
