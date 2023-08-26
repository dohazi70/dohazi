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

#seq
shot_name = input("shot name: ")
shot_count = int(input("shot index: "))
shot_folder_path = os.path.join(project_content_path, "Shots")
os.makedirs(shot_folder_path, exist_ok=True)

for i in range(1, shot_count + 1):
    shot_path = os.path.join(shot_folder_path, f"{shot_name}_{i}")
    os.makedirs(shot_path)

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
for i in range(1, shot_count + 1):
    level_sequence = unreal.AssetTools.create_asset(asset_tools, asset_name = f"{shot_name}_{i}", package_path = "/Game/Shots/", asset_class = unreal.LevelSequence, factory = unreal.LevelSequenceFactoryNew())
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


