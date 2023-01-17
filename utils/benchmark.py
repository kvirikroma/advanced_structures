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


def get_args(branching_probability: float = None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--iterations", help="Number of iterations", type=positive_int, required=True)
    parser.add_argument("-c", "--count", help="Count of items to work on", type=positive_int, required=True)
    if branching_probability is not None:
        parser.add_argument(
            "-b", "--branching_probability",
            help="Probability of making an attempt to create a new branch while appending an item",
            type=float_01, required=False, default=branching_probability
        )
    parser.add_argument(
        "-p", "--print",
        help="Print a structure that was built (only for cases when '--iterations' is 1)",
        required=False, action=argparse.BooleanOptionalAction, default=False
    )
    args = parser.parse_args()
    if args.print and args.iterations != 1:
        raise ValueError("Cannot print tree when '--iterations' is other than 1")
