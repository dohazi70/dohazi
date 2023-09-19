import os
import unreal

folder_path = "D:\dev\UnrealEngine\MV_richman\Saved\MovieRenders\v02\S_015\MASTER"

file_list = os.listdir(folder_path)

for file_name in file_list:
    print(file_name)