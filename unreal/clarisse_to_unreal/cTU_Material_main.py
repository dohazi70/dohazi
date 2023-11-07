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
        if dif_value not in unique_difs:
            unique_difs.append(dif_value)

for item_dict in Json_data:
    for key in item_dict:
        mat_value = item_dict[key]['mat']
        if mat_value not in unique_mats:
            unique_mats.append(mat_value)

for dif in unique_difs:
    dif_extension = os.path.splitext(os.path.basename(dif))[0]
    dif_base_name = re.sub(r'\.\d+$', '', dif_extension)
    import_unreal_texture(dif, ue_texture_path, dif_base_name)
    
for mat in unique_mats:
    dif_local_path = ue_texture_path + "/" + dif_base_name
    material_instance(mat, dif_local_path)

