import os
from PySide2 import QtCore

class FileRenamerController(QtCore.QObject):
    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view

        self.view.find_line.textChanged.connect(self.update_new_name)
        self.view.option_combo.currentTextChanged.connect(self.update_new_name)
        self.view.replace_button.clicked.connect(self.replace)

    def update_new_name(self):
        path = self.view.find_line.text()
        option = self.view.option_combo.currentIndex()
        self.model.set_input_path(path)
        self.model.set_selected_option(option)
        
        file_list = self.model.get_file_list()
        
        if file_list:
            file_name = file_list[0]
            new_file_name = self.model.generate_new_file_name(file_name)
            self.view.new_name_label.setText(f"New file name:\n{new_file_name}")
        else:
            self.view.new_name_label.setText("No files found in the specified directory.")

    def replace(self):
        file_list = self.model.get_file_list()
        for file_name in file_list:
            new_file_name = self.model.generate_new_file_name(file_name)
            file_path = os.path.join(self.model.input_path, file_name)
            new_file_name_path = os.path.join(self.model.input_path, new_file_name)
            os.rename(file_path, new_file_name_path)
