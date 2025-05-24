import math

class Node:
    def __init__(self, history, id, parent=None, exploration_weight=0, msg=None):
        self.parent = parent
        self.history = history # messages history
        self.children = []
        self.Q = 0 # total reward of the node
        self.V = 0 # mean value of award (Q / N)
        self.N = 0 # total visit count of the node
        self.exploration_weight = exploration_weight # exploration weight of the node
        self.msg = msg
        self.node_id = id
        self.children_count = 0

    def add_child(self, msg, id):
        child = Node(parent=self, msg=msg, history=self.history + [msg], id=id)
        self.children.append(child)
        self.children_count += 1

        print("[Tree Action] Child with id=" + str(id) + " and parent_id=" + str(self.node_id) + " added")

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