import argparse
from concurrent.futures import ProcessPoolExecutor
from random import random, choice, randint
from time import time_ns
from typing import Hashable
from ordered_set import OrderedSet

from multi_list import MultiList, MultiListPath


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
    paths = OrderedSet()
    appendable_paths = OrderedSet()
    result = [[], [], [], []]
    for _ in range(items_count):
        full_appending_time_start = time_ns()
        value_to_add = randint(*VALUE_GENERATION_RANGE)
        if paths:
            if random() < branching_probability:
                parent_path = choice((*paths,))
                new_path = MultiListPath((*parent_path, 0))
                if lst.exists(new_path):
                    parent_path = choice((*appendable_paths,))
                    path = MultiListPath((*(parent_path[:-1]), parent_path[-1] + 1))
                    appendable_paths.remove(parent_path)
                else:
                    path = new_path
            else:
                parent_path = choice((*appendable_paths,))
                path = MultiListPath((*(parent_path[:-1]), parent_path[-1] + 1))
                appendable_paths.remove(parent_path)
        else:
            path = MultiListPath('0')
        main_appending_time_start = time_ns()
        lst.append(value_to_add, path)
        result[0].append(time_ns() - main_appending_time_start)
        paths.add(HashablePath((*path, )))
        appendable_paths.add(HashablePath((*path, )))
        result[1].append(time_ns() - full_appending_time_start)
    if print_tree:
        lst.print_all()
    for path in paths:
        searching_time_start = time_ns()
        lst.find(path)
        result[2].append(time_ns() - searching_time_start)
    for path in paths[::-1]:
        deleting_time_start = time_ns()
        lst.delete(path)
        result[3].append(time_ns() - deleting_time_start)
    return *result,


def main():
    def positive_int(value):
        try:
            int_value = int(value)
            if int_value <= 0:
                raise ValueError
        except ValueError:
            raise argparse.ArgumentTypeError(f"{value} is an invalid positive int value")
        return int_value
        
    def float_01(value):
        try:
            value = float(value)
            if value < 0:
                raise ValueError
            if value > 1:
                raise ValueError
        except ValueError:
            raise argparse.ArgumentTypeError(f"{value} is an invalid value (should be between 0 and 1)")
        return value

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--iterations", help="Number of iterations", type=positive_int, required=True)
    parser.add_argument("-c", "--count", help="Count of items to work on", type=positive_int, required=True)
    parser.add_argument(
        "-b", "--branching_probability",
        help="Probability of making an attempt to create a new branch while appending an item",
        type=float_01, required=False, default=DEFAULT_BRANCHING_PROBABILITY
    )
    parser.add_argument(
        "-p", "--print",
        help="Print a tree that was built (only for cases when '--iterations' is 1)",
        required=False, action=argparse.BooleanOptionalAction, default=False
    )
    args = parser.parse_args()
    if args.print and args.iterations != 1:
        raise ValueError("Cannot print tree when '--iterations' is other than 1")
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
