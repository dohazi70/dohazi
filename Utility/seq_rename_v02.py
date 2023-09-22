import os
import maya.cmds as cmds
from PySide2 import QtWidgets, QtGui, QtCore

input_path = r"\\10.0.40.42\virtual\unreal_projects\Project_Richman\Version\tset\0020\v002"
parts = input_path.split("\\")
desired_part = "\\".join(parts[-3:])
master_path_name = desired_part.replace("\\", "_")
print(master_path_name)

file_list = os.listdir(input_path)
prefix = master_path_name + "_"

for file_name in file_list:
    file_path = os.path.join(input_path, file_name)
    file_name_path = file_name.split(".")
    file_desired_path = ".".join(file_name_path[-2:])
    
    new_file_name = f"{prefix}{file_desired_path}"
    new_file_name_path = os.path.join(input_path, new_file_name)
    os.rename(file_path, new_file_name_path) 
    
    
    print(new_file_name_path)

