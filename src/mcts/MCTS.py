import json
import math
import random
from typing import Dict, List

from src.mcts.Node import Node
from src.LLM.MessagesCreationAgent import MessagesCreationAgent
from src.LLM.ValuerAgent import ValuerAgent

def parse_response(message):
    json_str = message.content[0].text
    print(json_str)
    data = json.loads(json_str)

    return data # python dic

class MCTS:
    def __init__(self, c, base_history, max_tokens, api_key, k=2,  root=None):
        self.root = root
        self.k = k # number of nodes to spawn for each expanding
        self.MessagesCreationAgent = MessagesCreationAgent(api_key, max_tokens) ## max_tokens delete
        self.ValuerAgent = ValuerAgent(api_key, max_tokens)
        self.exploration_const = c
        self.lastNodeId = 0
        self.base_history: List[Dict[str, str]] = base_history

    def search(self, iterations):
        for _ in range(iterations):
            node = self.select(self.root)
            child = self.expand(node)
            value = parse_response(self.rollout(child))
            print("Rating of the message: " + str(value))

            child.update(value["score"])

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
                candidates = self.MessagesCreationAgent.get_client_messages(node.history, self.k)
                for candidate in candidates:
                    new_child_nodes.append(node.add_child(parse_response(candidate), self.lastNodeId))
                    self.lastNodeId += 1

        return random.choice(new_child_nodes) if new_child_nodes else node


    def select(self, node):
        while not node.is_leaf() and node.is_fully_expanded(self.k):
            node = max(node.children, key=lambda n: n.uct_score(self.exploration_const))

        print("[Tree Select Action] Selected node_id=" + str(node.node_id) + " with uct_score=" + str(node.uct_score(self.exploration_const)))
        return node

    def rollout(self, node):
        agent_msg = parse_response(self.MessagesCreationAgent.get_partner_messages(node.history, k=1)[0])

        node.history.append(agent_msg)

        print("Rollout virtual history: " + str(node.history))

        return self.ValuerAgent.value(node.history)

    def traverse(self):
        self.root.traverse()