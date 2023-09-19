import nuke

camera_node = nuke.createNode('Camera2')

camera_node['use_matrix'].setValue('input')
camera_node['matrix'].fromScript('0.9976 -0.0659 -0.0213 0.0000 0.0659 0.9976 -0.0213 0.0000 0.0213 0.0213 0.9996 0.0000 -0.0426 0.0199 0.0465 1.0000')
camera_node['haperture'].setValue(36.0)
camera_node['vaperture'].setValue(24.0)
camera_node['focal'].setValue(50.0)

camera_node['translate'].setValue([0.0, 0.0, 10.0])
camera_node['rotate'].setValue([-10.0, 0.0, 0.0])

#file
file_path = "Z:\\virtual\\sanghyeop\\project\\richman\\Camimport_test\\ue_cam_test_001.fbx"
camera_node["file"].setValue(file_path)

viewport_node = nuke.createNode('Viewer')
viewport_node.setInput(0, camera_node)

nuke.autoplace(0)

nuke.scriptUpdateUI()
