from typing import Optional, Iterable, Union
from collections import deque


class MultiListNode:
    def __init__(self, value, right: Optional["MultiListNode"] = None, child: Optional["MultiList"] = None):
        self.value = value
        self.right = right
        self.child = child

    def __repr__(self):
        return f"MultiListNode(value={self.value}, right={'...' if self.right else 'None'}," \
               f" child={repr(self.child) if self.child else 'None'})"


class MultiListPath:
    def __init__(self, path_sequence: Iterable[int] | str, separator: str = "/"):
        self.separator = separator
        if isinstance(path_sequence, str):
            self._sequence = tuple(
                int(i) for i in path_sequence.strip().strip(self.separator).split(self.separator) if i
            )
        else:
            self._sequence = tuple(path_sequence)

    def __str__(self):
        return str.join(self.separator, (str(i) for i in self._sequence))

    def __repr__(self):
        return f"MultiListPath('{str(self)}')"

    def __len__(self):
        return len(self._sequence)

    def __iter__(self):
        return iter(self._sequence)

    def __getitem__(self, item) -> Union[int, "MultiListPath"]:
        result = self._sequence.__getitem__(item)
        return MultiListPath(result) if isinstance(item, slice) else result

    def __bool__(self):
        return bool(self._sequence)

    def __eq__(self, other: "MultiListPath"):
        return self._sequence == other._sequence

    def startswith(self, other: "MultiListPath"):
        if len(other) > len(self):
            return False
        for i, j in zip(self._sequence, other._sequence):
            if i != j:
                return False
        return True


