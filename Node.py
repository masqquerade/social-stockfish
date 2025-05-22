import math
from collections import defaultdict
import numpy as np

class Node:
    def __init__(self, history, parent=None, exploration_weight=0, msg=None):
        self.parent = parent
        self.history = history # messages history
        self.children = []
        self.Q = 0 # total reward of the node
        self.V = 0 # mean value of award (Q / N)
        self.N = 0 # total visit count of the node
        self.exploration_weight = exploration_weight # exploration weight of the node
        self.msg = msg

    def add_child(self, msg):
        child = Node(parent=self, msg=msg, history=self.history + [msg])
        self.children.append(child)

    def is_leaf(self):
        return len(self.children) == 0

    def uct_score(self, c=math.sqrt(2)):
        if self.parent is None or self.N == 0:
            return float('inf')
        return self.V + 2 * math.sqrt((math.log10(self.N) / self.parent.N))

    def update(self, value):
        self.N += 1
        self.Q += value
        self.V = self.Q / self.N
        if self.parent:
            self.parent.update(value)