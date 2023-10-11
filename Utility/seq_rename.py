import os
from PySide2 import QtWidgets, QtGui, QtCore

def update_new_name():
    input_path = find_line.text()
    parts = input_path.split("\\")
    desired_part = "\\".join(parts[-3:])
    master_path = desired_part.replace("\\", "_")

    selected_option = option_combo.currentIndex()
    
    if selected_option == 0:
        prefix = master_path + "_" + "2K" + "_"
        print(selected_option)
    else:
        prefix = master_path + "_" + "4K" + "_"
        print(selected_option)
    
    
    file_list = os.listdir(input_path)
    
    if file_list:
        file_name = file_list[0]
        file_name_path = file_name.split("_")
        file_desired_path = "_".join(file_name_path[-1:])
        new_file_name = f"{prefix}{file_desired_path}"
        new_name_label.setText(f"New file name:\n{new_file_name}")
    else:
        new_name_label.setText("No files found in the specified directory.")

def replace():
    input_path = find_line.text()
    parts = input_path.split("\\")
    desired_part = "\\".join(parts[-3:])
    master_path = desired_part.replace("\\", "_")

    file_list = os.listdir(input_path)

    selected_option = option_combo.currentIndex()

    if selected_option == 0:
        prefix = master_path + "_" + "2K" + "_"
        print(selected_option)
    else:
        prefix = master_path + "_" + "4K" + "_"
        print(selected_option)

    for file_name in file_list:
        file_path = os.path.join(input_path, file_name)
        file_name_path = file_name.split("_")
        file_desired_path = "_".join(file_name_path[-1:])
        
        new_file_name = f"{prefix}{file_desired_path}"
        new_file_name_path = os.path.join(input_path, new_file_name)
        os.rename(file_path, new_file_name_path) 


app = QtWidgets.QApplication.instance()
if not app:
    app = QtWidgets.QApplication([])


window = QtWidgets.QWidget()
window.setWindowTitle("File Name Replacement")
window.setMinimumWidth(400)

layout = QtWidgets.QVBoxLayout()

find_layout = QtWidgets.QHBoxLayout()
find_label = QtWidgets.QLabel("File path:")
find_layout.addWidget(find_label)
find_line = QtWidgets.QLineEdit()
find_layout.addWidget(find_line)
layout.addLayout(find_layout)

option_layout = QtWidgets.QHBoxLayout()
option_label = QtWidgets.QLabel("Option:")
option_layout.addWidget(option_label)
option_combo = QtWidgets.QComboBox()
option_combo.addItems(["2K", "4K"])
option_layout.addWidget(option_combo)
layout.addLayout(option_layout)

new_name_label = QtWidgets.QLabel("")
layout.addWidget(new_name_label)

replace_button = QtWidgets.QPushButton("Replace")
replace_button.clicked.connect(replace)
layout.addWidget(replace_button)

window.setLayout(layout)
window.show()

# text updata
find_line.textChanged.connect(update_new_name)
option_combo.currentTextChanged.connect(update_new_name)


app.exec_()
