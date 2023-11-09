import unreal
import os
from unreal import UsdStageImportFactory as usd_factory
###
folder_path = r'\\10.0.40.42\show\tmp\recover\RND\20231026_assets\env_USD\goyobada\moongr_balhae'
start_index = 1
###
file_list = [f for f in os.listdir(folder_path) if f.endswith('.usd')]


def import_unreal_usd():
    usd_class = unreal.UsdStageActor
    factory = usd_factory()
    editor_actor_subsystem = unreal.EditorActorSubsystem()
    task = unreal.AssetImportTask()

    usd_dir_path = file_path # usd stage dir path import path / root_layout path
    usd_file_name = file_name
    print("d: "+ usd_file_name)
    usd_path_name = "/Game/layout/" + usd_file_name

    #import usd asset
    task.set_editor_property("filename", usd_dir_path)
    task.set_editor_property("destination_path", usd_path_name)
    task.set_editor_property("automated", True)


    factory.asset_import_task = task
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    task.set_editor_property("save", True)
    
    #viewport spawn usdStageActor
    spawn_location = unreal.Vector(0.0, 0.0, 0.0)
    spawn_rotation = unreal.Rotator(0.0, 0.0, 0.0)
    spawn_actor = editor_actor_subsystem.spawn_actor_from_class(usd_class, spawn_location, spawn_rotation)

    usd_file_name = os.path.splitext(file_name)[0]
    spawn_actor.set_actor_label(usd_file_name)
    spawn_actor.set_root_layer(usd_dir_path)

    unreal.EditorAssetLibrary.save_directory("/Game/layout", only_if_is_dirty=True, recursive=True)
    unreal.EditorLevelLibrary.save_current_level()


for index, file_name in enumerate(file_list[start_index - 1:], start=start_index):
    file_path = os.path.join(folder_path, file_name)
    print(f"Processing file {index} of {len(file_list)} : {file_name}")
    import_unreal_usd()


#for index, file_name in enumerate(file_list, start=1):
#    file_path = os.path.join(folder_path, file_name)
#    print(f"Processing file {index} of {len(file_list)} : {file_name}")
#    import_unreal_usd()
