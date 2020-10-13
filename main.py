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

        self.hello = (0, 0)

    def paintEvent(self, event):
        weight = self.display_image.shape[1]
        height = self.display_image.shape[0]
        qimage = QImage(
            self.display_image.data, weight, height, QImage.Format_RGB888).rgbSwapped()

        painter = QPainter(self)
        painter.drawPixmap(self.rect(), QPixmap(qimage))

        pen_rectangle = QPen(Qt.red)
        pen_rectangle.setWidth(3)

        painter.setPen(pen_rectangle)
        painter.drawRect(self.hello[0], self.hello[1], 3, 3)

    def mouseMoveEvent(self, event):
        self.hello = (event.x(), event.y())
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = CutGUI()
    gui.show()
    sys.exit(app.exec_())
