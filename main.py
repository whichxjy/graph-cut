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

        self.obj_seed_pen = QPen(Qt.red)
        self.obj_seed_pen.setWidth(3)

        self.bkg_seed_pen = QPen(Qt.blue)
        self.bkg_seed_pen.setWidth(3)

    def paintEvent(self, event):
        weight = self.display_image.shape[1]
        height = self.display_image.shape[0]
        qimage = QImage(
            self.display_image.data, weight, height, QImage.Format_RGB888).rgbSwapped()

        painter = QPainter(self)
        painter.drawPixmap(self.rect(), QPixmap(qimage))

        for obj_seed in self.graph_maker.obj_seed_list:
            painter.setPen(self.obj_seed_pen)
            painter.drawRect(obj_seed[0], obj_seed[1], 3, 3)

        for bkg_seed in self.graph_maker.bkg_seed_list:
            painter.setPen(self.bkg_seed_pen)
            painter.drawRect(bkg_seed[0], bkg_seed[1], 3, 3)

    def mouseMoveEvent(self, event):
        self.graph_maker.add_seed((event.x(), event.y()))
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            self.graph_maker.switch_seed_mode()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = CutGUI()
    gui.show()
    sys.exit(app.exec_())
