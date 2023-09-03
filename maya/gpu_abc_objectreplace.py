import maya.cmds as cmds

# GPU 캐시 노드 목록 가져오기
gpu_cache_nodes = cmds.ls(type="gpuCache")
abc_cache_nodes = cmds.ls(type="mesh")

# "test"가 들어간 이름을 가진 GPU 캐시 노드를 선택
selected_gpu_cache_nodes = [node for node in gpu_cache_nodes if "test" in node]
selected_abc_cache_nodes = [node for node in abc_cache_nodes if "test" in node]

# Shape를 없애줌
selected_gpu_cache_nodes = [node.replace("Shape", "") for node in selected_gpu_cache_nodes]
selected_abc_cache_nodes = [node.replace("Shape", "") for node in selected_abc_cache_nodes]

# GPU 캐시 노드 선택
cmds.select(selected_gpu_cache_nodes)

# ABC 캐시 노드 선택 (add=True를 사용하여 추가 선택)
cmds.select(selected_abc_cache_nodes, add=True)

cmds.ReplaceObjects()
