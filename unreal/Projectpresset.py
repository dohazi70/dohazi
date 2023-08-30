import unreal
import os

# 프로젝트 컨텐츠 경로 가져오기
project_content_path = unreal.Paths.project_content_dir()

# 각종 경로 설정
asset_path = os.path.join(project_content_path, "asset")
char_path = os.path.join(asset_path, "char")
props_path = os.path.join(asset_path, "props")
building_path = os.path.join(asset_path, "building")
nft_path = os.path.join(asset_path, "NFT")
mastermaterial_path = os.path.join(project_content_path, "MasterMaterial")
materialfunction_path = os.path.join(mastermaterial_path, "function")
shot_folder_path = os.path.join(project_content_path, "Shots")
shot_lv_folder_path = os.path.join(shot_folder_path, "Shot_LV")
Utility_path = os.path.join(project_content_path, "Utility")
work_path = os.path.join(project_content_path, "work")
dh_path = os.path.join(work_path, "dh_work")
jb_path = os.path.join(work_path, "jb_work")
yy_path = os.path.join(work_path, "yy_work")

# Movies 경로 생성
movies_path = os.path.join(project_content_path, "Movies")

# 폴더 생성 함수
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print(f"Directory '{path}' already exists.")

# 폴더 생성
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


# 레벨 제작
shot_name = "sot"
shot_count = 20

#os.makedirs(shot_folder_path, exist_ok=True)

# 레벨 생성 및 경로 변환
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
level_factory = unreal.EditorLevelLibrary
level_names = ["CAM", "CHAR", "ENV", "LIGHT"]
level_suffixes = ["CAM", "CHAR", "ENV", "LIGHT"]

for i in range(1, shot_count + 1):
    shot_path = os.path.join(shot_lv_folder_path, f"{shot_name}_{i:03d}")
    create_directory(shot_path)
    for j, level_name in enumerate(level_names):
        full_level_name = f"{shot_name}_{i:03d}_{level_suffixes[j]}"
        full_level_path = os.path.join(shot_path, full_level_name)
        content_index = full_level_path.find("Content")
        if content_index != -1:
            unreal_path = "/Game" + full_level_path[content_index + len("Content"):].replace("\\", "/")
            level_factory.new_level(unreal_path)

# 서브레벨 등록
main_level_path = "/Game/main"
target_level_path = "/Game/Shots/Shot_LV/"
unreal.EditorLoadingAndSavingUtils.load_map(main_level_path)
world = unreal.EditorLevelLibrary.get_editor_world()
level_asset_data = unreal.EditorAssetLibrary.list_assets(target_level_path, recursive=True, include_folder=True)
for arry_level_path in level_asset_data:
    if os.path.basename(arry_level_path):  # 파일만 출력
        print(arry_level_path)
        unreal.EditorLevelUtils.add_level_to_world(world, arry_level_path, unreal.LevelStreamingAlwaysLoaded)
unreal.EditorLevelLibrary.save_current_level()

# 레벨 시퀀스 제작
for i in range(1, shot_count + 1):
    level_sequence = unreal.AssetTools.create_asset(asset_tools, asset_name = f"{shot_name}_{i:03d}", package_path = "/Game/Shots/", asset_class = unreal.LevelSequence, factory = unreal.LevelSequenceFactoryNew())
    frame_rate = unreal.FrameRate(numerator = 24, denominator = 1)
    level_sequence.set_display_rate(frame_rate)



