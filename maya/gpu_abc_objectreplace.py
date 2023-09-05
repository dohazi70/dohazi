import maya.cmds as cmds
from PySide2 import QtWidgets

def get_user_search_text():
    # 대화 상자 생성
    dialog = QtWidgets.QInputDialog()
    dialog.setWindowTitle("Search Text")
    dialog.setLabelText("Enter search text:")
    dialog.setInputMode(QtWidgets.QInputDialog.TextInput)
    dialog.setTextValue("")

    if dialog.exec_():
        search_text = dialog.textValue()
        return search_text
    else:
        return None

search_text = get_user_search_text()

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

if search_text is not None:
    gpu_cache_nodes = cmds.ls(type="gpuCache")
    directory_path = r"\\10.0.40.42\user\gen\projects\KFA"
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