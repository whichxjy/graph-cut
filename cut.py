import cv2
import numpy as np


class GraphMaker:
    OBJ_SEED_MODE = 1
    BKG_SEED_MODE = 2

    OBJ_SEED_COLOR = (0, 0, 255)
    BKG_SEED_COLOR = (0, 255, 0)
    SEED_THICKNESS = 2

    OBJ_POS_VAL = 1
    BKG_POS_VAL = 0
    DEFAULT_POS_VAL = 0.5

    MAX_NUM = 99999999999

    def __init__(self):
        self.image = cv2.imread("./resource/hat.jpg")
        self.seed_layer = np.zeros_like(self.image)

        self.seed_mode = self.OBJ_SEED_MODE
        self.obj_seed_list = []
        self.bkg_seed_list = []

        self.graph = None

        self.node_list = None
        self.edge_list = None

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

        print("Start processing graph.")
        self.init_graph()

        print("Start making graph.")
        self.make_graph()

    def init_graph(self):
        weight = self.image.shape[0]
        height = self.image.shape[1]
        self.graph = np.zeros((weight, height))
        self.graph.fill(self.DEFAULT_POS_VAL)

        for obj_seed in self.obj_seed_list:
            self.graph[obj_seed[1], obj_seed[0]] = self.OBJ_POS_VAL
        for bkg_seed in self.bkg_seed_list:
            self.graph[bkg_seed[1], bkg_seed[0]] = self.BKG_POS_VAL

    def make_graph(self):
        # node: [node_index, cap_source, cap_sink]
        self.node_list = []
        # edge: [a_node_index, b_node_index, capacity]
        self.edge_list = []

        height = self.image.shape[1]

        # Create nodes.
        for (y, x), val in np.ndenumerate(self.graph):
            if val == self.OBJ_POS_VAL:
                self.node_list.append(
                    (self.get_node_index(x, y, height), self.MAX_NUM, 0))
            elif val == self.BKG_POS_VAL:
                self.node_list.append(
                    (self.get_node_index(x, y, height), 0, self.MAX_NUM))
            else:
                self.node_list.append(
                    (self.get_node_index(x, y, height), 0, 0))

        # Create edges.
        # 0 < edge_capacity <= 1
        for (y, x), val in np.ndenumerate(self.graph):
            if x == self.graph.shape[1] - 1 or y == self.graph.shape[0] - 1:
                continue

            curr_node_index = self.get_node_index(x, y, height)

            # (x, y) <--> (x + 1, y)
            right_node_index = self.get_node_index(x + 1, y, height)
            edge_capacity = 1 / (1 +
                                 np.sum(np.power(self.image[y, x] - self.image[y, x + 1], 2)))
            self.edge_list.append(
                (curr_node_index, right_node_index, edge_capacity))

            # (x, y) <--> (x, y + 1)
            down_node_index = self.get_node_index(x, y + 1, height)
            edge_capacity = 1 / (1 +
                                 np.sum(np.power(self.image[y, x] - self.image[y + 1, x], 2)))
            self.edge_list.append(
                (curr_node_index, down_node_index, edge_capacity))

    def switch_seed_mode(self):
        if self.seed_mode == self.OBJ_SEED_MODE:
            self.seed_mode = self.BKG_SEED_MODE
        elif self.seed_mode == self.BKG_SEED_MODE:
            self.seed_mode = self.OBJ_SEED_MODE

    @staticmethod
    def get_node_index(x, y, col_num):
        return y * col_num + x
