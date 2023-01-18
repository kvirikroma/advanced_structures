from concurrent.futures import ProcessPoolExecutor
from random import randint
from time import time_ns
from argparse import BooleanOptionalAction

from skip_list import SkipList
from utils.benchmark import get_args, print_results


def test(items_count: int, print_list: bool = False, as_tree: bool = False):
    lst = SkipList()
    items_in_list = set()
    result = [[], [], []]
    if as_tree:
        while len(items_in_list) < items_count:
            items_in_list.add(randint(0, items_count * 10))
        appending_time_start = time_ns()
        lst.from_iterable(items_in_list)
        whole_appending_time = time_ns() - appending_time_start
        result[0] = [whole_appending_time // items_count for _ in range(items_count)]
    else:
        while len(lst) < items_count:
            item = randint(0, items_count * 10)
            try:
                appending_time_start = time_ns()
                lst.append(item)
                result[0].append(time_ns() - appending_time_start)
                items_in_list.add(item)
            except ValueError:
                pass
    if print_list:
        lst.print()
    for item in items_in_list:
        searching_time_start = time_ns()
        lst.present(item)
        result[1].append(time_ns() - searching_time_start)
    for item in items_in_list:
        deleting_time_start = time_ns()
        lst.delete(item)
        result[2].append(time_ns() - deleting_time_start)
    return *result,


def main():
    args = get_args([
        lambda parser: parser.add_argument(
            "-t", "--tree",
            help="Build the list as a binary tree",
            required=False, action=BooleanOptionalAction, default=False
        )
    ])
    executor = ProcessPoolExecutor()
    addition_time = []
    search_time = []
    deletion_time = []
    try:
        for addition, search, deletion in executor.map(
                test, *zip(*((args.count, args.print, args.tree) for _ in range(args.iterations)))
        ):
            addition_time.extend(addition)
            search_time.extend(search)
            deletion_time.extend(deletion)
    finally:
        executor.shutdown(wait=False, cancel_futures=True)
    for name, results in (("Addition", addition_time), ("Search", search_time), ("Deletion", deletion_time)):
        print_results(name, results, only_average=(args.tree and name == "Addition"))


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExit")
