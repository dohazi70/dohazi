import os
import re
import json
import unreal

Json_file_path = r'Z:\unreal_projects\Jaruwon\json\spe_district_gen_dev_v002_w029_edit_mesh_info.json'
material_instace_path = "/Game/Material"
parent_material_path = "/Game/Material/MasterMaterial"
layout_path = '/Game/layout'
material_path = '/Game/Material'

##parmeters name
texture_parameter_name = "BaseColor"
texture_uv_x = "X"
texture_uv_y = "Y"


with open(Json_file_path, 'r') as file:
    Json_data = json.load(file)



all_static_mesh = []
all_material = []

asset_library = unreal.EditorAssetLibrary
all_static_meshs_find = asset_library.list_assets(layout_path, recursive=True, include_folder=False)
for mesh in all_static_meshs_find:
    all_static_mesh.append(mesh)

all_material_find = asset_library.list_assets(material_path, recursive=False, include_folder=False)
for material in all_material_find:
    all_material.append(material)

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
parent_material = unreal.load_asset(parent_material_path)



for item_dict in Json_data:
    for key in item_dict:
        dif_value = item_dict[key]['dif']
        mat_value = item_dict[key]['mat']
        mesh_value = item_dict[key]['mesh']
        y_value = item_dict[key]['y']
        x_value = item_dict[key]['x']
    material_instance_name = mat_value
    material_instace_path = "/Game/Material"
    parent_material_path = "/Game/Material/MasterMaterial"
    x_value = float(x_value)
    y_value = float(y_value)

    dif_texture = os.path.basename(dif_value)
    dif_texture = os.path.splitext(dif_texture)[0]
    dif_texture = re.sub(r'\d{4}$', '', dif_texture)
    if dif_texture.endswith('.') or dif_texture.endswith('_'):
        dif_texture = dif_texture[:-1]

    texture_asset_path = '/Game/Material/Texture' + '/' + dif_texture
## make material_instance 
    full_material_instance_path = material_instace_path + '/' + material_instance_name
    if not unreal.EditorAssetLibrary.does_asset_exist(full_material_instance_path):
        material_instance = asset_tools.create_asset(material_instance_name, material_instace_path, unreal.MaterialInstanceConstant, None)
        if material_instance:
            material_instance.set_editor_property('Parent', parent_material)
            texture_asset = unreal.load_asset(texture_asset_path)
            unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(material_instance, unreal.Name("X"), x_value)
            unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(material_instance, unreal.Name("Y"), y_value)
            unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(material_instance, unreal.Name("BaseColor"), texture_asset)
            unreal.EditorAssetLibrary.save_loaded_asset(material_instance)
    else:
        print(f"{material_instance_name} = Skip")
## static mesh set material
    matching_mesh_path = []
    matching_material = []
    for mesh_path in all_static_mesh:
        if mesh_value in mesh_path.split('/')[-1]:
            matching_mesh_path.append(mesh_path)
    for materiai_path in all_material:
        if mat_value in materiai_path.split('/')[-1]:
            matching_material.append(materiai_path)
    
    for mesh_path, materiai_path in zip(matching_mesh_path, matching_material):
        static_mesh = unreal.EditorAssetLibrary.load_asset(mesh_path)
        material = unreal.EditorAssetLibrary.load_asset(materiai_path)
        unreal.StaticMesh.set_material(static_mesh, 0, material)



