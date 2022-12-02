from typing import Optional, Iterable


class MultiListNode:
    def __init__(self, value, right: Optional["MultiListNode"] = None, child: Optional["MultiList"] = None):
        self.value = value
        self.right = right
        self.child = child


class MultiListPath:
    def __init__(self, path_sequence: Iterable[int] | str, separator: str = "/"):
        self.separator = separator
        if isinstance(path_sequence, str):
            self._sequence = tuple(int(i) for i in path_sequence.strip().strip(self.separator).split(self.separator))
        else:
            self._sequence = tuple(path_sequence)

    def __str__(self):
        return str.join(self.separator, (str(i) for i in self._sequence))

    def __len__(self):
        return len(self._sequence)

    def startswith(self, other: "MultiListPath"):
        if len(other) > len(self):
            return False
        for i, j in zip(self._sequence, other._sequence):
            if i != j:
                return False
        return True


class MultiList:
    def __init__(self):
        self.root = None
        self._items_count = 0

    def print_all(self):
        pass

    def find(self, path: MultiListPath) -> MultiListNode:
        pass

    def add(self, node: MultiListNode, path: MultiListPath):
        pass

    def delete(self, path: MultiListPath):
        pass

    def get_items_count(self, include_all_levels: bool = True) -> int:
        pass

    def move_item(self, source_path: MultiListPath, destination_path: MultiListPath):
        pass

    def delete_level(self, level_number: int):
        pass

    def make_full_copy(self):
        pass

    def clear(self):
        self.__init__()
