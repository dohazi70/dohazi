import maya.cmds as cmds
from PySide2 import QtWidgets, QtGui, QtCore


def file_path():
    # 파일 경로 설정
    diffuse_file_path = diffuse_path.text()
    normal_file_path = normal_path.text()
    roughness_file_path = roughness_path.text()
    selected_nodes = cmds.ls(selection=True)
    
    if not diffuse_file_path and not normal_file_path and not roughness_file_path:
        cmds.warning("All texture paths are empty. File nodes and place2dTextures will not be created.")
        return
    
    if diffuse_file_path:
        # file 노드 생성
        diffuse_file_node = cmds.shadingNode('file', asTexture=True, name='diffuse_file')
        cmds.setAttr(diffuse_file_node + '.fileTextureName', diffuse_file_path, type='string')
        
        # place2dTexture 노드 생성
        place2d_diffuse_texture = cmds.shadingNode('place2dTexture', asUtility=True, name='place2d_diffuse_Texture')
        
        # file 노드의 UV좌표 입력에 place2dTexture 노드 연결
        cmds.connectAttr(place2d_diffuse_texture + '.coverage', diffuse_file_node + '.coverage', force=True)
        cmds.connectAttr(place2d_diffuse_texture + '.translateFrame', diffuse_file_node + '.translateFrame', force=True)
        cmds.connectAttr(place2d_diffuse_texture + '.rotateFrame', diffuse_file_node + '.rotateFrame', force=True)
        cmds.connectAttr(place2d_diffuse_texture + '.mirrorU', diffuse_file_node + '.mirrorU', force=True)
        cmds.connectAttr(place2d_diffuse_texture + '.mirrorV', diffuse_file_node + '.mirrorV', force=True)
        cmds.connectAttr(place2d_diffuse_texture + '.stagger', diffuse_file_node + '.stagger', force=True)
        cmds.connectAttr(place2d_diffuse_texture + '.wrapU', diffuse_file_node + '.wrapU', force=True)
        cmds.connectAttr(place2d_diffuse_texture + '.wrapV', diffuse_file_node + '.wrapV', force=True)
        cmds.connectAttr(place2d_diffuse_texture + '.repeatUV', diffuse_file_node + '.repeatUV', force=True)
        cmds.connectAttr(place2d_diffuse_texture + '.offset', diffuse_file_node + '.offset', force=True)
        cmds.connectAttr(place2d_diffuse_texture + '.rotateUV', diffuse_file_node + '.rotateUV', force=True)
        cmds.connectAttr(place2d_diffuse_texture + '.noiseUV', diffuse_file_node + '.noiseUV', force=True)
        
        cmds.connectAttr(place2d_diffuse_texture + '.outUV', diffuse_file_node + '.uvCoord', force=True)
        cmds.connectAttr(diffuse_file_node + '.outColor', selected_nodes[0] + '.diffuseColor', force=True)
    
    if normal_file_path:
        # file 노드 생성
        normal_file_node = cmds.shadingNode('file', asTexture=True, name='normal_file')
        cmds.setAttr(normal_file_node + '.fileTextureName', normal_file_path, type='string')
        
        # place2dTexture 노드 생성
        place2d_normal_texture = cmds.shadingNode('place2dTexture', asUtility=True, name='place2d_normal_Texture')
        
        # file 노드의 UV좌표 입력에 place2dTexture 노드 연결
        cmds.connectAttr(place2d_normal_texture + '.coverage', normal_file_node + '.coverage', force=True)
        cmds.connectAttr(place2d_normal_texture + '.translateFrame', normal_file_node + '.translateFrame', force=True)
        cmds.connectAttr(place2d_normal_texture + '.rotateFrame', normal_file_node + '.rotateFrame', force=True)
        cmds.connectAttr(place2d_normal_texture + '.mirrorU', normal_file_node + '.mirrorU', force=True)
        cmds.connectAttr(place2d_normal_texture + '.mirrorV', normal_file_node + '.mirrorV', force=True)
        cmds.connectAttr(place2d_normal_texture + '.stagger', normal_file_node + '.stagger', force=True)
        cmds.connectAttr(place2d_normal_texture + '.wrapU', normal_file_node + '.wrapU', force=True)
        cmds.connectAttr(place2d_normal_texture + '.wrapV', normal_file_node + '.wrapV', force=True)
        cmds.connectAttr(place2d_normal_texture + '.repeatUV', normal_file_node + '.repeatUV', force=True)
        cmds.connectAttr(place2d_normal_texture + '.offset', normal_file_node + '.offset', force=True)
        cmds.connectAttr(place2d_normal_texture + '.rotateUV', normal_file_node + '.rotateUV', force=True)
        cmds.connectAttr(place2d_normal_texture + '.noiseUV', normal_file_node + '.noiseUV', force=True)
        
        cmds.connectAttr(place2d_normal_texture + '.outUV', normal_file_node + '.uvCoord', force=True)
        cmds.connectAttr(normal_file_node + '.outColor', selected_nodes[0] + '.normal', force=True)
    
    if roughness_file_path:
        # file 노드 생성
        roughness_file_node = cmds.shadingNode('file', asTexture=True, name='roughness_file')
        cmds.setAttr(roughness_file_node + '.fileTextureName', roughness_file_path, type='string')
        
        # place2dTexture 노드 생성
        place2d_roughness_texture = cmds.shadingNode('place2dTexture', asUtility=True, name='place2d_roughness_Texture')
        
        # file 노드의 UV좌표 입력에 place2dTexture 노드 연결
        cmds.connectAttr(place2d_roughness_texture + '.coverage', roughness_file_node + '.coverage', force=True)
        cmds.connectAttr(place2d_roughness_texture + '.translateFrame', roughness_file_node + '.translateFrame', force=True)
        cmds.connectAttr(place2d_roughness_texture + '.rotateFrame', roughness_file_node + '.rotateFrame', force=True)
        cmds.connectAttr(place2d_roughness_texture + '.mirrorU', roughness_file_node + '.mirrorU', force=True)
        cmds.connectAttr(place2d_roughness_texture + '.mirrorV', roughness_file_node + '.mirrorV', force=True)
        cmds.connectAttr(place2d_roughness_texture + '.stagger', roughness_file_node + '.stagger', force=True)
        cmds.connectAttr(place2d_roughness_texture + '.wrapU', roughness_file_node + '.wrapU', force=True)
        cmds.connectAttr(place2d_roughness_texture + '.wrapV', roughness_file_node + '.wrapV', force=True)
        cmds.connectAttr(place2d_roughness_texture + '.repeatUV', roughness_file_node + '.repeatUV', force=True)
        cmds.connectAttr(place2d_roughness_texture + '.offset', roughness_file_node + '.offset', force=True)
        cmds.connectAttr(place2d_roughness_texture + '.rotateUV', roughness_file_node + '.rotateUV', force=True)
        cmds.connectAttr(place2d_roughness_texture + '.noiseUV', roughness_file_node + '.noiseUV', force=True)
        
        cmds.connectAttr(place2d_roughness_texture + '.outUV', roughness_file_node + '.uvCoord', force=True)
        cmds.connectAttr(roughness_file_node + '.outAlpha', selected_nodes[0] + '.roughness', force=True)
    
