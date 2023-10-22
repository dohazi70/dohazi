class TodoView:
    def show_todos(self, todos):
        for index, todo in enumerate(todos):
            print(f"{index + 1}. {todo}")

    def get_user_input(self):
        return input("할 일을 입력하세요: ")