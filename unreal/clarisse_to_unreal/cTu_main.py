import unreal
import os
from unreal import UsdStageImportFactory as usd_factory

folder_path = r'D:\Kitchen_set\Kitchen_set\usd'
file_list = [f for f in os.listdir(folder_path) if f.endswith('.usd')]


def import_unreal_usd():
    usd_class = unreal.UsdStageActor
    factory = usd_factory()
    editor_actor_subsystem = unreal.EditorActorSubsystem()
    task = unreal.AssetImportTask()

    usd_dir_path = file_path # usd stage dir path import path / root_layout path
    usd_file_name = file_name
    usd_path_name = "/Game/" + usd_file_name

    #import usd asset
    task.set_editor_property("filename", usd_dir_path)
    task.set_editor_property("destination_path", usd_path_name)
    task.set_editor_property('automated', True)

    factory.asset_import_task = task
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])

    #viewport spawn usdStageActor
    # spawn_location = unreal.Vector(0.0, 0.0, 0.0)
    # spawn_rotation = unreal.Rotator(0.0, 0.0, 0.0)
    # spawn_actor = editor_actor_subsystem.spawn_actor_from_class(usd_class, spawn_location, spawn_rotation)

    # spawn_actor.set_actor_label(usd_file_name)
    # spawn_actor.set_root_layer(usd_dir_path)

for file_name in file_list:
    file_path = os.path.join(folder_path, file_name)
    import_unreal_usd()