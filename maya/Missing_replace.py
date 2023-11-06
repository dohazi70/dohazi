import os
import maya.cmds as cmds
from PySide2 import QtWidgets, QtGui, QtCore

class MissingFilesWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MissingFilesWindow, self).__init__(parent)
        self.setWindowTitle("Missing Files")
        self.setGeometry(200, 200, 600, 400)
        self.buildUI()
        self.populate()

    def buildUI(self):
        layout = QtWidgets.QVBoxLayout(self)

        # Search and Replace layout
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

        # Table Widget
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['File Path', 'Status'])
        layout.addWidget(self.tableWidget)

        # Close Button
        closeBtn = QtWidgets.QPushButton("Close")
        closeBtn.clicked.connect(self.close)
        layout.addWidget(closeBtn)

    def populate(self):
        self.tableWidget.setRowCount(0)

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

                    if file_path and not os.path.exists(file_path):
                        row_position = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(row_position)
                        self.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(file_path))
                        item = QtWidgets.QTableWidgetItem("Not Found")
                        icon = QtGui.QIcon(":status_error.png")
                        item.setIcon(icon)
                        self.tableWidget.setItem(row_position, 1, item)

        self.tableWidget.resizeColumnsToContents()

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

        # Refresh the table
        self.populate()

def showWindow():
    try:
        for widget in QtWidgets.QApplication.allWidgets():
            if widget.objectName() == 'missingFilesWindow':
                widget.close()
    except:
        pass

    win = MissingFilesWindow(parent=QtWidgets.QApplication.activeWindow())
    win.setObjectName('missingFilesWindow')
    win.show()

showWindow()
