import maya.cmds as cmds

def create_lambert_material(shading_engine_name):
    lambert_material_name = shading_engine_name.replace("_SG", "")
    
    usd_surface_shader = cmds.shadingNode("usdPreviewSurface", asShader=True, name=lambert_material_name)
    
    cmds.defaultNavigation(connectToExisting=True, source=lambert_material_name + ".outColor", destination=shading_engine_name + ".surfaceShader")
    
    return usd_surface_shader

selected_shading_engines = cmds.ls(selection=True, type='shadingEngine')

if selected_shading_engines:
    print("선택된 ShadingEngine 노드 목록:")
    for shading_engine in selected_shading_engines:
        print(shading_engine)
        create_lambert_material(shading_engine)
else:
    print("ShadingEngine 노드가 선택되지 않았습니다.")
