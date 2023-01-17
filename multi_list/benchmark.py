from concurrent.futures import ProcessPoolExecutor
from random import random, randint
from time import time_ns
from typing import Hashable

from multi_list import MultiList, MultiListPath
from utils.benchmark import get_args


DEFAULT_BRANCHING_PROBABILITY = 0.1
VALUE_GENERATION_RANGE = (0, 255)
# VALUE_GENERATION_RANGE = (-2147483648, 2147483647)


class HashablePath(MultiListPath, Hashable):
    def __hash__(self):
        return hash(self._sequence) ^ hash(self.separator)

    def __eq__(self, other: "HashablePath"):
        return self._sequence == other._sequence and self.separator == other.separator


def test(items_count: int, print_tree: bool = False, branching_probability: int = DEFAULT_BRANCHING_PROBABILITY):
    lst = MultiList()
    paths = []
    appendable_paths = []
    result = [[], [], [], []]
    for _ in range(items_count):
        full_appending_time_start = time_ns()
        value_to_add = randint(*VALUE_GENERATION_RANGE)
        if paths:
            if random() < branching_probability:
                parent_path = paths[randint(0, len(paths) - 1 if len(paths) > 0 else 0)]
                new_path = MultiListPath((*parent_path, 0))
                if lst.exists(new_path):
                    parent_path_index = randint(0, len(appendable_paths) - 1 if len(appendable_paths) > 0 else 0)
                    parent_path = appendable_paths[parent_path_index]
                    path = MultiListPath((*(parent_path[:-1]), parent_path[-1] + 1))
                    del appendable_paths[parent_path_index]
                else:
                    path = new_path
            else:
                parent_path_index = randint(0, len(appendable_paths) - 1 if len(appendable_paths) > 0 else 0)
                parent_path = appendable_paths[parent_path_index]
                path = MultiListPath((*(parent_path[:-1]), parent_path[-1] + 1))
                del appendable_paths[parent_path_index]
        else:
            path = MultiListPath('0')
        main_appending_time_start = time_ns()
        lst.append(value_to_add, path)
        result[0].append(time_ns() - main_appending_time_start)
        paths.append(HashablePath((*path, )))
        appendable_paths.append(HashablePath((*path, )))
        result[1].append(time_ns() - full_appending_time_start)
    if print_tree:
        lst.print_all()
    for path in paths:
        searching_time_start = time_ns()
        lst.find(path)
        result[2].append(time_ns() - searching_time_start)
    for path in reversed(paths):
        deleting_time_start = time_ns()
        lst.delete(path)
        result[3].append(time_ns() - deleting_time_start)
    return *result,


def main():
    args = get_args(DEFAULT_BRANCHING_PROBABILITY)
    executor = ProcessPoolExecutor()
    addition_time = []
    full_addition_time = []
    search_time = []
    deletion_time = []
    try:
        for addition, full_addition, search, deletion in executor.map(
                test, *zip(*((args.count, args.print, args.branching_probability) for _ in range(args.iterations)))
        ):
            addition_time.extend(addition)
            full_addition_time.extend(full_addition)
            search_time.extend(search)
            deletion_time.extend(deletion)
    finally:
        executor.shutdown(wait=False, cancel_futures=True)
    for name, results in (("Clear addition", addition_time), ("Full addition", full_addition_time),
                          ("Search", search_time), ("Deletion", deletion_time)):
        average = (sum(results) / len(results)) / 1000
        print(f"{name} time (μs):")
        print("\tAverage:", average)
        print("\tMin:", min(results) / 1000)
        print("\tMax:", max(results) / 1000)
        print("\tStandard deviation", (sum((average - (i / 1000)) ** 2 for i in results) / len(results)) ** 0.5)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExit")
