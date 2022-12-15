from multi_list import MultiList, MultiListPath


class MultiListCommandInterface:
    def __init__(self):
        self.lst = MultiList()
        self.lst_copy = None
        self.path_separator = MultiListPath('').separator
        self.item_type = str
        self.commands = {
            "type": self.item_type,
            "separator": self.control_path_separator,
            "help": self.help,
            "size": self.get_size,
            "levels": self.get_levels_count,
            "print": self.print_all,
            "add": self.add_item,
            "delete": self.delete_item,
            "delete-level": self.delete_level,
            "delete-branch": self.delete_branch,
            "copy": self.copy,
            "clear": self.clear
        }

    def __call__(self):
        while True:
            print(">> ", end='')
            command = [i for i in input().split() if i]
            if not command:
                continue
            if command[0] not in self.commands:
                print(f"Unrecognized command '{command[0]}'")
                print("Enter 'help' for more information")
            try:
                self.commands[command[0]](command[1:])
            except TypeError:
                print("Invalid parameters")

    @staticmethod
    def help():
        print(
            "Commands:\n"
            "help - show this help message\n"
            "type get|set [int|str|float] - get current item type or change it\n"
            "separator get|set [SYMBOL] - get or change the separator for item paths (SYMBOL is 1-character string)\n"
            "size - print count of items in the whole multi-list\n"
            "levels - print count of levels in the multi-list\n"
            "print - print the whole multi-list\n"
            "add VALUE PATH - append given VALUE at the given PATH\n"
            "delete PATH - delete item which is located at PATH\n"
            "delete-level LEVEL - delete the level number LEVEL and everything under it\n"
            "delete-branch PATH - delete branch of multi-list, which parent is at PATH\n"
            "copy make|restore|switch|delete - control the copy of list\n"
            "clear - clear the multi-list\n"
        )

    def item_type(self, action: str, item_type: str = None):
        pass

    def control_path_separator(self, action: str, separator: str = None):
        pass

    def get_size(self):
        pass

    def get_levels_count(self):
        pass

    def print_all(self):
        pass

    def add_item(self, path: str, item: str | int):
        pass

    def move_item(self, source_path: str, destination_path: str):
        pass

    def delete_item(self, path: str):
        pass

    def delete_level(self, level_number: str | int):
        pass

    def delete_branch(self, path: str):
        pass

    def copy(self, action: str):
        pass

    def clear(self):
        self.lst.clear()


if __name__ == "__main__":
    try:
        MultiListCommandInterface()()
    except (KeyboardInterrupt, EOFError):
        print("\nExit")
