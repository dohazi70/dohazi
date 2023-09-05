import maya.cmds as cmds
from PySide2 import QtWidgets

class SearchAndPathDialog(QtWidgets.QDialog):
    def __init__(self):
        super(SearchAndPathDialog, self).__init__()

        self.setWindowTitle("Search Text and Directory Path")
        self.setMinimumWidth(400)

        layout = QtWidgets.QVBoxLayout()

        search_layout = QtWidgets.QHBoxLayout()
        search_label = QtWidgets.QLabel("Enter search text:")
        self.search_line_edit = QtWidgets.QLineEdit()
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_line_edit)
        layout.addLayout(search_layout)

        path_layout = QtWidgets.QHBoxLayout()
        path_label = QtWidgets.QLabel("Enter directory path:")
        self.path_line_edit = QtWidgets.QLineEdit()
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_line_edit)
        layout.addLayout(path_layout)

        button = QtWidgets.QPushButton("OK")
        button.clicked.connect(self.on_ok_button_clicked)
        layout.addWidget(button)

        self.setLayout(layout)

    def on_ok_button_clicked(self):
        search_text = self.search_line_edit.text()
        directory_path = self.path_line_edit.text()
        self.accept()

def get_user_input():
    dialog = SearchAndPathDialog()
    result = dialog.exec_()

    if result == QtWidgets.QDialog.Accepted:
        search_text = dialog.search_line_edit.text()
        directory_path = dialog.path_line_edit.text()
        return search_text, directory_path
    else:
        return None, None

search_text, directory_path = get_user_input()

def import_abc_files_in_directory(directory_path, search_text):
    abc_cache_nodes = []
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".abc") and search_text in file:
                abc_file_path = os.path.join(root, file)
                print(f"Importing ABC file: {abc_file_path}")
                
                cmds.AbcImport(abc_file_path, mode="import")
                
                abc_cache_nodes.append(file)
    
    return abc_cache_nodes

def pad_numbers(text):
    import re
    def replace(match):
        number = match.group(0)
        return f'{int(number):02d}'
    return re.sub(r'\d+', replace, text)

def select_nodes_with_error(node_names):
    selected_nodes = []
    for node_name in node_names:
        try:
            cmds.select(node_name, add=True)
            selected_nodes.append(node_name)
        except:
            corrected_node_name = "|" + node_name
            try:
                cmds.select(corrected_node_name, add=True)
                selected_nodes.append(corrected_node_name)
            except:
                cmds.warning(f"Unable to select node: {node_name}")
    
    return selected_nodes

if search_text is not None and directory_path is not None:
    gpu_cache_nodes = cmds.ls(type="gpuCache")
    abc_cache_nodes = import_abc_files_in_directory(directory_path, search_text)
    print(f"Found ABC Cache Nodes: {abc_cache_nodes}")
    
    selected_gpu_cache_nodes = [pad_numbers(node) for node in gpu_cache_nodes if search_text in node]
    selected_abc_cache_nodes = [pad_numbers(node) for node in abc_cache_nodes if search_text in node]

    selected_gpu_cache_nodes = [node.replace("Shape", "") for node in selected_gpu_cache_nodes]
    print(selected_gpu_cache_nodes)
    selected_abc_cache_nodes = [node.replace("Shape", "").replace(".abc", "") for node in selected_abc_cache_nodes]
    print(selected_abc_cache_nodes)
    
    cmds.select(selected_gpu_cache_nodes)
    selected_nodes = select_nodes_with_error(selected_abc_cache_nodes)
    
    cmds.ReplaceObjects()