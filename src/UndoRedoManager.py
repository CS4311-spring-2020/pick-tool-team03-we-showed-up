# Tries to follow the commander design pattern
from TableManager import TableManager


class UndoRedoManager:
    def __init__(self, action_list=[], table_manager=None, command_switcher=None):
        self.action_list = action_list
        self.table_manager = table_manager
        self.command_switcher = command_switcher
        self.current_iter = 0

    def undo(self):
        print("undo")
        if self.action_list[self.current_iter][0] == "set_node_field":
            self.command_switcher["set_node_field"](row=self.action_list[self.current_iter][1][0],
                                                    column=self.action_list[self.current_iter][1][1],
                                                    value=self.action_list[self.current_iter][1][2],
                                                    vector_um=self.action_list[self.current_iter][1][3])

    def redo(self):
        print("redo")

    def initialize_command_switcher(self):
        self.command_switcher = {
            "set_node_field": self.table_manager.edit_node_table
        }

    def add_command(self, command_key, args_list):
        self.action_list.append([command_key, args_list])
