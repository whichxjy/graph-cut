import cv2
import numpy as np
import maxflow


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

    OBJ_SEG_COLOR = (0, 0, 0)
    BKG_SEG_COLOR = (204, 204, 153)

    SHOW_SEED_MODE = 1
    SHOW_SEG_MODE = 2

    def __init__(self, input_file):
        self.image = cv2.imread(input_file)
        self.seed_layer = np.zeros_like(self.image)
        self.segment_layer = np.zeros_like(self.image)

        self.seed_mode = self.OBJ_SEED_MODE
        self.obj_seed_list = []
        self.bkg_seed_list = []

        self.graph = None

        self.node_list = None
        self.edge_list = None

        self.show_mode = self.SHOW_SEED_MODE

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

        print("Start cutting graph.")
        self.cut_graph()

        self.show_mode = self.SHOW_SEG_MODE
        print("Done.")

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
                    (self.get_node_index(x, y, height), 0, self.MAX_NUM))
            elif val == self.BKG_POS_VAL:
                self.node_list.append(
                    (self.get_node_index(x, y, height), self.MAX_NUM, 0))
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

            # (x, y) <--> (x + 1, y + 1)
            right_down_node_index = self.get_node_index(x + 1, y + 1, height)
            edge_capacity = 1 / (1 +
                                 np.sum(np.power(self.image[y, x] - self.image[y + 1, x + 1], 2)))
            self.edge_list.append(
                (curr_node_index, right_down_node_index, edge_capacity))

    def cut_graph(self):
        virtual_graph = maxflow.Graph[float](
            len(self.node_list), len(self.edge_list))
        virtual_node_list = virtual_graph.add_nodes(len(self.node_list))

        height = self.image.shape[1]

        # Add edges to terminal nodes.
        for node in self.node_list:
            node_index = node[0]
            cap_source = node[1]
            cap_sink = node[2]
            virtual_graph.add_tedge(
                virtual_node_list[node_index], cap_source, cap_sink)

        # Add other edges.
        for edge in self.edge_list:
            a_node_index = edge[0]
            b_node_index = edge[1]
            capacity = edge[2]
            virtual_graph.add_edge(
                virtual_node_list[a_node_index], virtual_node_list[b_node_index], capacity, capacity)

        virtual_graph.maxflow()

        for node_index in range(len(self.node_list)):
            x, y = self.get_pos(node_index, height)
            if virtual_graph.get_segment(node_index) == 1:
                # It's an object position.
                self.segment_layer[y, x] = self.OBJ_SEG_COLOR
            else:
                # It's a background position.
                self.segment_layer[y, x] = self.BKG_SEG_COLOR

    def get_mask_layer(self):
        if self.show_mode == self.SHOW_SEED_MODE:
            return self.seed_layer
        return self.segment_layer

    def switch_seed_mode(self):
        if self.seed_mode == self.OBJ_SEED_MODE:
            self.seed_mode = self.BKG_SEED_MODE
        elif self.seed_mode == self.BKG_SEED_MODE:
            self.seed_mode = self.OBJ_SEED_MODE

    @staticmethod
    def get_node_index(x, y, col_num):
        return y * col_num + x

    @staticmethod
    def get_pos(node_index, col_num):
        return (node_index % col_num), (node_index // col_num)
