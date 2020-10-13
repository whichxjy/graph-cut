import cv2
import numpy as np


class GraphMaker:
    OBJ_SEED_MODE = 1
    BKG_SEED_MODE = 2

    def __init__(self):
        self.image = cv2.imread("./resource/hat.jpg")
        self.graph = np.zeros_like(self.image)
        self.seed_layer = np.zeros_like(self.image)

        self.seed_mode = self.OBJ_SEED_MODE
        self.obj_seed_list = []
        self.bkg_seed_list = []

    def add_seed(self, seed):
        if self.seed_mode == self.OBJ_SEED_MODE:
            self.obj_seed_list.append(seed)
        elif self.seed_mode == self.BKG_SEED_MODE:
            self.bkg_seed_list.append(seed)

    def switch_seed_mode(self):
        if self.seed_mode == self.OBJ_SEED_MODE:
            self.seed_mode = self.BKG_SEED_MODE
        elif self.seed_mode == self.BKG_SEED_MODE:
            self.seed_mode = self.OBJ_SEED_MODE
