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

    def paintEvent(self, event):
        weight = self.graph_maker.image.shape[1]
        height = self.graph_maker.image.shape[0]
        qimage = QImage(
            self.graph_maker.image.data, weight, height, QImage.Format_RGB888).rgbSwapped()
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
