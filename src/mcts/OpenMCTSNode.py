from typing import Optional

from src.Planner.Actions import RomanceAction
from src.Selector.Selector import Selector

class OpenMCTSNode:
    def __init__(self,
                 parent: "Optional[OpenMCTSNode]",
                 action: RomanceAction,
                 p: float,
                 _id: int):

        self.parent = parent
        self.action = action
        self.id = _id
        self.children = []
        self.children_count = 0

        self.Q = 0 # Total reward of the node
        self.N = 0 # Total count of visits of the node
        self.P = p # Action reward of the node

    def add_child(self, action, _id, child_p):
        child = OpenMCTSNode(
            parent = self,
            action = action,
            p = child_p,
            _id = _id
        )

        self.children.append(child)
        self.children_count += 1

        print("[Open MCTS Tree Action] Child with id=" + str(_id) + " and parent_id=" + str(self.id) + " added.")

    def get_puct_score(self):
        return Selector.puct_score(self.Q, self.P, self.N, self.parent.N)

    def update(self, reward):
        self.N += 1
        self.Q += reward
        if self.parent is not None:
            self.parent.update(reward)

        print("[Open MCTS Tree Action] Node with id=" + str(self.id) + " updated: Q: " + str(self.Q), ", N: " + str(self.N))

    def is_leaf(self):
        return self.children_count == 0

    def is_fully_expanded(self, k):
        return self.children_count == k