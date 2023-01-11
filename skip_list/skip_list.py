from typing import List


class SkipListNode:
    def __init__(self, value, levels: int):
        self.value = value
        self.levels = levels
        self.right: List[SkipListNode | None] = [None for _ in range(levels)]

    def __repr__(self):
        return f"SkipListNode(value={self.value}, levels={self.levels}"


class SkipList:
    pass
