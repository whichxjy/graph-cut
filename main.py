from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import numpy as np
import cv2

from cut import GraphMaker


class CutGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.graph_maker = GraphMaker()
        self.origin_image = self.graph_maker.image

    def paintEvent(self, event):
        weight = self.origin_image.shape[1]
        height = self.origin_image.shape[0]
        self.resize(weight, height)

        display_image = cv2.addWeighted(
            self.origin_image, 0.9, self.graph_maker.get_mask_layer(), 0.8, 0.1)

        qimage = QImage(
            display_image.data, weight, height, QImage.Format_RGB888).rgbSwapped()

        painter = QPainter(self)
        painter.drawPixmap(self.rect(), QPixmap(qimage))

    def mouseMoveEvent(self, event):
        self.graph_maker.add_seed((event.x(), event.y()))
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Return:
            self.graph_maker.process_graph()
        else:
            self.graph_maker.switch_seed_mode()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = CutGUI()
    gui.show()
    sys.exit(app.exec_())
