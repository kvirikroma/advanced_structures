from typing import Optional, Iterable
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
            self._sequence = tuple(int(i) for i in path_sequence.strip().strip(self.separator).split(self.separator))
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
        self._iteration_item: MultiListNode | None = None
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

    def exists(self, path: MultiListPath) -> bool:
        pass

    def find(self, path: MultiListPath) -> MultiListNode:
        pass

    def add(self, node: MultiListNode, path: MultiListPath):
        pass

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
