import os
import sys
from PySide2 import QtWidgets, QtGui, QtCore

class RenameFilesApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Rename Files')
        self.setGeometry(100, 100, 400, 150)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.input_path_label = QLabel('Input Path:')
        self.input_path_edit = QLineEdit()
        self.input_verison_label = QLabel('Input Version:')
        self.input_verison_edit = QLineEdit()

        self.rename_button = QPushButton('Rename Files')
        self.rename_button.clicked.connect(self.rename_files)

        layout.addWidget(self.input_path_label)
        layout.addWidget(self.input_path_edit)
        layout.addWidget(self.input_verison_label)
        layout.addWidget(self.input_verison_edit)
        layout.addWidget(self.rename_button)

        central_widget.setLayout(layout)

    def rename_files(self):
        input_path = self.input_path_edit.text()
        input_verison = self.input_verison_edit.text()

        parts = input_path.split("\\")
        desired_part = "\\".join(parts[-2:])
        master_path = desired_part.replace("\\", "_")

        file_list = os.listdir(input_path)

        prefix = master_path + "_" + input_verison + "_"
        start_number = 0

        for file_name in file_list:
            file_path = os.path.join(input_path, file_name)
            file_extension = os.path.splitext(file_name)[-1]

            new_file_name = f"{prefix}{start_number:03d}{file_extension}"
            new_file_path = os.path.join(input_path, new_file_name)

            os.rename(file_path, new_file_path)
            start_number += 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RenameFilesApp()
    ex.show()
    sys.exit(app.exec_())
