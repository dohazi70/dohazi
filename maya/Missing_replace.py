import os
import maya.cmds as cmds
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

        searchReplaceLayout.addWidget(QtWidgets.QLabel("Search:"))
        self.searchLineEdit = QtWidgets.QLineEdit()
        searchReplaceLayout.addWidget(self.searchLineEdit)

        searchReplaceLayout.addWidget(QtWidgets.QLabel("Replace:"))
        self.replaceLineEdit = QtWidgets.QLineEdit()
        searchReplaceLayout.addWidget(self.replaceLineEdit)

        replaceButton = QtWidgets.QPushButton("Replace Paths")
        replaceButton.clicked.connect(self.replacePaths)
        searchReplaceLayout.addWidget(replaceButton)

        udimset = QtWidgets.QPushButton("UDIM_1K")
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

    def udimset():
        texture_nodes = cmds.ls(type='file')
        for texture_node in texture_nodes:
            try:
                cmds.setAttr(f"{texture_node}.uvTilingMode", 3)
                cmds.setAttr(f"{texture_node}.uvTileProxyQuality", 1)
            except: print(f"Error setting resolution for")

def showWindow():
    win = MissingFilesWindow(parent=QtWidgets.QApplication.activeWindow())
    win.populate()
    win.show()

showWindow()

