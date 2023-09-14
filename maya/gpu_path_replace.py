import maya.cmds as cmds
from PySide2 import QtWidgets, QtGui, QtCore

def replace_cache_paths():
    all_node = cmds.ls()
    find_text = find_line.text()
    replace_text = replace_line.text()
    
    for node in all_node:
        if cmds.nodeType(node) == "gpuCache":
            cache_path = cmds.getAttr(node + ".cacheFileName")
            modified_path = cache_path.replace(find_text, replace_text)
            cmds.setAttr(node + ".cacheFileName", modified_path, type="string")

# Qt 어플리케이션 생성
app = QtWidgets.QApplication.instance()
if not app:
    app = QtWidgets.QApplication([])

window = QtWidgets.QWidget()
window.setWindowTitle("GPU Cache Path Replacer")
window.setMinimumWidth(400)

layout = QtWidgets.QVBoxLayout()

find_layout = QtWidgets.QHBoxLayout()
find_label = QtWidgets.QLabel("Find:")
find_layout.addWidget(find_label)
find_line = QtWidgets.QLineEdit()
find_layout.addWidget(find_line)
layout.addLayout(find_layout)

replace_layout = QtWidgets.QHBoxLayout()
replace_label = QtWidgets.QLabel("Replace:")
replace_layout.addWidget(replace_label)
replace_line = QtWidgets.QLineEdit()
replace_layout.addWidget(replace_line)
layout.addLayout(replace_layout)

button = QtWidgets.QPushButton("Replace")
button.clicked.connect(replace_cache_paths)
layout.addWidget(button)

window.setLayout(layout)
window.show()
