import os
from PySide2 import QtWidgets, QtGui, QtCore


def replace():
    input_path = find_line.text()
    parts = input_path.split("\\")
    desired_part = "\\".join(parts[-3:])
    master_path = desired_part.replace("\\", "_")

    file_list = os.listdir(input_path)
    print(file_list)

    prefix = master_path + "_"
    start_number = 0

    for file_name in file_list:
        file_path = os.path.join(input_path, file_name)
        file_extension = os.path.splitext(file_name)[-1]
        
        new_file_name = f"{prefix}{start_number:04d}{file_extension}"
        new_file_path = os.path.join(input_path, new_file_name)
        
        os.rename(file_path, new_file_path)
        start_number += 1001



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

