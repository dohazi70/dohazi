from PySide2 import QtWidgets

class FileRenamerView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Name Replacement")
        self.setMinimumWidth(400)

        self.layout = QtWidgets.QVBoxLayout()

        find_layout = QtWidgets.QHBoxLayout()
        self.find_label = QtWidgets.QLabel("File path:")
        find_layout.addWidget(self.find_label)
        self.find_line = QtWidgets.QLineEdit()
        find_layout.addWidget(self.find_line)
        self.layout.addLayout(find_layout)

        option_layout = QtWidgets.QHBoxLayout()
        self.option_label = QtWidgets.QLabel("Option:")
        option_layout.addWidget(self.option_label)
        self.option_combo = QtWidgets.QComboBox()
        self.option_combo.addItems(["2K", "4K"])
        option_layout.addWidget(self.option_combo)
        self.layout.addLayout(option_layout)

        self.new_name_label = QtWidgets.QLabel("")
        self.layout.addWidget(self.new_name_label)

        self.replace_button = QtWidgets.QPushButton("Replace")
        self.layout.addWidget(self.replace_button)
