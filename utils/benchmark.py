import argparse


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


def get_args(additional_functions: list = None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--iterations", help="Number of iterations", type=positive_int, required=True)
    parser.add_argument("-c", "--count", help="Count of items to work on", type=positive_int, required=True)
    parser.add_argument(
        "-p", "--print",
        help="Print a structure that was built (only for cases when '--iterations' is 1)",
        required=False, action=argparse.BooleanOptionalAction, default=False
    )
    if additional_functions:
        for func in additional_functions:
            func(parser)
    args = parser.parse_args()
    if args.print and args.iterations != 1:
        raise ValueError("Cannot print tree when '--iterations' is other than 1")
    return args


def print_results(name, results, only_average: bool = False) -> None:
    average = (sum(results) / len(results)) / 1000
    print(f"{name} time (μs):")
    print("\tAverage:", average)
    if not only_average:
        print("\tMin:", min(results) / 1000)
        print("\tMax:", max(results) / 1000)
        print("\tStandard deviation", (sum((average - (i / 1000)) ** 2 for i in results) / len(results)) ** 0.5)
