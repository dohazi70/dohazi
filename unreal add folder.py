import os
import unreal

# 언리얼 프로젝트의 디렉토리 경로 가져오기
project_directory = unreal.Paths.project_dir()

# "Content" 폴더의 경로 생성
content_folder_path = os.path.join(project_directory, "Content")

# "asset" 폴더 경로 생성
asset_folder_path = os.path.join(content_folder_path, "asset")

# "char" 폴더 경로 생성
char_folder_path = os.path.join(asset_folder_path, "char")

# "props" 폴더 경로 생성
props_folder_path = os.path.join(asset_folder_path, "props")

# 각 폴더 생성
os.makedirs(char_folder_path)
os.makedirs(props_folder_path)
