from typing import List, Callable, Iterable
from math import log2
from random import randint


class SkipListNode:
    def __init__(self, value, levels: int):
        self.value = value
        self.right: List[SkipListNode | None] = [None for _ in range(levels)]

    def __repr__(self):
        return f"SkipListNode(value={self.value}, levels={self.levels})"

    @property
    def levels(self):
        return len(self.right)


class SkipList:
    def __init__(self, max_level: Callable[[int], int] | int | None = None):
        self.count = 0
        self.root = SkipListNode(None, 0)
        self.max_level = max_level if max_level else lambda count: (log2(count) // 1 if count >= 2 else 1)

    def _generate_levels_count_randomly(self) -> int:
        max_level = self.max_level if isinstance(self.max_level, int) else int(self.max_level(self.count))
        min_level = 1
        result = int(max_level - int(log2(randint(2 ** min_level, (2 ** (max_level + 1)) - 1)) // 1) + min_level)
        return min(result, self.root.levels + 1)

    @property
    def levels(self):
        return self.root.levels

    def from_iterable(self, source: Iterable, tree_like: bool = False):
        if tree_like:
            sorted_data = [[i, None] for i in sorted(source)]

            def mark_levels(data: List[List], level: int):
                if not data:
                    return
                if len(data) == 1:
                    data[0][1] = level
                    return
                left = data[:len(data) // 2]
                right = data[len(data) // 2 + 1:]
                data[len(data) // 2][1] = level
                mark_levels(left, max(level - 1, 0))
                mark_levels(right, max(level - 1, 0))

            mark_levels(
                sorted_data,
                self.max_level if isinstance(self.max_level, int) else int(
                    self.max_level(self.count + (len(sorted_data) // 1.5))
                )
            )
            for value, lvl in sorted_data:
                self._append(value, lvl)
        else:
            for i in source:
                self.append(i)

    def _append(self, value, level: int | None = None):
        node = SkipListNode(value, level + 1 if level is not None else self._generate_levels_count_randomly())
        current = self.root
        if self.root.levels < node.levels:
            self.root.right.append(None)
        update: List[SkipListNode | None] = [None for _ in range(self.levels)]
        for i in range(self.levels - 1, -1, -1):
            while current.right[i] and current.right[i].value < value:
                current = current.right[i]
            update[i] = current
        current = current.right[0]
        if current is not None and current.value == value:
            raise ValueError("This value already exists in the list")
        if node.levels >= self.levels:
            for i in range(self.levels, node.levels):
                update[i] = self.root
        for i in range(node.levels):
            node.right[i] = update[i].right[i]
            update[i].right[i] = node
        self.count += 1

    def append(self, value):
        self._append(value)

    def _iterate(self, include_levels: bool = False, get_raw_nodes: bool = False):
        if not self.root:
            return
        node = self.root.right[0]
        while node:
            yield node if get_raw_nodes else ((node.value, len(node.right)) if include_levels else node.value)
            node = node.right[0]

    def __iter__(self):
        return self._iterate()

    def print(self):
        levels = [[] for _ in self.root.right]
        for node in self._iterate(get_raw_nodes=True):
            for level in range(node.levels):
                levels[level].append(f'"{node.value}"' if isinstance(node.value, str) else str(node.value))
        for level in range(len(levels)):
            print(f"Level {level}:", ", ".join(levels[level]))

    def delete(self, value):
        update: List[SkipListNode | None] = [None for _ in range(self.levels)]
        current = self.root
        for i in range(self.levels - 1, -1, -1):
            while current.right[i] and current.right[i].value < value:
                current = current.right[i]
            update[i] = current
        current = current.right[0]
        if current is None or current.value != value:
            raise ValueError("This value does not exist in the list")
        for i in range(self.levels):
            if update[i].right[i] != current:
                break
            update[i].right[i] = current.right[i]
        while self.root and self.root.right[-1] is None:
            del self.root.right[-1]
        self.count -= 1

    def present(self, value) -> bool:
        current = self.root
        for i in range(self.levels - 1, -1, -1):
            while current.right[i] and current.right[i].value < value:
                current = current.right[i]
        current = current.right[0]
        return current and current.value == value

    def copy(self) -> "SkipList":
        result = SkipList(self.max_level)
        result.count = self.count
        source_node = SkipListNode(None, 1)
        source_node.right[0] = self.root.right[0] if self.root.right else None
        destination_node = start_node = SkipListNode(None, 1)
        destination_node.right[0] = None
        true_max_level = 1
        while source_node := source_node.right[0]:
            destination_node.right[0] = SkipListNode(source_node.value, len(source_node.right))
            destination_node = destination_node.right[0]
            true_max_level = max(true_max_level, len(source_node.right))
        result.root = SkipListNode(None, self.levels)
        last_node_on_level: List[SkipListNode | None] = [None for _ in range(true_max_level)]
        node = start_node
        while node := node.right[0]:
            for level in range(len(node.right)):
                if last_node_on_level[level]:
                    last_node_on_level[level].right[level] = node
                if not result.root.right[level]:
                    result.root.right[level] = node
                last_node_on_level[level] = node
        return result

    def clear(self):
        self.__init__(self.max_level)
