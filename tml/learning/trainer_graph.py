import matplotlib.pyplot as plt
import matplotlib as mlab
import numpy as np
import tensorflow.train
from enum import Enum

class Types(Enum):
    WEIGHT_FREQ = 0
    BIAS_FREQ = 1

class TrainerGraph():
    def __init__(self, optimizer, graph_type, percentiles):
        self.optimizer = optimizer
        self.graph_type = graph_type
        self.percentiles = percentiles

#    def graph(self):
#        if self.graph_type == Types.WEIGHT_FREQ:
