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

    def iterate(self, include_all_levels: bool = True):
        iteration_item = self.root
        while iteration_item:
            yield iteration_item
            if include_all_levels and iteration_item.child:
                yield from iteration_item.child.iterate(True)
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
            for item in current_list.iterate(include_all_levels=False):
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

    def append(self, value, path: MultiListPath):
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
                    parent_node.child.root = MultiListNode(value, right=node)
                else:
                    for _ in range(path[-1] - 1):
                        node = node.right
                    node.right = MultiListNode(value, right=node.right)
                parent_node.child._items_count += 1
            else:
                if path[-1] != 0:
                    raise LookupError("Path does not exist")
                parent_node.child.root = MultiListNode(value)
                parent_node.child._items_count = 1
        else:
            if path[-1] != 0:
                raise LookupError("Path does not exist")
            parent_node.child = MultiList()
            parent_node.child.root = MultiListNode(value)
            parent_node.child._items_count = 1

    def delete(self, path: MultiListPath):
        pass

    def get_items_count(self, include_all_levels: bool = True) -> int:
        if include_all_levels:
            return sum(bool(i) for i in self.iterate(include_all_levels=True))
        else:
            return self._items_count

    def move_item(self, source_path: MultiListPath, destination_path: MultiListPath):
        pass

    def delete_level(self, level_number: int):
        pass

    def make_full_copy(self):
        pass

    def clear(self):
        self.__init__()
