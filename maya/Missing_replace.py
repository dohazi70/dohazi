import os
import maya.cmds as cmds
import shutil
from PySide2 import QtGui, QtWidgets

class MissingFilesWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MissingFilesWindow, self).__init__(parent)
        self.setWindowTitle("File Status")
        self.setGeometry(200, 200, 1200, 1200)
        self.buildUI()

    def buildUI(self):
        layout = QtWidgets.QVBoxLayout(self)

        searchReplaceLayout = QtWidgets.QHBoxLayout()
        layout.addLayout(searchReplaceLayout)
        copyLayout = QtWidgets.QHBoxLayout()
        layout.addLayout(copyLayout)

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

        tifButton = QtWidgets.QPushButton("tif")
        tifButton.clicked.connect(self.tifs)
        copyLayout.addWidget(tifButton)

        udimset = QtWidgets.QPushButton("UDIM")
        udimset.clicked.connect(self.udimset)
        searchReplaceLayout.addWidget(udimset)

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

    def udimset(self):
        texture_nodes = cmds.ls(type='file')
        unique_paths = set()
        file_name_last = []
        duplicate_names = []
        unique_names = []

        for node in texture_nodes:
            path = cmds.getAttr(f"{node}.fileTextureName")
            parts = path.split("/")
            if len(parts) > 1:
                unique_paths.add("/".join(parts[:-1]))
                
            file_name = os.path.basename(path)
            file_name_without_extension, extension = os.path.splitext(file_name)
            
            if file_name_without_extension and file_name_without_extension[-1].isdigit():
                processed_name = file_name_without_extension[:-4]
                file_name_last.append(processed_name)
            else:
                file_name_last.append(file_name_without_extension)

        for name in file_name_last:
            if file_name_last.count(name) > 1:
                duplicate_names.append(name)
            else:
                unique_names.append(name)

        texture_nodes = cmds.ls(type='file')

        for node in texture_nodes:
            path = cmds.getAttr(f"{node}.fileTextureName")
            if any(name in path for name in duplicate_names):
                print(f"uv: {node}")
                cmds.setAttr(f"{node}.uvTilingMode", 3)
                cmds.setAttr(f"{node}.uvTileProxyQuality", 1)
            else:
                print(f"none: {node}")
                cmds.setAttr(f"{node}.uvTilingMode", 0)
        self.populate()
    
    def tifs(self):
        file_nodes = cmds.ls(type='file')
        for f in file_nodes:
            current_path = cmds.getAttr(f + '.fileTextureName')
            file_name = os.path.basename(current_path)
            new_path = './tif/' + file_name
            cmds.setAttr(f + '.fileTextureName', new_path, type='string')
        self.populate()

    def copy_files(self):
        destination_directory = self.copyLineEdit.text()
        ass_nodes = cmds.ls(type='aiStandIn')
        texture_nodes = cmds.ls(type='file')
        ass_file_paths = []
        valid_file_names = set()
        unique_paths = set()
##ass
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

##files
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
                                index += 1  # 인덱스 증가
                            except Exception as e:
                                print(f"[{index}/{total_files}] Error copying {source_path}: {e}")

        print('done')




def showWindow():
    win = MissingFilesWindow(parent=QtWidgets.QApplication.activeWindow())
    win.populate()
    win.show()

showWindow()