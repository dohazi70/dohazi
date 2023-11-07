## usd ##
 
# import usd
import unreal 
from unreal import UsdStageImportFactory as usd_factory

def import_unreal_usd():
    factory = usd_factory()
    task = unreal.AssetImportTask()
    task.set_editor_property("filename", r"\\10.0.40.42\virtual\unreal_projects\Hero\Bridge\clarisse\USD_test\xhouse.usd")
    task.set_editor_property("destination_path", "/Game/Content/xhouse")
    task.set_editor_property("automated", True)
    factory.asset_import_task = task

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])

import_unreal_usd()

#import usd stage actor
import unreal

def import_unreal_usdStage():
    usd_class = unreal.UsdStageActor
    editor_actor_subsystem = unreal.EditorActorSubsystem()

    path = r"D:/test.usd" # usd stage root_layer path
    usd_stage_label = "test" # usd stage actor name

    spawn_location = unreal.Vector(0.0, 0.0, 0.0)
    spawn_rotation = unreal.Rotator(0.0, 0.0, 0.0)
    spawned_actor = editor_actor_subsystem.spawn_actor_from_class(usd_class, spawn_location, spawn_rotation)

    spawned_actor.set_actor_label(usd_stage_label)
    spawned_actor.set_root_layer(path)


## material ##
import unreal
import re

text  = """ 
TextureMapFile {
    name "snow_with_tall_grass_diffuse2"
    #version 0.98
    copy_from "build://project/layout/a/snow_mountain/detail/dini_snow_mtl/snow_with_tall_grass_diffuse2"
    positions "mat_1" -1093 8721
    projection 0
    space 1
    axis 1
    object_space 2
    uv_scale {
        value 1 1 1
        texture "build://project/layout/a/snow_mountain/detail/dini_snow_mtl/constant_color1"
    }
    filename "\\\\10.0.40.42\\user\\gen\\library\\sourceimages\\pbr\\snow\\CGAxis\\CGAxis PBR Textures Volume 12 - Snow\\snow_with_tall_grass\\4K\\tx\\snow_with_tall_grass_diffuse.tx"
    frame_rate 24
    color_space_auto_detect no
    file_color_space "Clarisse|sRGB"
}
""" #입력 받아야하는 값

def clarisse_TextureMapFile_data():
    copy_from_match = re.search(r'copy_from "(.*?)"', text)
    if copy_from_match:
        copy_from = copy_from_match.group(1)
    else:
        copy_from = None
    filename_match = re.search(r'filename "(.*?)"', text)
    if filename_match:
        filename = filename_match.group(1)
    else:
        filename = None
    positions_match = re.search(r'positions "(.*?)"', text)
    if positions_match:
        positions = positions_match.group(1)
    else:
        positions = None

# import texture
def import_unreal_texture(file_path, destination_path, texture_name):

    import_task = unreal.AssetImportTask()
    import_task.filename = file_path
    import_task.destination_path = destination_path
    import_task.destination_name = texture_name
    import_task.options = None # https://docs.unrealengine.com/5.3/en-US/PythonAPI/class/AssetImportTask.html#unreal.AssetImportTask

    result = unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([import_task]) 

# 머트리얼 및 텍스쳐 연동

import unreal
def material_instance():
    material_instance_name = "NewMaterialInstance2"
    material_instance_path = "/Game/Material/"
    parent_material_path = "/Game/Material/ParentMaterial"

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    parent_material = unreal.load_asset(parent_material_path)

    material_instance = asset_tools.create_asset(material_instance_name, material_instance_path, unreal.MaterialInstanceConstant, None)

    if material_instance:
        material_instance.set_editor_property('Parent', parent_material)

        texture_parameter_name = "BaseColor"
        texture_asset_path = "/Game/Material/texture/storage_lunar_diffC"

        texture_asset = unreal.load_asset(texture_asset_path)
        if texture_asset and isinstance(texture_asset, unreal.Texture):
            unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(material_instance, unreal.Name(texture_parameter_name), texture_asset)

        unreal.EditorAssetLibrary.save_loaded_asset(material_instance)














