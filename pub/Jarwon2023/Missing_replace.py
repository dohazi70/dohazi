import os
import maya.cmds as cmds
import shutil
import re
from PySide2 import QtGui, QtWidgets

def find_first_numeric_file(folder_path, base_name):
    numeric_files = []

    for file in os.listdir(folder_path):
        if base_name in file:
            numbers = re.findall(r'\d+', file)
            if numbers:
                numeric_files.append((int(numbers[0]), file))

    numeric_files.sort()
    return numeric_files[0][1] if numeric_files else None
def find_numeric_file(folder_path, base_name):
    numeric_files2 = []

    for file in os.listdir(folder_path):
        if base_name in file:
            numbers = re.findall(r'\d+', file)
            if numbers:
                numeric_files2.append((int(numbers[0]), file))
    return numeric_files2

class MissingFilesWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MissingFilesWindow, self).__init__(parent)
        self.setWindowTitle("File Status")
        self.setGeometry(200, 200, 1000, 1200)
        self.buildUI()

    def buildUI(self):
        layout = QtWidgets.QVBoxLayout(self)

        searchReplaceLayout = QtWidgets.QHBoxLayout()
        layout.addLayout(searchReplaceLayout)
        copyLayout = QtWidgets.QHBoxLayout()
        layout.addLayout(copyLayout)
        buttonLayout = QtWidgets.QHBoxLayout()
        layout.addLayout(buttonLayout)

        searchReplaceLayout.addWidget(QtWidgets.QLabel("Search:"))
        self.searchLineEdit = QtWidgets.QLineEdit()
        searchReplaceLayout.addWidget(self.searchLineEdit)

        searchReplaceLayout.addWidget(QtWidgets.QLabel("Replace:"))
        self.replaceLineEdit = QtWidgets.QLineEdit()
        searchReplaceLayout.addWidget(self.replaceLineEdit)

        copyLayout.addWidget(QtWidgets.QLabel("Copy Path:"))
        self.copyLineEdit = QtWidgets.QLineEdit()
        copyLayout.addWidget(self.copyLineEdit)

        replaceButton = QtWidgets.QPushButton("Replace")
        replaceButton.clicked.connect(self.replacePaths)
        searchReplaceLayout.addWidget(replaceButton)

        CopyButton = QtWidgets.QPushButton("Copy")
        CopyButton.clicked.connect(self.copy_files)
        copyLayout.addWidget(CopyButton)

        assButton = QtWidgets.QPushButton("ass")
        assButton.clicked.connect(self.ass_copy)
        copyLayout.addWidget(assButton)

        tifButton = QtWidgets.QPushButton("Set tif")
        tifButton.clicked.connect(self.tifs)
        buttonLayout.addWidget(tifButton)
        
        refresh = QtWidgets.QPushButton("Refresh")
        refresh.clicked.connect(self.populate)
        buttonLayout.addWidget(refresh)

        # Tab Widget
        self.tabWidget = QtWidgets.QTabWidget()
        self.missingTab = QtWidgets.QWidget()
        self.okTab = QtWidgets.QWidget()

        self.tabWidget.addTab(self.missingTab, "Missing")
        self.tabWidget.addTab(self.okTab, "Found")
        layout.addWidget(self.tabWidget)

        # Setup Missing Tab
        self.missingLayout = QtWidgets.QVBoxLayout(self.missingTab)
        self.missingTable = QtWidgets.QTableWidget()
        self.missingTable.setColumnCount(2)
        self.missingTable.setHorizontalHeaderLabels(['File Path', 'Status'])
        self.missingLayout.addWidget(self.missingTable)

        # Setup OK Tab
        self.okLayout = QtWidgets.QVBoxLayout(self.okTab)
        self.okTable = QtWidgets.QTableWidget()
        self.okTable.setColumnCount(2)
        self.okTable.setHorizontalHeaderLabels(['File Path', 'Status'])
        self.okLayout.addWidget(self.okTable)

        # Close Button
        closeBtn = QtWidgets.QPushButton("Close")
        closeBtn.clicked.connect(self.close)
        layout.addWidget(closeBtn)



    def populate(self):
        self.missingTable.setRowCount(0)
        self.okTable.setRowCount(0)

        nodes_attrs = [
            ('file', 'fileTextureName'),
            ('AlembicNode', 'abc_File'),
            ('gpuCache', 'cacheFileName'),
            ('aiStandIn', 'dso'),
        ]

        for node_type, attr_name in nodes_attrs:
            nodes = cmds.ls(type=node_type)
            for node in nodes:
                if cmds.attributeQuery(attr_name, node=node, exists=True):
                    file_path = cmds.getAttr(f"{node}.{attr_name}")
                    row_position = self.missingTable.rowCount() if not os.path.exists(file_path) else self.okTable.rowCount()
                    table_to_use = self.missingTable if not os.path.exists(file_path) else self.okTable

                    table_to_use.insertRow(row_position)
                    table_to_use.setItem(row_position, 0, QtWidgets.QTableWidgetItem(file_path))

                    if not os.path.exists(file_path):
                        item = QtWidgets.QTableWidgetItem("Not Found")
                        item.setBackground(QtGui.QColor(255, 0, 0))
                        item.setForeground(QtGui.QBrush(QtGui.QColor(0, 0, 0)))
                        icon = QtGui.QIcon(":status_error.png")
                        item.setIcon(icon)
                        table_to_use.setItem(row_position, 1, item)
                    else:
                        item = QtWidgets.QTableWidgetItem("Found")
                        item.setBackground(QtGui.QColor(0, 255, 0))
                        item.setForeground(QtGui.QBrush(QtGui.QColor(0, 0, 0)))
                        icon = QtGui.QIcon(":status_success.png")
                        item.setIcon(icon)
                        table_to_use.setItem(row_position, 1, item)

        self.missingTable.resizeColumnsToContents()
        self.okTable.resizeColumnsToContents()

    def replacePaths(self):
        search_str = self.searchLineEdit.text()
        replace_str = self.replaceLineEdit.text()

        nodes_attrs = [
            ('file', 'fileTextureName'),
            ('AlembicNode', 'abc_File'),
            ('gpuCache', 'cacheFileName'),
            ('aiStandIn', 'dso'),
        ]

        for node_type, attr_name in nodes_attrs:
            nodes = cmds.ls(type=node_type)
            for node in nodes:
                if cmds.attributeQuery(attr_name, node=node, exists=True):
                    file_path = cmds.getAttr(f"{node}.{attr_name}")

                    if file_path and search_str in file_path:
                        new_path = file_path.replace(search_str, replace_str)
                        cmds.setAttr(f"{node}.{attr_name}", new_path, type="string")
                        
        self.populate()

    def tifs(self):
        file_path = r"./tif"
        file_nodes = cmds.ls(type = 'file')
        for node in file_nodes:
            file_full_name = cmds.getAttr(f"{node}.fileTextureName")
            file_1base_name = os.path.basename(file_full_name)
            file_base_name = os.path.splitext(file_1base_name)[0]
            file_base_name_cleaned = re.sub(r'\d{4}$', '', file_base_name)
            file_base_name_cleaned_udim = file_base_name_cleaned.replace("<UDIM>", "").replace("<udim>", "")
            find_file = find_first_numeric_file(file_path, file_base_name_cleaned_udim)
            find_file_index = find_numeric_file(file_path, file_base_name_cleaned_udim)
            
            if find_file is not None:
                new_path = './tif/' + find_file
                cmds.setAttr(node + '.fileTextureName', new_path, type='string')
            else:
                notnew_path = './tif/' + file_1base_name
                cmds.setAttr(node + '.fileTextureName', notnew_path, type='string')
            
            if len(find_file_index) == 2:
                cmds.setAttr(f"{node}.uvTilingMode", 0)
            elif len(find_file_index) > 2:
                cmds.setAttr(f"{node}.uvTilingMode", 3)
                cmds.setAttr(f"{node}.uvTileProxyQuality", 1)
        
        ass_nodes = cmds.ls(type='aiStandIn')
        for a in ass_nodes:
            a_current_path = cmds.getAttr(a + '.dso')
            a_file_name = os.path.basename(a_current_path)
            a_new_path = './tif/' + a_file_name
            cmds.setAttr(a + '.dso', a_new_path, type='string')
        self.populate()


    def ass_copy(self):
        destination_directory = self.copyLineEdit.text()
        ass_nodes = cmds.ls(type='aiStandIn')
        ass_file_paths = []

        for ass_node in ass_nodes:
            ass_path = cmds.getAttr(f"{ass_node}.dso")
            if ass_path.lower().endswith(".ass"):
                ass_file_paths.append(ass_path)
        ass_index = 1
        for ass_path in ass_file_paths:
            ass_file_paths = os.path.basename(ass_path)
            ass_destination = os.path.join(destination_directory, ass_file_paths)
            try:
                shutil.copy2(ass_path, ass_destination)
                print(f"{ass_index}")
                ass_index += 1
            except Exception as e:
                print(f"Error copying {ass_file_paths}: {e}")
    print("ass copy done")


    def copy_files(self):
        destination_directory = self.copyLineEdit.text()
        texture_nodes = cmds.ls(type='file')
        valid_file_names = set()
        unique_paths = set()
        try:
            for node in texture_nodes:
                path = cmds.getAttr(f"{node}.fileTextureName")
                parts = path.split("/")
                if len(parts) > 1:
                    unique_paths.add("/".join(parts[:-1]))
                    
                file_name = os.path.basename(path)
                file_name_without_extension, extension = os.path.splitext(file_name)
                
                extracted_name = file_name_without_extension[:7]
                valid_file_names.add(extracted_name)

            index = 1
            total_files = len(valid_file_names)

            for unique_path in unique_paths:
                files_in_path = os.listdir(unique_path)
                for file_name in files_in_path:
                    for extracted_name in valid_file_names:
                        if extracted_name in file_name:
                            source_path = os.path.join(unique_path, file_name)
                            destination = os.path.join(destination_directory, file_name)
                            if not os.path.isdir(source_path):
                                try:
                                    shutil.copy2(source_path, destination)
                                    print(f'{index}')
                                    index += 1
                                except Exception as e:
                                    print(f"[{index}/{total_files}] Error copying {source_path}: {e}")
        except:
            print("none")

        print('texture copy done')




def showWindow():
    win = MissingFilesWindow(parent=QtWidgets.QApplication.activeWindow())
    win.populate()
    win.show()

showWindow()