class MultiList:
    def __init__(self):
        self.root: MultiListNode | None = None
        self._items_count = 0

    def _iterate(self, include_all_levels: bool = True):
        iteration_item = self.root
        while iteration_item:
            yield iteration_item
            if include_all_levels and iteration_item.child:
                yield from iteration_item.child._iterate(True)
            iteration_item = iteration_item.right

    def print_all(self, level: int = 0):
        levels_to_print = deque(((None, self, level), ))
        previous_level = None
        while levels_to_print:
            parent_index, current_list, current_level = levels_to_print.popleft()
            if previous_level != current_level:
                if previous_level is not None:
                    print()
                print(f"Level {current_level}:", end='')
            print(", " if previous_level == current_level else " ", end='')
            if parent_index is not None:
                print(f"{parent_index}:", end='')
            print("[", end='')
            first_printed = False
            index: int | None = 0
            for item in current_list._iterate(include_all_levels=False):
                if first_printed:
                    print(", ", end='')
                print(item.value, end='')
                if item.child:
                    levels_to_print.append((index, item.child, current_level + 1))
                first_printed = True
                index += 1
            previous_level = current_level
            print("]", end='')
        print()

    def _find_node(self, path: MultiListPath) -> MultiListNode | None:
        if not path:
            return None
        node = self.root
        path_part_index = 0
        for index in path:
            assert index >= 0
            for i in range(index):
                if not node:
                    return None
                node = node.right
            if not node:
                return None
            path_part_index += 1
            if path_part_index < len(path):
                node = node.child.root if node.child else None
                if not node:
                    return None
        return node

    def exists(self, path: MultiListPath) -> bool:
        return self._find_node(path) is not None

    def find(self, path: MultiListPath):
        node = self._find_node(path)
        if not node:
            raise LookupError("Path does not exist")
        return node.value

    def _append(self, value, path: MultiListPath) -> MultiListNode:
        assert path[-1] >= 0
        parent_node = MultiListNode(None, None, self) if len(path) == 1 else self._find_node(path[:-1])
        if parent_node is None:
            raise LookupError("Path does not exist")
        if parent_node.child:
            if parent_node.child.root:
                if parent_node.child._items_count < path[-1]:
                    raise LookupError("Path does not exist")
                node = parent_node.child.root
                if path[-1] == 0:
                    result = parent_node.child.root = MultiListNode(value, right=node)
                else:
                    for _ in range(path[-1] - 1):
                        node = node.right
                    result = node.right = MultiListNode(value, right=node.right)
                parent_node.child._items_count += 1
                return result
            else:
                if path[-1] != 0:
                    raise LookupError("Path does not exist")
                parent_node.child.root = MultiListNode(value)
                parent_node.child._items_count = 1
                return parent_node.child.root
        else:
            if path[-1] != 0:
                raise LookupError("Path does not exist")
            parent_node.child = MultiList()
            parent_node.child.root = MultiListNode(value)
            parent_node.child._items_count = 1
            return parent_node.child.root

    def append(self, value, path: MultiListPath):
        self._append(value, path)

    def _delete(self, path: MultiListPath) -> MultiListNode:
        assert path[-1] >= 0
        parent_node = MultiListNode(None, None, self) if len(path) == 1 else self._find_node(path[:-1])
        if parent_node is None or parent_node.child is None or parent_node.child._items_count <= path[-1]:
            raise LookupError("Path does not exist")
        if path[-1] == 0:
            result = parent_node.child.root
            parent_node.child.root = parent_node.child.root.right
        else:
            node = parent_node.child.root
            for _ in range(path[-1] - 1):
                node = node.right
            result = node.right
            node.right = node.right.right
        parent_node.child._items_count -= 1
        if parent_node.child._items_count == 0:
            parent_node.child = None
        return result

    def delete(self, path: MultiListPath):
        self._delete(path)

    def get_items_count(self, include_all_levels: bool = True) -> int:
        if include_all_levels:
            return sum(1 for _ in self._iterate(include_all_levels=True))
        else:
            return self._items_count

    def move(self, source_path: MultiListPath, destination_path: MultiListPath):
        """
        This action completes in 2 steps:
        1. Remove node on source_path
        2. Insert it on destination_path
        Considering that, destination_path should be specified as if source node was already removed.
        This behaviour guarantees that the item that was on source_path before the action
        will appear on destination_path after it
        """
        assert source_path[-1] >= 0 and destination_path[-1] >= 0
        if source_path == destination_path:
            raise ValueError("Source and destination paths cannot be the same")
        if destination_path.startswith(source_path):
            raise ValueError("Such move would create a loop")
        source_node = self._find_node(source_path)
        if not source_node:
            raise LookupError("Source path does not exist")
        self.delete(source_path)
        try:
            result_node = self._append(source_node.value, destination_path)
            result_node.child = source_node.child
        except LookupError:
            result_node = self._append(source_node.value, source_path)
            result_node.child = source_node.child
            raise LookupError("Destination path does not exist")

    def swap(self, path1: MultiListPath, path2: MultiListPath):
        if path1.startswith(path2) or path2.startswith(path1):
            raise ValueError("Such move would create a loop")
        node1 = self._find_node(path1)
        if not node1:
            raise LookupError("path1 does not exist")
        node2 = self._find_node(path2)
        if not node2:
            raise LookupError("path2 does not exist")
        node1.child, node2.child, node1.value, node2.value = node2.child, node1.child, node2.value, node1.value

    def delete_level(self, level_number: int):
        if level_number < 0:
            raise ValueError("Level must be more than 0")
        elif level_number == 0:
            return self.clear()
        for i in self._iterate(include_all_levels=False):
            if i.child is not None:
                if level_number == 1:
                    i.child = None
                else:
                    i.child.delete_level(level_number - 1)

    def make_full_copy(self) -> "MultiList":
        result = MultiList()
        result._items_count = self._items_count
        right_node = None
        for i in self._iterate(include_all_levels=False):
            node_copy = MultiListNode(i.value, None, i.child.make_full_copy() if i.child else None)
            if right_node:
                right_node.right = node_copy
                right_node = node_copy
            else:
                result.root = right_node = node_copy
        return result

    def delete_child(self, path: MultiListPath):
        node = self._find_node(path)
        if not node:
            raise LookupError("Path does not exist")
        node.child = None

    def clear(self):
        self.__init__()
