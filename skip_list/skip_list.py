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
        self.root: List[SkipListNode] = []
        self.max_level = max_level if max_level else lambda count: (log2(count) if self.count >= 2 else 1)

    def _generate_level_randomly(self):
        max_level = self.max_level if isinstance(self.max_level, int) else self.max_level(self.count)
        min_level = 1
        result = max_level - (log2(randint(2 ** min_level, (2 ** (max_level + 1)) - 1)) // 1) + min_level
        return min(result, len(self.root))

    def _find_node(self, value, return_previous_if_absent: bool = False) -> SkipListNode | None:
        if not self.root:
            return None
        node = self.root[-1]
        for level in reversed(range(len(self.root))):
            while True:
                if node.value > value:
                    return None
                if node.value == value:
                    return node
                if node.value < value:
                    if not node.right[level]:
                        break
                    if node.right[level].value > value:
                        break
                    node = node.right[level]
        if return_previous_if_absent:
            return node

    def _find_previous_node(self, value) -> SkipListNode | None:
        if not self.root:
            return None
        node = self.root[-1]
        for level in reversed(range(len(self.root))):
            while True:
                if node.value >= value:
                    return None
                if node.value < value:
                    if not node.right[level]:
                        break
                    if node.right[level].value >= value:
                        break
                    node = node.right[level]
        return node

    def from_iterable(self, source: Iterable, tree_like: bool = False):
        pass

    def append(self, value):
        pass

    def delete(self, value):
        pass

    def present(self, value) -> bool:
        return self._find_node(value) is not None

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
