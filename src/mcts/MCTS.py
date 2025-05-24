import math
import random

from src.mcts.Node import Node
from src.LLM.MessagesCreationAgent import MessagesCreationAgent
from src.LLM.ValuerAgent import ValuerAgent

class MCTS:
    def __init__(self, c, base_history, api_key, k=2,  root=None):
        self.root = root
        self.k = k # number of nodes to spawn for each expanding
        self.MessagesCreationAgent = MessagesCreationAgent(api_key)
        self.ValuerAgent = ValuerAgent()
        self.exploration_const = c
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
                candidates = self.MessagesCreationAgent.get_messages(node.history, self.k)
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
        user_msg = self.MessagesCreationAgent.get_messages(sim_history)[0]
        sim_history.append(user_msg)
        agent_msg = self.MessagesCreationAgent.get_messages(sim_history)[0]
        sim_history.append(agent_msg)

        return self.ValuerAgent.value(sim_history)

    def traverse(self):
        self.root.traverse()