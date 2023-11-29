class TodoModel:
    def __init__(self):
        self.todos = []

    def add_todo(self, task):
        self.todos.append(task)

    def get_todos(self):
        return self.todos