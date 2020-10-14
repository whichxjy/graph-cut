import cv2
import numpy as np


class GraphMaker:
    OBJ_SEED_MODE = 1
    BKG_SEED_MODE = 2

    OBJ_SEED_COLOR = (0, 0, 255)
    BKG_SEED_COLOR = (0, 255, 0)
    SEED_THICKNESS = -1

    OBJ_POS_VAL = 1
    BKG_POS_VAL = 0
    DEFAULT_POS_VAL = 0.5

    def __init__(self):
        self.image = cv2.imread("./resource/hat.jpg")
        self.seed_layer = np.zeros_like(self.image)

        self.seed_mode = self.OBJ_SEED_MODE
        self.obj_seed_list = []
        self.bkg_seed_list = []

        self.graph = None

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

    def process_graph(self):
        if len(self.obj_seed_list) == 0:
            print("No object seed.")
            return
        if len(self.bkg_seed_list) == 0:
            print("No background seed.")
            return

        print("Start process graph.")
        self.init_graph()

        print(self.graph)

    def init_graph(self):
        weight = self.image.shape[0]
        height = self.image.shape[1]
        self.graph = np.zeros((weight, height))
        self.graph.fill(self.DEFAULT_POS_VAL)

        for obj_seed in self.obj_seed_list:
            self.graph[obj_seed[1], obj_seed[0]] = self.OBJ_POS_VAL
        for bkg_seed in self.bkg_seed_list:
            self.graph[bkg_seed[1], bkg_seed[0]] = self.BKG_POS_VAL

    def switch_seed_mode(self):
        if self.seed_mode == self.OBJ_SEED_MODE:
            self.seed_mode = self.BKG_SEED_MODE
        elif self.seed_mode == self.BKG_SEED_MODE:
            self.seed_mode = self.OBJ_SEED_MODE
