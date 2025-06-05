import math

class Selector:
    """
    Class which provides PUCT scoring functionality to select between exploitation & exploration
    """

    @staticmethod
    def puct_score(q: float,
                   p: float,
                   n: float,
                   parent_n: float,
                   cp: float = 1.0) -> float:
        """
        :param cp: exploration–exploitation trade-off constant
        :param q: reward for the move
        :param p: reward for the action
        :param n: count of visits of the child
        :param parent_n: count of visits of the parent
        :return: puct scoring;
        """

        return q + cp * (p * math.sqrt(parent_n) / (1 + n))