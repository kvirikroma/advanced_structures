from skip_list import SkipList
from utils.cli import CommandInterface


class SkipListCommandInterface(CommandInterface):
    def __init__(self):
        super().__init__()
        self.lst: SkipList = SkipList()
        self.lst_copy: SkipList | None = None
        self.commands = {
            "type": self.control_item_type,
            "help": self.help,
            "size": self.get_size,
            "levels": self.get_levels_count,
            "print": self.print_all,
            "add": self.add_item,
            "delete": self.delete_item,
            "present": self.is_present,
            "from-sequence": self.from_sequence,
            "copy": lambda action: self.copy(action, 'copy'),
            "clear": self.clear
        }

    @staticmethod
    def help():
        print(
            "Commands:\n"
            "help - show this help message\n"
            "type get|set [int|str|float] - get current item type or change it and \n"
            "size - print count of items in the whole skip-list\n"
            "levels - print count of levels in the skip-list\n"
            "print - print the whole skip-list\n"
            "add VALUE - append the VALUE\n"
            "delete VALUE - delete the VALUE\n"
            "present VALUE - check if the VALUE present in the skip-list\n"
            "from-sequence SEQUENCE [as-tree] - fill the skip-list from the given SEQUENCE of values. "
            "The SEQUENCE must contain values separated by commas, without spaces (like that: -1,2,-4,8,0). "
            "The as-tree parameter is optional and if it is specified, the levels will be generated not randomly, "
            "but as a levels of a balanced binary tree.\n"
            "copy make|restore|switch|delete - control the copy of list\n"
            "clear - clear the skip-list\n"
        )

    def control_item_type(self, action: str, item_type: str = None):
        if super().control_item_type(action, item_type) and action == "set":
            self.clear()

    def get_size(self):
        print(f"Size: {len(self.lst)}")

    def get_levels_count(self):
        print(f"Levels: {self.lst.levels}")

    def print_all(self):
        self.lst.print()

    def clear(self):
        self.lst.clear()

    def is_present(self, value: str | int | float):
        try:
            value = self.item_type(value)
        except ValueError:
            return print("Error: invalid item type")
        print(f"The value {repr(value)} is {'not ' * (not self.lst.present(value))}present")

    def add_item(self, value: str | int | float):
        try:
            value = self.item_type(value)
        except ValueError:
            return print("Error: invalid item type")
        try:
            self.lst.append(value)
        except ValueError as err:
            return print(f"Error: {err.args[0]}")

    def delete_item(self, value: str | int | float):
        try:
            value = self.item_type(value)
        except ValueError:
            return print("Error: invalid item type")
        try:
            self.lst.delete(value)
        except ValueError as err:
            return print(f"Error: {err.args[0]}")

    def from_sequence(self, sequence=None, as_tree=None):
        if not sequence or as_tree not in ('as-tree', None):
            return print("Invalid parameters")
        try:
            sequence = [self.item_type(item) for item in sequence.split(',')]
        except ValueError:
            return print("Invalid sequence given (maybe wrong item type?)")
        try:
            self.lst.from_iterable(sequence, tree_like=bool(as_tree))
        except ValueError as err:
            return print(f"Error: {err.args[0]}")


if __name__ == "__main__":
    try:
        SkipListCommandInterface()()
    except (KeyboardInterrupt, EOFError):
        print("\nExit")
