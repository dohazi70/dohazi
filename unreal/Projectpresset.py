import unreal
import os

###########
shot_count = 2
shot_sucount = 4
###########

# project path
project_content_path = unreal.Paths.project_content_dir()

# path
asset_path = os.path.join(project_content_path, "Asset")
char_path = os.path.join(asset_path, "Char")
props_path = os.path.join(asset_path, "Props")
building_path = os.path.join(asset_path, "Building")
nft_path = os.path.join(asset_path, "NFT")
mastermaterial_path = os.path.join(project_content_path, "Material")
materialfunction_path = os.path.join(mastermaterial_path, "function")
shot_folder_path = os.path.join(project_content_path, "Shots")
shot_lv_folder_path = os.path.join(shot_folder_path, "Shot_LV")
Utility_path = os.path.join(project_content_path, "Utility")
work_path = os.path.join(project_content_path, "work")
dh_path = os.path.join(work_path, "dh_work")
jb_path = os.path.join(work_path, "jb_work")
yy_path = os.path.join(work_path, "yy_work")
movies_path = os.path.join(project_content_path, "Movies")

# folder mf
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print(f"Directory '{path}' already exists.")

# folder create
create_directory(movies_path)
create_directory(char_path)
create_directory(props_path)
create_directory(building_path)
create_directory(nft_path)
create_directory(materialfunction_path)
create_directory(Utility_path)
create_directory(dh_path)
create_directory(jb_path)
create_directory(yy_path)
create_directory(shot_folder_path)

# create level
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
level_factory = unreal.EditorLevelLibrary
level_names = ["CAM", "CHAR", "ENV", "LIGHT"]
level_suffixes = ["CAM", "CHAR", "ENV", "LIGHT"]

for x in range(1, shot_count + 1):
    shot_path_name = f"S{x:03d}"
    for i in range(1, shot_sucount + 1):
        i = int(i) * 10
        shot_path = os.path.join(shot_lv_folder_path, shot_path_name + f"_{i:04d}")
        create_directory(shot_path)
        for j, level_name in enumerate(level_names):
            full_level_name = shot_path_name + f"_{i:04d}_{level_suffixes[j]}"
            full_level_path = os.path.join(shot_path, full_level_name)
            content_index = full_level_path.find("Content")
            if content_index != -1:
                unreal_path = "/Game" + full_level_path[content_index + len("Content"):].replace("\\", "/")
                level_factory.new_level(unreal_path)

# sublevel
main_level_path = "/Game/main"
target_level_path = "/Game/Shots/Shot_LV/"
unreal.EditorLoadingAndSavingUtils.load_map(main_level_path)
world = unreal.EditorLevelLibrary.get_editor_world()
level_asset_data = unreal.EditorAssetLibrary.list_assets(target_level_path, recursive=True, include_folder=True)
for arry_level_path in level_asset_data:
    if os.path.basename(arry_level_path):
        unreal.EditorLevelUtils.add_level_to_world(world, arry_level_path, unreal.LevelStreamingAlwaysLoaded)
unreal.EditorLevelLibrary.save_current_level()

# seq
for x in range(1, shot_count + 1):
    shot_path_name = f"S{x:03d}"
    for i in range(1, shot_sucount + 1):
        i = int(i) * 10
        level_sequence = unreal.AssetTools.create_asset(asset_tools, asset_name = shot_path_name + f"_{i:04d}", package_path = "/Game/Shots/", asset_class = unreal.LevelSequence, factory = unreal.LevelSequenceFactoryNew())
        frame_rate = unreal.FrameRate(numerator = 24, denominator = 1)
        level_sequence.set_display_rate(frame_rate)
        target_level_path2 = "/Game/Shots/Shot_LV/" + shot_path_name + f"_{i:04d}/"
        print(target_level_path2)
        level_asset_data2 = unreal.EditorAssetLibrary.list_assets(target_level_path2, recursive=True, include_folder=True)
        for arry_level_path in level_asset_data2:
                if os.path.basename(arry_level_path):
                    filename, _ = os.path.splitext(os.path.basename(arry_level_path))
                    print("path:" + filename)
                    level_visibility_track = level_sequence.add_master_track(unreal.MovieSceneLevelVisibilityTrack)
                    level_visibility_section = level_visibility_track.add_section()
                    level_visibility_section.set_range(0, 150)
                    level_visibility_section.set_level_names([filename])