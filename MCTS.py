import math

from Node import Node
from CoreLLM import CoreLLM
from ValuerLLM import ValuerLLM

class MCTS:
    def __init__(self, d, root, c, k=2):
        self.root = root
        self.k = k # number of nodes to spawn for each expanding
        self.coreLLM = CoreLLM()
        self.valuerLLM = ValuerLLM()
        self.exploration_const = c
        self.rollout_depth = d

    def search(self, root, iterations=100):
        for _ in range(iterations):
            node = self.select(root)
            child = self.expand(node)
            value = self.rollout(child)
            child.update(value)

    def expand(self, node: Node):
        new_child_nodes = []

        if node.is_leaf():
            if node.N == 0:
                candidates = self.coreLLM.get_messages(node.history, self.k)
                for candidate in candidates:
                    new_child_nodes.append(node.add_child(candidate))

        return new_child_nodes[0] if new_child_nodes else node


    def select(self, node):
        while not node.is_leaf() and len(node.children) >= self.k:
            node = max(node.children, key=lambda n: n.uct_score(self.exploration_const))

        return node

    def rollout(self, history):
        sim_history = history.copy()
        for _ in range(self.rollout_depth):
            user_msg = self.coreLLM.get_messages(sim_history, 1)[0]
            sim_history.append(user_msg)
            agent_msg = self.coreLLM.get_messages(sim_history, self.k)[0]
            sim_history.append(agent_msg)

        return self.valuerLLM.value(sim_history)


def main():
    history = ["Alice: Hi there!", "Bob: Hello, how are you?"]

    root = Node(history=history)

    mcts = MCTS(
        k=3,
        root=root,
        c=math.sqrt(2),
        d=2
    )

    mcts.expand(root)

if __name__ == "__main__":
    main()
