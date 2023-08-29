import unreal
import os


project_content_path = unreal.Paths.project_content_dir( )

# asset
asset_path = os.path.join(project_content_path, "asset")
char_path = os.path.join(asset_path, "char")
props_path = os.path.join(asset_path, "props")
building_path = os.path.join(asset_path, "building")
nft_path = os.path.join(asset_path, "NFT")

#material
mastermaterial_path = os.path.join(project_content_path, "MasterMaterial")
materialfunction_path = os.path.join(mastermaterial_path, "function")

#blueprint
Utility_path = os.path.join(project_content_path, "Utility")

#work
work_path = os.path.join(project_content_path, "work")
dh_path = os.path.join(work_path, "dh_work")
jb_path = os.path.join(work_path, "jb_work")
yy_path = os.path.join(work_path, "yy_work")

#shots
shot_name = "sot"
shot_count = int(20)
shot_folder_path = os.path.join(project_content_path, "Shots")
shot_lv_folder_path = os.path.join(shot_folder_path, "Shot_LV")
os.makedirs(shot_folder_path, exist_ok=True)

# 레벨 제작

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
level_factory = unreal.EditorLevelLibrary
level_names = ["CAM", "CHAR", "ENV", "LIGHT"]
level_suffixes = ["CAM", "CHAR", "ENV", "LIGHT"]
level_path = "/Game/Levels/"


for i in range(1, shot_count + 1):
    shot_path = os.path.join(shot_lv_folder_path, f"{shot_name}_{i:03d}")
    os.makedirs(shot_path)
    for j, level_name in enumerate(level_names):
        full_level_name = f"{shot_name}_{i:03d}_{level_suffixes[j]}"
        print("full_level_name: " + full_level_name)
        full_level_path = os.path.join(shot_path, full_level_name)
        print("full_level_name: " + full_level_path)

        content_index = full_level_path.find("Content")
        if content_index != -1:
            unreal_path = "/Game" + full_level_path[content_index + len("Content"):].replace("\\", "/")
            print(unreal_path)
        else:
            print("invalid input path")
        
        level_factory = unreal.EditorLevelLibrary
        makeleve = level_factory.new_level(unreal_path.format())

## 서브레벨 등록

main_level_path = "/Game/main"
target_level_path = "/Game/Shots/Shot_LV/"

unreal.EditorLoadingAndSavingUtils.load_map(main_level_path)

world = unreal.EditorLevelLibrary.get_editor_world()
level_asset_data = unreal.EditorAssetLibrary.list_assets(target_level_path, recursive=True, include_folder=True)
level_asset_data_len = len(level_asset_data)

for i in range(level_asset_data_len):
    arry_level_path = level_asset_data[i]
    unreal.EditorLevelUtils.add_level_to_world(world, arry_level_path, unreal.LevelStreamingAlwaysLoaded)

unreal.EditorLevelLibrary.save_current_level()

#레벨시퀀스 제작

for i in range(1, shot_count + 1):
    level_sequence = unreal.AssetTools.create_asset(asset_tools, asset_name = f"{shot_name}_{i:03d}", package_path = "/Game/Shots/", asset_class = unreal.LevelSequence, factory = unreal.LevelSequenceFactoryNew())
    frame_rate = unreal.FrameRate(numerator = 24, denominator = 1)
    level_sequence.set_display_rate(frame_rate)


#movies
movies_path = os.path.join(project_content_path, "Movies")


os.makedirs(char_path)
os.makedirs(props_path)
os.makedirs(building_path)
os.makedirs(nft_path)
os.makedirs(materialfunction_path)
os.makedirs(Utility_path)
os.makedirs(movies_path)
os.makedirs(dh_path)
os.makedirs(jb_path)
os.makedirs(yy_path)

