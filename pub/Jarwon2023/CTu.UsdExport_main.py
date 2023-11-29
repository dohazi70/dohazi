import os

import ix

selection_list = []

class EventReWire(ix.api.EventObject):
    def SearchDirectory(self, sender, evtid):
        home_path = os.path.expanduser('~')
        root_dir = ix.api.GuiWidget.open_folder(ix.application, home_path, 'USD Directory')
        rootPathLineEdit.set_text(root_dir)

    def PlusContext(self, sender, evtid):
        select_item = ix.selection
        selection_name_list = []

        for i in range(select_item.get_count()):
            selection_name_list.append(select_item[i].get_name())
            selection_list.append(select_item[i])
            usdLayoutList.add_item(selection_name_list[i])

        del selection_name_list[:]

    def MinusContext(self, sender, evtid):
        select_index = usdLayoutList.get_selected_index()

        usdLayoutList.remove_item(select_index)
        del selection_list[select_index]

    def ExportUSD(self, sender, evtid):
        root_dir = rootPathLineEdit.get_text()
        if root_dir:
            export_ui = ix.item_exists("default://usd_export_ui")
            if export_ui == None:
                export_ui = ix.create_object("usd_export_ui", "UsdExportUI", ix.get_item("default:/"))
                export_ui.set_private(True)
                export_ui.set_static(True)
            
            for i in range(len(selection_list)):
                ix.selection.deselect_all()
                
                item_name = selection_list[i].get_full_name()
                ix.selection.add(item_name)

                usd_file_path = '{0}{1}.usd'.format(root_dir, usdLayoutList.get_item_name(i))
                export_ui.get_attribute('filename').set_string(usd_file_path)
                export_ui.call_action("export_context")

                print('usd export ----------- {0:04d}/{1:04d}'.format(i+1, len(selection_list)))

                export_ui.get_attribute('filename').set_string('')
                ix.selection.deselect_all()

            print('usd exporting is done')
        else:
            print('path is empty')

    def CloseWindow(self, sender, evtid):
        sender.get_window().hide()

clarisse_win = ix.application.get_event_window()
window = ix.api.GuiWindow(clarisse_win, 900, 400, 400, 330)
window.set_title('USD Exporter')

panel = ix.api.GuiPanel(window, 0, 0, window.get_width(), window.get_height())
panel.set_constraints(ix.api.GuiWidget.CONSTRAINT_LEFT, ix.api.GuiWidget.CONSTRAINT_TOP,
                      ix.api.GuiWidget.CONSTRAINT_RIGHT, ix.api.GuiWidget.CONSTRAINT_BOTTOM)

rootPathLabel = ix.api.GuiLabel(panel, 10, 10, 150, 22, "Save Path")

rootPathLineEdit = ix.api.GuiLineEdit(panel, 160, 10, 235, 22)
rootPathLineEdit.set_constraints(ix.api.GuiWidget.CONSTRAINT_LEFT, ix.api.GuiWidget.CONSTRAINT_TOP, 
                              ix.api.GuiWidget.CONSTRAINT_RIGHT, rootPathLineEdit.get_height())

browseBtn = ix.api.GuiPushButton(panel, 80, 10, 70, 22, "Browse")

plusBtn = ix.api.GuiPushButton(panel, 245, 40, 70, 22, "+")
plusBtn.set_constraints(plusBtn.get_x(), ix.api.GuiWidget.CONSTRAINT_TOP, 
                        ix.api.GuiWidget.CONSTRAINT_RIGHT, plusBtn.get_height())

minusBtn = ix.api.GuiPushButton(panel, 325, 40, 70, 22, "-")
minusBtn.set_constraints(minusBtn.get_x(), ix.api.GuiWidget.CONSTRAINT_TOP, 
                        ix.api.GuiWidget.CONSTRAINT_RIGHT, minusBtn.get_height())

usdLayoutListLabel = ix.api.GuiLabel(panel, 10, 65, 150 ,22, "usd layout name")

usdLayoutList = ix.api.GuiListView(panel,10, 90, 385, 200)
usdLayoutList.set_constraints(ix.api.GuiWidget.CONSTRAINT_LEFT, ix.api.GuiWidget.CONSTRAINT_TOP, 
                              ix.api.GuiWidget.CONSTRAINT_RIGHT, ix.api.GuiWidget.CONSTRAINT_BOTTOM)

exportBtn = ix.api.GuiPushButton(panel, 245, 300, 70, 22, "Export")
exportBtn.set_constraints(exportBtn.get_x(), exportBtn.get_height() , 
                            ix.api.GuiWidget.CONSTRAINT_RIGHT, ix.api.GuiWidget.CONSTRAINT_BOTTOM)
cancelButton = ix.api.GuiPushButton(panel, 325, 300, 70, 22, "Cancel")
cancelButton.set_constraints(cancelButton.get_x(), cancelButton.get_height(), 
                             ix.api.GuiWidget.CONSTRAINT_RIGHT, ix.api.GuiWidget.CONSTRAINT_BOTTOM)


event_rewire = EventReWire()
event_rewire.connect(browseBtn, 'EVT_ID_PUSH_BUTTON_CLICK', event_rewire.SearchDirectory)
event_rewire.connect(plusBtn, 'EVT_ID_PUSH_BUTTON_CLICK', event_rewire.PlusContext)
event_rewire.connect(minusBtn, 'EVT_ID_PUSH_BUTTON_CLICK', event_rewire.MinusContext)
event_rewire.connect(exportBtn, 'EVT_ID_PUSH_BUTTON_CLICK', event_rewire.ExportUSD)
event_rewire.connect(cancelButton, 'EVT_ID_PUSH_BUTTON_CLICK', event_rewire.CloseWindow)

window.show()
while window.is_shown():
    ix.application.check_for_events()
window.hide()