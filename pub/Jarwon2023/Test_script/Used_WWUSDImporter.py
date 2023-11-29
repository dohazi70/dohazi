import unreal
from unreal import UsdStageImportFactory as usd_factory
from pxr import Usd, Sdf, UsdShade, UsdGeom

import os
import tkinter
from tkinter import filedialog
import pathlib

asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
material_lib = unreal.MaterialEditingLibrary()
editor_asset_lib = unreal.EditorAssetLibrary()

preset_mat_path = "/WWPlugin/WWPresets/SpecWorkflowPreset/M_SpecWF_VT"

def collect_material_prims(prim_path, prim, traverse_variants, material_prim_paths):
    if not prim:
        return

    for child in prim.GetChildren():

        child_path = prim_path.AppendChild(child.GetName())

        if UsdShade.Material(child):
            material_prim_paths.add(child_path)

        collect_material_prims(child_path, child, traverse_variants, material_prim_paths)

# Import Asset
def buildImportTask(filename='', destination_path='', destination_name = '', options=None):
    task = unreal.AssetImportTask()
    #task.set_editor_property('automated', True)
    task.set_editor_property('destination_name', destination_name)
    task.set_editor_property('destination_path', destination_path)
    task.set_editor_property('filename', filename)
    task.set_editor_property('replace_existing', True)
    #task.set_editor_property('save', True)
    task.set_editor_property('options', options)
    return task


#file open
root = tkinter.Tk()
root.withdraw()
usd_file_path = filedialog.askopenfile().name
asset_name = os.path.splitext(os.path.basename(usd_file_path))[0]
asset_path = os.path.dirname(usd_file_path)
specC = None
texture_path = None
usd_mat = None


factory = usd_factory()
task = unreal.AssetImportTask()

options = unreal.UsdStageImportOptions()
options.set_editor_property("override_stage_options",True)
options.set_editor_property("import_geometry",True)
options.set_editor_property("import_materials",True)
options.stage_options = unreal.UsdStageOptions(meters_per_unit=1, up_axis=unreal.UsdUpAxis.Y_AXIS)

task.set_editor_property('automated', True)
task.set_editor_property("filename", usd_file_path)
task.set_editor_property("destination_path", "/Game")
task.set_editor_property("options",options)

factory.asset_import_task = task

asset_tools.import_asset_tasks([task])



all_materials = asset_reg.get_assets_by_path("/Game/"+asset_name+"/Materials",False,False)

stage_root = r'{}'.format(usd_file_path)

stage = Usd.Stage.Open(stage_root, Usd.Stage.LoadAll)
layers_to_traverse = stage.GetUsedLayers(True)

material_prim_paths = set()
traverse_variants = False
collect_material_prims(Sdf.Path("/"), stage.GetPseudoRoot(), traverse_variants, material_prim_paths)


for material in all_materials:
    material_name = str(material.asset_name).split("MI_")[-1]
    
    path = "/"+asset_name+"/materials/PBR_shader"
    print(path)
    PBR_shader = stage.GetPrimAtPath(path)

    if PBR_shader.GetAttribute('inputs:useSpecularWorkflow').Get() == 1:
        if PBR_shader.GetAttribute('inputs:specularColor').HasAuthoredConnections():
            specular_prim = stage.GetPrimAtPath( str(PBR_shader.GetAttribute('inputs:specularColor').GetConnections()[0]).replace(".outputs:rgb", "") )

            texture_path = str(specular_prim.GetAttribute('inputs:file').Get()).replace("./", asset_path + "/texture/").replace("@","")

            if "<UDIM>" in texture_path:
                if os.path.exists(texture_path.replace("<UDIM>", "1001")):
                    texture_path = texture_path.replace("<UDIM>", "1001")
                else:
                    pathlib_path = pathlib.Path(os.path.dirname(texture_path))
                    for item in pathlib_path.iterdir():
                        if item.is_file():
                            if os.path.basename(texture_path).split("<UDIM>")[0] in item.name :
                                texture_path = str(item)
                                start_from_another_number = True
                                break


            print(texture_path)
            task_2 = buildImportTask(texture_path, "/Game/"+asset_name+"/Textures", asset_name+"_SpecC")
            print(task)
            asset_tools.import_asset_tasks([task_2])

            specC = task_2.imported_object_paths[0]
            print(specC)

            preset_mat = editor_asset_lib.load_asset(preset_mat_path)
            usd_mat = editor_asset_lib.load_asset(material.package_name)

            material_lib.set_material_instance_parent(usd_mat, preset_mat)

            tex_asset = editor_asset_lib.find_asset_data(specC).get_asset()
            material_lib.set_material_instance_texture_parameter_value(usd_mat, "SpecularColorTexture", tex_asset)


static_mesh_list = editor_asset_lib.list_assets("/Game/"+asset_name+"/StaticMeshes",False,False)
for static_mesh_path in static_mesh_list:
    static_mesh = editor_asset_lib.load_asset(static_mesh_path)
    actor_location = unreal.Vector(0.0,0.0,0.0)
    actor_rotation = unreal.Rotator(0.0,0.0,0.0)
    unreal.EditorLevelLibrary.spawn_actor_from_object(static_mesh, actor_location, actor_rotation)

# Get a reference to the editor subsystem
editor_subsystem = unreal.UnrealEditorSubsystem()
editor_actor_subsystem = unreal.EditorActorSubsystem()
# Get a reference to the current level
level = editor_subsystem.get_editor_world()
actors = unreal.GameplayStatics.get_all_actors_of_class(level,unreal.Actor)

# Search for the actor by name
actor_to_delete = []
for actor in actors:
    if asset_name in actor.get_name() :
        actor_to_delete.append(actor)
# If the actor was found, delete it
if len(actor_to_delete)>0:
    editor_actor_subsystem.destroy_actors(actor_to_delete)

