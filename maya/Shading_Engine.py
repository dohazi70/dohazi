import maya.cmds as cmds

def create_lambert_material(shading_engine_name):
    # Lambert 머티리얼 이름 설정 (Shading Engine 이름과 동일하게)
    lambert_material_name = shading_engine_name.replace("_SG", "")
    
    # Lambert 머티리얼 생성
    usd_surface_shader = cmds.shadingNode("usdPreviewSurface", asShader=True, name=lambert_material_name)
    
    # Lambert 머티리얼을 Shading Engine에 연결
    cmds.defaultNavigation(connectToExisting=True, source=lambert_material_name + ".outColor", destination=shading_engine_name + ".surfaceShader")
    
    return usd_surface_shader

# 현재 선택된 ShadingEngine 노드 가져오기
selected_shading_engines = cmds.ls(selection=True, type='shadingEngine')

if selected_shading_engines:
    print("선택된 ShadingEngine 노드 목록:")
    for shading_engine in selected_shading_engines:
        print(shading_engine)
        create_lambert_material(shading_engine)
else:
    print("ShadingEngine 노드가 선택되지 않았습니다.")