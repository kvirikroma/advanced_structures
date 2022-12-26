from multi_list import MultiList, MultiListPath


class MultiListCommandInterface:
    def __init__(self):
        self.lst: MultiList = MultiList()
        self.lst_copy: MultiList | None = None
        self.path_separator: str = MultiListPath('').separator
        self.item_type: type = str
        self.commands = {
            "type": self.control_item_type,
            "separator": self.control_path_separator,
            "help": self.help,
            "size": self.get_size,
            "levels": self.get_levels_count,
            "print": self.print_all,
            "add": self.add_item,
            "move": self.move_item,
            "swap": self.swap_items,
            "get": self.get_item,
            "set": self.set_item,
            "delete": self.delete_item,
            "delete-level": self.delete_level,
            "delete-branch": self.delete_branch,
            "copy": self.copy,
            "clear": self.clear
        }

    def __call__(self):
        while True:
            try:
                command = [i for i in input(">> ").split() if i]
            except KeyboardInterrupt:
                print()
                continue
            if not command:
                continue
            if command[0] not in self.commands:
                print(f"Unrecognized command '{command[0]}'")
                print("Enter 'help' for more information")
                continue
            try:
                self.commands[command[0]](*command[1:])
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
            "move PATH1 PATH2 - delete item from PATH1 and then insert it (with child if it's present)"
            "into PATH2 in updated structure\n"
            "swap PATH1 PATH2 - swap items on PATH1 and PATH2 along with their children\n"
            "get PATH - get value in PATH\n"
            "set VALUE PATH - set VALUE to existing node in PATH\n"
            "delete PATH - delete item which is located at PATH\n"
            "delete-level LEVEL - delete the level number LEVEL and everything under it\n"
            "delete-branch PATH - delete branch of multi-list, which parent is at PATH\n"
            "copy make|restore|switch|delete - control the copy of list\n"
            "clear - clear the multi-list\n"
        )

    def control_item_type(self, action: str, item_type: str = None):
        if action == 'get':
            print(self.item_type)
        elif action == 'set':
            if item_type == 'int':
                self.item_type = int
            elif item_type == 'str':
                self.item_type = str
            elif item_type == 'float':
                self.item_type = float
            else:
                print("Error: type should be in [int, str, float]")
        else:
            print("Invalid action type: must be 'get' or 'set'")

    def control_path_separator(self, action: str, separator: str = None):
        if action == 'get':
            print(self.path_separator)
        elif action == 'set':
            if isinstance(separator, str) and len(separator) == 1:
                self.path_separator = separator
            else:
                print("Error: separator must be specified and be 1-character string")
        else:
            print("Invalid action type: must be 'get' or 'set'")

    def get_size(self):
        print(f"Size: {self.lst.get_items_count(include_all_levels=True)}")

    def get_levels_count(self):
        print(f"Levels: {self.lst.deepest_level_number() + 1}")

    def print_all(self):
        self.lst.print_all(path_separator=self.path_separator, highlight_string_values=True)

    def add_item(self, value: str | int | float, path: str):
        try:
            path = MultiListPath(path, separator=self.path_separator)
        except ValueError:
            return print("Error: invalid path (maybe wrong separator?)")
        try:
            value = self.item_type(value)
        except ValueError:
            return print("Error: invalid item type")
        try:
            self.lst.append(value, path)
        except (LookupError, AssertionError) as err:
            return print(f"Error: {err.args[0]}")

    def move_item(self, source_path: str, destination_path: str):
        try:
            source_path = MultiListPath(source_path, separator=self.path_separator)
            destination_path = MultiListPath(destination_path, separator=self.path_separator)
        except ValueError:
            return print("Error: invalid path (maybe wrong separator?)")
        try:
            self.lst.move(source_path, destination_path)
        except (ValueError, LookupError, AssertionError) as err:
            return print(f"Error: {err.args[0]}")

    def swap_items(self, path1: str, path2: str):
        try:
            path1 = MultiListPath(path1, separator=self.path_separator)
            path2 = MultiListPath(path2, separator=self.path_separator)
        except ValueError:
            return print("Error: invalid path (maybe wrong separator?)")
        try:
            self.lst.swap(path1, path2)
        except (ValueError, LookupError) as err:
            return print(f"Error: {err.args[0]}")

    def get_item(self, path: str):
        try:
            path = MultiListPath(path, separator=self.path_separator)
        except ValueError:
            return print("Error: invalid path (maybe wrong separator?)")
        try:
            result = self.lst.find(path)
            print(result, f"(type: {type(result).__name__})")
        except LookupError as err:
            return print(f"Error: {err.args[0]}")

    def set_item(self, value: str | int | float, path: str):
        try:
            path = MultiListPath(path, separator=self.path_separator)
        except ValueError:
            return print("Error: invalid path (maybe wrong separator?)")
        try:
            value = self.item_type(value)
        except ValueError:
            return print("Error: invalid item type")
        try:
            self.lst.change_value(value, path)
        except LookupError as err:
            return print(f"Error: {err.args[0]}")

    def delete_item(self, path: str):
        try:
            path = MultiListPath(path, separator=self.path_separator)
        except ValueError:
            return print("Error: invalid path (maybe wrong separator?)")
        try:
            self.lst.delete(path)
        except (LookupError, AssertionError) as err:
            return print(f"Error: {err.args[0]}")

    def delete_level(self, level_number: str | int):
        try:
            level_number = int(level_number)
        except ValueError:
            return print("Invalid level number (must be integer)")
        try:
            self.lst.delete_level(level_number)
        except ValueError as err:
            return print(f"Error: {err.args[0]}")

    def delete_branch(self, path: str):
        try:
            path = MultiListPath(path, separator=self.path_separator)
        except ValueError:
            return print("Error: invalid path (maybe wrong separator?)")
        try:
            self.lst.delete_child(path)
        except LookupError as err:
            return print(f"Error: {err.args[0]}")

    def copy(self, action: str):
        if action == "make":
            self.lst_copy = self.lst.make_full_copy()
        elif action == "restore":
            if self.lst_copy is None:
                return print("No copy available, nothing to restore")
            self.lst = self.lst_copy.make_full_copy()
        elif action == "switch":
            if self.lst_copy is None:
                return print("No copy available, nothing to switch with")
            self.lst, self.lst_copy = self.lst_copy, self.lst
        elif action == "delete":
            if self.lst_copy is None:
                return print("No copy available, nothing to delete")
            self.lst_copy = None
        else:
            print(f"Error: unknown action '{action}'")

    def clear(self):
        self.lst.clear()


if __name__ == "__main__":
    try:
        MultiListCommandInterface()()
    except (KeyboardInterrupt, EOFError):
        print("\nExit")
