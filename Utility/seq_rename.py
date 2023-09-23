import os
from PySide2 import QtWidgets, QtGui, QtCore


def replace():
    input_path = find_line.text()
    parts = input_path.split("\\")
    desired_part = "\\".join(parts[-3:])
    master_path = desired_part.replace("\\", "_")

    file_list = os.listdir(input_path)

    prefix = master_path + "_"

    for file_name in file_list:
        file_path = os.path.join(input_path, file_name)
        file_name_path = file_name.split(".")
        file_desired_path = ".".join(file_name_path[-2:])
        
        new_file_name = f"{prefix}{file_desired_path}"
        new_file_name_path = os.path.join(input_path, new_file_name)
        os.rename(file_path, new_file_name_path) 



#pyside 
app = QtWidgets.QApplication.instance()
if not app:
    app = QtWidgets.QApplication([])

window = QtWidgets.QWidget()
window.setWindowTitle("seq file repalce:")
window.setMinimumWidth(400)

layout = QtWidgets.QVBoxLayout()

find_layout = QtWidgets.QHBoxLayout()
find_label = QtWidgets.QLabel("file path:")
find_layout.addWidget(find_label)
find_line = QtWidgets.QLineEdit()
find_layout.addWidget(find_line)
layout.addLayout(find_layout)

button = QtWidgets.QPushButton("Replace")
button.clicked.connect(replace)
layout.addWidget(button)

window.setLayout(layout)
window.show()

app.exec_()

