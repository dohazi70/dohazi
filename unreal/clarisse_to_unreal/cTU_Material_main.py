import os
import re
import json
import unreal

def import_unreal_texture(texture_file_path, destination_path, texture_name):

    import_task = unreal.AssetImportTask()
    import_task.filename = texture_file_path
    import_task.destination_path = destination_path
    import_task.destination_name = texture_name
    import_task.options = None
    result = unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([import_task]) 
def material_instance(mtl_instance_name, texture_path):
    material_instance_name = mtl_instance_name
    material_instance_path = "/Game/Material/"
    parent_material_path = "/Game/Material/ParentMaterial"

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    parent_material = unreal.load_asset(parent_material_path)

    material_instance = asset_tools.create_asset(material_instance_name, material_instance_path, unreal.MaterialInstanceConstant, None)

    if material_instance:
        material_instance.set_editor_property('Parent', parent_material)

        texture_parameter_name = "BaseColor"
        texture_asset_path = texture_path

        texture_asset = unreal.load_asset(texture_asset_path)
        if texture_asset and isinstance(texture_asset, unreal.Texture):
            unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(material_instance, unreal.Name(texture_parameter_name), texture_asset)

        unreal.EditorAssetLibrary.save_loaded_asset(material_instance)
def find_static_meshes(search_string):
    all_static_meshes = unreal.EditorAssetLibrary.list_assets('/Game/layout', recursive=True, include_folder=True)
    
    matching_meshes = []
    for mesh in all_static_meshes:
        if unreal.EditorAssetLibrary.does_asset_exist(mesh):
            asset_name = mesh.split('/')[-1]
            if asset_name.startswith(search_string + '.'):
                matching_meshes.append(mesh)
    return matching_meshes
def find_material(search_string):
    all_material = unreal.EditorAssetLibrary.list_assets('/Game/Material', recursive=True, include_folder=True)
    
    matching_material = []
    for mesh in all_material:
        if unreal.EditorAssetLibrary.does_asset_exist(mesh):
            asset_name = mesh.split('/')[-1]
            if asset_name.startswith(search_string + '.'):
                matching_material.append(mesh)
    return matching_material
def process_json_data(Json_data):
    all_matching_meshes = []
    all_matching_materials = []

    for item_dict in Json_data:
        for key in item_dict:
            mesh_value = item_dict[key]['mesh']
            mat2_value = item_dict[key]['mat']

            matching_meshes = find_static_meshes(mesh_value)
            matching_materials = find_material(mat2_value)

            all_matching_meshes.extend(matching_meshes)  # 결과를 전체 리스트에 추가합니다.
            all_matching_materials.extend(matching_materials)  # 결과를 전체 리스트에 추가합니다.

    # 모든 처리가 끝난 후, 메시 리스트와 재질 리스트를 반환합니다.
    return all_matching_meshes, all_matching_materials

Json_file_path = r'D:\dev\Code\dohazi\unreal\clarisse_to_unreal\Test_script\test.json'

ue_material_path = '/Game/Material'
ue_texture_path = '/Game/Material/Texture'

with open(Json_file_path, 'r') as file:
    Json_data = json.load(file)

unique_difs = []
unique_mats = []

for item_dict in Json_data:
    for key in item_dict:
        dif_value = item_dict[key]['dif']
        mat_value = item_dict[key]['mat']
        if dif_value not in unique_difs:
            unique_difs.append(dif_value)
        if mat_value not in unique_mats:
            unique_mats.append(mat_value)

for dif in unique_difs:
    dif_extension = os.path.splitext(os.path.basename(dif))[0]
    dif_base_name = re.sub(r'\.\d+$', '', dif_extension)
    import_unreal_texture(dif, ue_texture_path, dif_base_name)

for mat in unique_mats:
    dif_local_path = ue_texture_path + "/" + dif_base_name
    material_instance(mat, dif_local_path)

matching_meshes, matching_materials = process_json_data(Json_data)

for meshe_path, materials_path in zip(matching_meshes, matching_materials):
    static_mesh = unreal.EditorAssetLibrary.load_asset(meshe_path)
    material = unreal.EditorAssetLibrary.load_asset(materials_path)
    unreal.StaticMesh.set_material(static_mesh, 0, material)

