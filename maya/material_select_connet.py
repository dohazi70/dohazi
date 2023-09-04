import maya.cmds as cmds

# 파일 경로 설정
file_path = r"\\10.0.40.42\show\asd2\assets\global\gen\pub\library\model\prop\gen\asd_prop\sourceimages\v002\2K\jpg\prop_debris_c_2K_Albedo.jpg"

# file 노드 생성
file_node = cmds.shadingNode('file', asTexture=True, name='DiffuseColor')
cmds.setAttr(file_node + '.fileTextureName', file_path, type='string')

# place2dTexture 노드 생성
place2d_texture = cmds.shadingNode('place2dTexture', asUtility=True, name='place2dTexture')

# file 노드의 UV좌표 입력에 place2dTexture 노드 연결
cmds.connectAttr(place2d_texture + '.coverage', file_node + '.coverage', force=True)
cmds.connectAttr(place2d_texture + '.translateFrame', file_node + '.translateFrame', force=True)
cmds.connectAttr(place2d_texture + '.rotateFrame', file_node + '.rotateFrame', force=True)
cmds.connectAttr(place2d_texture + '.mirrorU', file_node + '.mirrorU', force=True)
cmds.connectAttr(place2d_texture + '.mirrorV', file_node + '.mirrorV', force=True)
cmds.connectAttr(place2d_texture + '.stagger', file_node + '.stagger', force=True)
cmds.connectAttr(place2d_texture + '.wrapU', file_node + '.wrapU', force=True)
cmds.connectAttr(place2d_texture + '.wrapV', file_node + '.wrapV', force=True)
cmds.connectAttr(place2d_texture + '.repeatUV', file_node + '.repeatUV', force=True)
cmds.connectAttr(place2d_texture + '.offset', file_node + '.offset', force=True)
cmds.connectAttr(place2d_texture + '.rotateUV', file_node + '.rotateUV', force=True)
cmds.connectAttr(place2d_texture + '.noiseUV', file_node + '.noiseUV', force=True)
cmds.connectAttr(place2d_texture + '.vertexCameraOne', file_node + '.vertexCameraOne', force=True)
cmds.connectAttr(place2d_texture + '.vertexUvThree', file_node + '.vertexUvThree', force=True)
cmds.connectAttr(place2d_texture + '.vertexUvThree', file_node + '.vertexUvThree', force=True)

# Out UV와 UV Coord 연결
cmds.connectAttr(place2d_texture + '.outUV', file_node + '.uvCoord', force=True)


# 선택한 노드에 file 노드 연결 (이 부분을 필요한 대상 노드로 변경하세요)
selected_nodes = cmds.ls(selection=True)
for node in selected_nodes:
    shading_group = cmds.listConnections(node + '.message', type='shadingEngine')[0]
    cmds.connectAttr(file_node + '.outColor', shading_group + '.diffuseColor', force=True)


import maya.cmds as cmds

# 파일 경로 설정
file_path = r"\\10.0.40.42\show\asd2\assets\global\gen\pub\library\model\prop\gen\asd_prop\sourceimages\v002\2K\jpg\prop_debris_c_2K_Albedo.jpg"

# file 노드 생성
file_node = cmds.shadingNode('file', asTexture=True, name='DiffuseColor')
cmds.setAttr(file_node + '.fileTextureName', file_path, type='string')

# place2dTexture 노드 생성
place2d_texture = cmds.shadingNode('place2dTexture', asUtility=True, name='place2dTexture')

# file 노드의 UV좌표 입력에 place2dTexture 노드 연결
cmds.connectAttr(place2d_texture + '.coverage', file_node + '.coverage', force=True)
cmds.connectAttr(place2d_texture + '.translateFrame', file_node + '.translateFrame', force=True)
cmds.connectAttr(place2d_texture + '.rotateFrame', file_node + '.rotateFrame', force=True)
cmds.connectAttr(place2d_texture + '.mirrorU', file_node + '.mirrorU', force=True)
cmds.connectAttr(place2d_texture + '.mirrorV', file_node + '.mirrorV', force=True)
cmds.connectAttr(place2d_texture + '.stagger', file_node + '.stagger', force=True)
cmds.connectAttr(place2d_texture + '.wrapU', file_node + '.wrapU', force=True)
cmds.connectAttr(place2d_texture + '.wrapV', file_node + '.wrapV', force=True)
cmds.connectAttr(place2d_texture + '.repeatUV', file_node + '.repeatUV', force=True)
cmds.connectAttr(place2d_texture + '.offset', file_node + '.offset', force=True)
cmds.connectAttr(place2d_texture + '.rotateUV', file_node + '.rotateUV', force=True)
cmds.connectAttr(place2d_texture + '.noiseUV', file_node + '.noiseUV', force=True)
cmds.connectAttr(place2d_texture + '.vertexCameraOne', file_node + '.vertexCameraOne', force=True)
cmds.connectAttr(place2d_texture + '.vertexUvThree', file_node + '.vertexUvThree', force=True)
cmds.connectAttr(place2d_texture + '.vertexUvThree', file_node + '.vertexUvThree', force=True)


selected_shading_engines = cmds.ls(selection=True, type='usdPreviewSurface')

# Out UV와 UV Coord 연결
cmds.connectAttr(place2d_texture + '.outUV', file_node + '.uvCoord', force=True)
cmds.connectAttr(file_node + '.outColor', selected_shading_engines + '.diffuseColor', force=True)


