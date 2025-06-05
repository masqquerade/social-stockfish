from src.mcts.OpenMCTSNode import OpenMCTSNode
from src.Planner.Actions import RomanceAction

class OpenMCTS:
    def __init__(self):
        self.root = None
        self.last_node_id = 0

    def search(self):
        return

    def init_root(self):
        """
        Initialization of the Tree-Root
        """

        self.root = OpenMCTSNode(
            parent=None,
            action=RomanceAction.ROOT_ACTION,
            p=0,
            _id=self.last_node_id
        )

        self.last_node_id += 1
        self.root.N = 1
        self.expand(self.root)
        self.root.N = 0

    def expand(self, node: OpenMCTSNode):
        return
