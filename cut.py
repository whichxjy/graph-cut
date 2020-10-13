import cv2
import numpy as np


class GraphMaker:
    OBJ_SEED_MODE = 1
    BKG_SEED_MODE = 2

    OBJ_SEED_COLOR = (0, 0, 255)
    BKG_SEED_COLOR = (0, 255, 0)
    SEED_THICKNESS = 2

    def __init__(self):
        self.image = cv2.imread("./resource/hat.jpg")
        self.seed_layer = np.zeros_like(self.image)

        self.seed_mode = self.OBJ_SEED_MODE
        self.obj_seed_list = []
        self.bkg_seed_list = []

        self.graph = np.zeros_like(self.image)

    def add_seed(self, seed):
        if self.seed_mode == self.OBJ_SEED_MODE:
            if seed not in self.obj_seed_list:
                self.obj_seed_list.append(seed)
                cv2.rectangle(
                    self.seed_layer,
                    (seed[0] - 1, seed[1] - 1), (seed[0] + 1, seed[1] + 1),
                    self.OBJ_SEED_COLOR, self.SEED_THICKNESS)
        elif self.seed_mode == self.BKG_SEED_MODE:
            if seed not in self.bkg_seed_list:
                self.bkg_seed_list.append(seed)
                cv2.rectangle(
                    self.seed_layer,
                    (seed[0] - 1, seed[1] - 1), (seed[0] + 1, seed[1] + 1),
                    self.BKG_SEED_COLOR, self.SEED_THICKNESS)

    def switch_seed_mode(self):
        if self.seed_mode == self.OBJ_SEED_MODE:
            self.seed_mode = self.BKG_SEED_MODE
        elif self.seed_mode == self.BKG_SEED_MODE:
            self.seed_mode = self.OBJ_SEED_MODE
