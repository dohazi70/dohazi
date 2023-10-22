from Model import TodoModel
from View import TodoView

class TodoController:
    def __init__(self):
        self.model = TodoModel()
        self.view = TodoView()

    def run(self):
        while True:
            self.view.show_todos(self.model.get_todos())
            user_input = self.view.get_user_input()
            self.model.add_todo(user_input)