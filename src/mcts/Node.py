import math
from copy import copy
from typing import List, Dict

class Node:
    # Node contains List[Dict[str, str]] as a history

    def __init__(self, history: List[Dict[str, str]], _id, parent=None, exploration_weight=0, msg=None):
        self.parent = parent
        self.history = history # messages history
        self.children = []
        self.Q = 0 # total reward of the node
        self.V = 0 # mean value of award (Q / N)
        self.N = 0 # total visit count of the node
        self.exploration_weight = exploration_weight # exploration weight of the node
        self.msg = msg
        self.node_id = _id
        self.children_count = 0

    # Node history is now the olds history array of Dict combined with new message, which is Dict[str, str]
    def add_child(self, response, _id):
        # response is a dictionary

        child = Node(parent=self, msg=response["message"], history=self.history + [response], _id=_id)
        self.children.append(child)
        self.children_count += 1

        print("[Tree Action] Child with id=" + str(_id) + " and parent_id=" + str(self.node_id) + " added. Message: " + response["message"])

        return child

    def is_leaf(self):
        return len(self.children) == 0

    def uct_score(self, c=math.sqrt(2)):
        if self.parent is None or self.N == 0:
            return float('inf')
        return self.V + 2 * math.sqrt((math.log10(self.parent.N) / self.N))

    def update(self, value):
        self.N += 1
        self.Q += value
        self.V = self.Q / self.N
        if self.parent:
            self.parent.update(value)

        print("[Tree Action] Node with id=" + str(self.node_id) + " updated: q: " + str(self.Q), ", n: " + str(self.N))

    def is_fully_expanded(self, k):
        return self.children_count == k