# Qt 어플리케이션 생성
app = QtWidgets.QApplication.instance()
if not app:
    app = QtWidgets.QApplication([])

# 메인 윈도우 생성
window = QtWidgets.QWidget()
window.setWindowTitle("File Paths")
window.setMinimumWidth(400)

layout = QtWidgets.QVBoxLayout()

# "diffuse" 레이블과 텍스트 입력 필드
find_layout = QtWidgets.QHBoxLayout()
diffuse_label = QtWidgets.QLabel("Diffuse:")
find_layout.addWidget(diffuse_label)
diffuse_path = QtWidgets.QLineEdit()
find_layout.addWidget(diffuse_path)
layout.addLayout(find_layout)

# "normal" 레이블과 텍스트 입력 필드
find_layout = QtWidgets.QHBoxLayout()
normal_label = QtWidgets.QLabel("Normal:")
find_layout.addWidget(normal_label)
normal_path = QtWidgets.QLineEdit()
find_layout.addWidget(normal_path)
layout.addLayout(find_layout)

# "roughness" 레이블과 텍스트 입력 필드 (추가)
find_layout = QtWidgets.QHBoxLayout()
roughness_label = QtWidgets.QLabel("Roughness:")
find_layout.addWidget(roughness_label)
roughness_path = QtWidgets.QLineEdit()
find_layout.addWidget(roughness_path)
layout.addLayout(find_layout)

# 대체 버튼
button = QtWidgets.QPushButton("Load Textures")
button.clicked.connect(file_path)
layout.addWidget(button)

window.setLayout(layout)
window.show()

