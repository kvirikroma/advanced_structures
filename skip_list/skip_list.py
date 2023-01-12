from typing import List, Callable, Iterable
from math import log2
from random import randint


class SkipListNode:
    def __init__(self, value, levels: int):
        self.value = value
        self.levels = levels
        self.right: List[SkipListNode | None] = [None for _ in range(levels)]

    def __repr__(self):
        return f"SkipListNode(value={self.value}, levels={self.levels}"


class SkipList:
    def __init__(self, max_level: Callable[[int], int] | int | None = None):
        self.count = 0
        self.root = []
        self.max_level = max_level if max_level else lambda count: (log2(count) if self.count >= 2 else 1)

    def _generate_level_randomly(self):
        max_level = self.max_level if isinstance(self.max_level, int) else self.max_level(self.count)
        min_level = 1
        return max_level - (log2(randint(2 ** min_level, (2 ** (max_level + 1)) - 1)) // 1) + min_level

    def _find_node(self, return_previous_if_absent: bool = False) -> SkipListNode | None:
        pass

    def from_iterable(self, source: Iterable, tree_like: bool = False):
        pass

    def append(self, value):
        pass

    def delete(self, value):
        pass

    def present(self, value) -> bool:
        pass

    def copy(self) -> "SkipList":
        result = SkipList(self.max_level)
        result.count = self.count
        source_node = SkipListNode(None, 1)
        source_node.right[0] = self.root[0] if self.root else None
        destination_node = start_node = SkipListNode(None, 1)
        destination_node.right[0] = None
        true_max_level = 1
        while source_node := source_node.right[0]:
            destination_node.right[0] = SkipListNode(source_node.value, source_node.levels)
            destination_node = destination_node.right[0]
            true_max_level = max(true_max_level, source_node.levels)
        result.root = [None for _ in range(len(self.root))]
        last_node_on_level: List[SkipListNode | None] = [None for _ in range(true_max_level)]
        node = start_node
        while node := node.right[0]:
            for level in range(node.levels):
                if last_node_on_level[level]:
                    last_node_on_level[level].right[level] = node
                if not result.root[level]:
                    result.root[level] = node
                last_node_on_level[level] = node
        return result

    def clear(self):
        self.__init__(self.max_level)
