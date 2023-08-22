import os
import unreal

# 언리얼 프로젝트의 디렉토리 경로 가져오기
project_directory = unreal.Paths.project_dir()

# "Content" 폴더의 경로 생성
content_folder_path = os.path.join(project_directory, "Content")

# 새 폴더 이름 정의
new_folder_name = "MyNewFolder"

# 새 폴더 경로 생성
new_folder_path = os.path.join(content_folder_path, new_folder_name)

# 새 폴더 생성
os.makedirs(new_folder_path)

print(f"새 폴더가 {new_folder_path} 경로에 생성되었습니다.")
