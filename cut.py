import cv2
import numpy as np


class GraphMaker:
    def __init__(self):
        self.image = cv2.imread("./resource/hat.jpg")
        self.graph = np.zeros_like(self.image)
        self.seed_layer = np.zeros_like(self.image)
        self.seed_list = []

    def add_seed(self, seed):
        self.seed_list.append(seed)
