import math
import random

from Node import Node
from CoreLLM import CoreLLM
from ValuerLLM import ValuerLLM

class MCTS:
    def __init__(self, d, c, base_history, k=2,  root=None):
        self.root = root
        self.k = k # number of nodes to spawn for each expanding
        self.coreLLM = CoreLLM()
        self.valuerLLM = ValuerLLM()
        self.exploration_const = c
        self.rollout_depth = d
        self.lastNodeId = 0
        self.base_history = base_history

    def search(self, iterations=100):
        for _ in range(iterations):
            node = self.select(self.root)
            child = self.expand(node)
            value = self.rollout(child.history)
            child.update(value)

        return max(self.root.children, key=lambda n: n.Q)

    def init_root(self):
        self.root = Node(self.base_history, self.lastNodeId)
        self.lastNodeId += 1
        self.root.N = 1
        self.expand(self.root)
        self.root.N = 0
        print("_________[Tree Action] Root Node created._________")

    def expand(self, node: Node):
        new_child_nodes = []

        if node.is_leaf():
            if node.N != 0:
                candidates = self.coreLLM.get_messages(node.history, self.k)
                for candidate in candidates:
                    new_child_nodes.append(node.add_child(candidate, self.lastNodeId))
                    self.lastNodeId += 1

        return random.choice(new_child_nodes) if new_child_nodes else node


    def select(self, node):
        while not node.is_leaf() and node.is_fully_expanded(self.k):
            node = max(node.children, key=lambda n: n.uct_score(self.exploration_const))

        print("[Tree Select Action] Selected node_id=" + str(node.node_id) + " with uct_score=" + str(node.uct_score(self.exploration_const)))
        return node

    def rollout(self, history):
        sim_history = history.copy()
        for _ in range(self.rollout_depth):
            user_msg = self.coreLLM.get_messages(sim_history, 1)[0]
            sim_history.append(user_msg)
            agent_msg = self.coreLLM.get_messages(sim_history, self.k)[0]
            sim_history.append(agent_msg)

        return self.valuerLLM.value(sim_history)

    def traverse(self):
        self.root.traverse()


def main():
    history = ["Alice: Hi there!", "Bob: Hello, how are you?"]

    root = Node(history=history, id=0)

    mcts = MCTS(
        k=3,
        c=math.sqrt(2),
        d=2,
        base_history=history,
    )

    mcts.init_root()
    result = mcts.search(100)

    print("[RESULT] Result message =" + str(result.msg))

if __name__ == "__main__":
    main()
