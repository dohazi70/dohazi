import os
from PySide2 import QtWidgets
import srncontroller
from srnview import FileRenamerView
from srnmodel import FileRenamerModel

app = QtWidgets.QApplication.instance()
if not app:
    app = QtWidgets.QApplication([])

model = FileRenamerModel()
view = FileRenamerView()
controller = srncontroller.FileRenamerController(model, view)
view.setLayout(view.layout)
view.show()

app.exec_()
