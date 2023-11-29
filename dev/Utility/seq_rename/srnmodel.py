import os

class FileRenamerModel:
    def __init__(self):
        self.input_path = ""
        self.selected_option = 0

    def set_input_path(self, path):
        self.input_path = path

    def set_selected_option(self, option):
        self.selected_option = option

    def get_file_list(self):
        return os.listdir(self.input_path)

    def generate_new_file_name(self, file_name):
        parts = self.input_path.split("\\")
        desired_part = "\\".join(parts[-3:])
        master_path = desired_part.replace("\\", "_")
        
        if self.selected_option == 0:
            prefix = master_path + "_" + "2K" + "_"
        else:
            prefix = master_path + "_" + "4K" + "_"
        
        file_name_path = file_name.split("_")
        file_desired_path = "_".join(file_name_path[-1:])
        
        new_file_name = f"{prefix}{file_desired_path}"
        return new_file_name
