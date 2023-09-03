import maya.cmds as cmds
from PySide2 import QtWidgets

def get_user_search_text():
    # 대화 상자 생성
    dialog = QtWidgets.QInputDialog()
    dialog.setWindowTitle("Search Text")
    dialog.setLabelText("Enter search text:")  # 사용자에게 입력할 텍스트를 입력하라는 메시지
    dialog.setInputMode(QtWidgets.QInputDialog.TextInput)
    dialog.setTextValue("")  # 초기 값 설정

    # 대화 상자를 표시하고 사용자 입력 받기
    if dialog.exec_():
        search_text = dialog.textValue()  # 사용자가 입력한 텍스트 가져오기
        return search_text
    else:
        return None

# 사용자로부터 검색 텍스트 받기
search_text = get_user_search_text()

if search_text is not None:
    # GPU 캐시 노드 목록 가져오기
    gpu_cache_nodes = cmds.ls(type="gpuCache")
    abc_cache_nodes = cmds.ls(type="mesh")

    # 사용자가 입력한 텍스트로 필터링하여 노드 선택
    selected_gpu_cache_nodes = [node for node in gpu_cache_nodes if search_text in node]
    selected_abc_cache_nodes = [node for node in abc_cache_nodes if search_text in node]

    # Shape를 없애줌
    selected_gpu_cache_nodes = [node.replace("Shape", "") for node in selected_gpu_cache_nodes]
    selected_abc_cache_nodes = [node.replace("Shape", "") for node in selected_abc_cache_nodes]

    # GPU 캐시 노드 선택
    cmds.select(selected_gpu_cache_nodes)

    # ABC 캐시 노드 선택 (add=True를 사용하여 추가 선택)
    cmds.select(selected_abc_cache_nodes, add=True)

    cmds.ReplaceObjects()
