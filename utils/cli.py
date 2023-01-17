from typing import Any


class CommandInterface:
    def __init__(self):
        self.item_type: type = str
        self.lst: Any | None = None
        self.lst_copy: Any | None = None
        self.commands = {}

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
        pass

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

    def copy(self, action: str, copy_method_name: str):
        if action == "make":
            self.lst_copy = getattr(self.lst, copy_method_name)()
        elif action == "restore":
            if self.lst_copy is None:
                return print("No copy available, nothing to restore")
            self.lst = getattr(self.lst_copy, copy_method_name)()
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
