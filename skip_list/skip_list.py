from typing import List, Callable, Iterable, Tuple
from math import log2
from random import randint


class SkipListNode:
    def __init__(self, value, levels: int):
        self.value = value
        self.right: List[SkipListNode | None] = [None for _ in range(levels)]

    def __repr__(self):
        return f"SkipListNode(value={self.value}, levels={len(self.right)}"


class SkipList:
    def __init__(self, max_level: Callable[[int], int] | int | None = None):
        self.count = 0
        self.root: List[SkipListNode] = []
        self.max_level = max_level if max_level else lambda count: (log2(count) // 1 if self.count >= 2 else 1)

    def _generate_levels_count_randomly(self) -> int:
        max_level = self.max_level if isinstance(self.max_level, int) else self.max_level(self.count)
        min_level = 1
        result = max_level - int(log2(randint(2 ** min_level, (2 ** (max_level + 1)) - 1)) // 1) + min_level
        return min(result, len(self.root) + 1)

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

    def _find_previous_node(self, value) -> Tuple[SkipListNode, List[SkipListNode | None]] | None:
        if not self.root:
            return None
        node = self.root[-1]
        left_connections = [None for _ in self.root]
        for level in reversed(range(len(self.root))):
            while True:
                if node.value >= value:
                    return None
                if node.value < value:
                    if not node.right[level]:
                        left_connections[level] = node
                        break
                    if node.right[level].value >= value:
                        left_connections[level] = node
                        break
                    node = node.right[level]
        return node, left_connections

    def from_iterable(self, source: Iterable, tree_like: bool = False):
        pass

    def append(self, value):
        prev_node_search = self._find_previous_node(value)
        new_node = SkipListNode(value, self._generate_levels_count_randomly())
        if prev_node_search:
            prev_node, connections = prev_node_search
            prev_node_right = prev_node.right
        else:
            prev_node_right = connections = self.root
        if prev_node_right[0] and prev_node_right[0].value == value:
            raise ValueError("This value already exists in the list")
        for level in range(len(new_node.right)):
            new_node.right[level] = connections[level]
            if len(connections) <= level:
                self.root.append(new_node)
            elif connections[level]:
                connections[level].right[level] = new_node
        self.count += 1

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
            destination_node.right[0] = SkipListNode(source_node.value, len(source_node.right))
            destination_node = destination_node.right[0]
            true_max_level = max(true_max_level, len(source_node.right))
        result.root = [None for _ in range(len(self.root))]
        last_node_on_level: List[SkipListNode | None] = [None for _ in range(true_max_level)]
        node = start_node
        while node := node.right[0]:
            for level in range(len(node.right)):
                if last_node_on_level[level]:
                    last_node_on_level[level].right[level] = node
                if not result.root[level]:
                    result.root[level] = node
                last_node_on_level[level] = node
        return result

    def clear(self):
        self.__init__(self.max_level)
