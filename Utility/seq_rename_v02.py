import os
import maya.cmds as cmds
from PySide2 import QtWidgets, QtGui, QtCore

input_path = r"\\10.0.40.42\virtual\unreal_projects\Project_Richman\Version\tset\0020\v002"
parts = input_path.split("\\")
desired_part = "\\".join(parts[-3:])
master_path_name = desired_part.replace("\\", "_")
print(master_path_name)

file_list = os.listdir(input_path)

for file_name in file_list:
    file_name_path = file_name.split("_")
    file_desired_path = "_".join(file_name_path[-3:])
    print(file_desired_path)

