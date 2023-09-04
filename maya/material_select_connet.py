import maya.cmds as cmds

# 파일 경로 설정
file_path = r"\\10.0.40.42\show\asd2\assets\global\gen\pub\library\model\prop\gen\asd_prop\sourceimages\v002\2K\jpg\prop_debris_c_2K_Albedo.jpg"
selected_shading = cmds.ls(selection=True, type='usdPreviewSurface')

# file 노드 생성
file_node_create = cmds.shadingNode('file', asTexture=True, name='DiffuseColor')
cmds.setAttr(file_node_create + '.fileTextureName', file_path, type='string')

#file 노드 shading 연결
cmds.connectAttr(file_node_create + '.outColor', selected_shading + '.diffuseColor', force=True)

# place2dTexture 노드 생성
place2d_texture_create = cmds.shadingNode('place2dTexture', asUtility=True, name='place2dTexture')

# file 노드의 UV좌표 입력에 place2dTexture 노드 연결
cmds.connectAttr(place2d_texture_create + '.coverage', file_node_create + '.coverage', force=True)
cmds.connectAttr(place2d_texture_create + '.translateFrame', file_node_create + '.translateFrame', force=True)
cmds.connectAttr(place2d_texture_create + '.rotateFrame', file_node_create + '.rotateFrame', force=True)
cmds.connectAttr(place2d_texture_create + '.mirrorU', file_node_create + '.mirrorU', force=True)
cmds.connectAttr(place2d_texture_create + '.mirrorV', file_node_create + '.mirrorV', force=True)
cmds.connectAttr(place2d_texture_create + '.stagger', file_node_create + '.stagger', force=True)
cmds.connectAttr(place2d_texture_create + '.wrapU', file_node_create + '.wrapU', force=True)
cmds.connectAttr(place2d_texture_create + '.wrapV', file_node_create + '.wrapV', force=True)
cmds.connectAttr(place2d_texture_create + '.repeatUV', file_node_create + '.repeatUV', force=True)
cmds.connectAttr(place2d_texture_create + '.offset', file_node_create + '.offset', force=True)
cmds.connectAttr(place2d_texture_create + '.rotateUV', file_node_create + '.rotateUV', force=True)
cmds.connectAttr(place2d_texture_create + '.noiseUV', file_node_create + '.noiseUV', force=True)
cmds.connectAttr(place2d_texture_create + '.vertexCameraOne', file_node_create + '.vertexCameraOne', force=True)
cmds.connectAttr(place2d_texture_create + '.vertexUvThree', file_node_create + '.vertexUvThree', force=True)
cmds.connectAttr(place2d_texture_create + '.vertexUvThree', file_node_create + '.vertexUvThree', force=True)


