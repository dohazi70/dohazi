import os
import json
import shutil

import ix

class EventReWire(ix.api.EventObject):
    def SearchDirectory(self, sender, evtid):
        home_path = os.path.expanduser('~')
        root_dir = ix.api.GuiWidget.open_folder(ix.application, home_path, 'save json file directory')
        rootPathLineEdit.set_text(root_dir)
    
    def ExportJson(self, sender, evtid):
        abc_type = ['GeometryBundleAlembic', 'GeometryAbcMesh']
        obj_type = ['GeometryPolyfile']
        mat_type = ['MaterialPhysicalStandard', 'MaterialPhysicalLayered', 'MaterialPhysicalDisneyPrincipled', 'MaterialPhysicalAutodeskStandardSurface']
        
        abc_mesh_name_list = []
        obj_mesh_name_list = []

        abc_sg_list = []
        obj_mat_list = []
        
        mat_full_path = []
        mat_list = []

        all_items = ix.api.OfObjectArray()
        ix.application.get_factory().get_all_objects(all_items)

        for i in range(all_items.get_count()):
            item = all_items[i]
            if item.get_type() in abc_type:
                abc_full_path = item.get_full_name()
                abc_clarisse_name = abc_full_path.split('/')

                geo = item.get_module()
                
                for j in range(geo.get_shading_group_count()):
                    if geo.get_shading_group(j) != 'default':
                        abc_mesh_name_list.append('SM_' + abc_clarisse_name[-1])
                        abc_sg_list.append(geo.get_shading_group(j))

            elif item.get_type() in obj_type:
                obj_full_path = item.get_full_name()
                obj_clarisse_name = obj_full_path.split('/')

                geo = item.get_module()

                for k in range(geo.get_shading_group_count()):
                    if str(geo.get_material(k).get_object()) != 'default://material' and geo.get_material(k).get_object().get_type() in mat_type:
                        obj_mesh_name_list.append('SM_' + obj_clarisse_name[-1])
                        obj_mat_list.append(geo.get_material(k).get_object())
                    else:
                        abc_mesh_name_list.append('SM_' + obj_clarisse_name[-1])
                        abc_sg_list.append(geo.get_shading_group(k))

            if item.get_type() in mat_type:
                mat_name = item.get_full_name()
                mat_full_path.append(mat_name)
                mat_name = mat_name.split('/')[-1]
                mat_list.append(mat_name)
            
        
        count_dict = {}
        mat_new_list = []

        for item in mat_list:
            if item in count_dict:
                count_dict[item] += 1
                new_item = '{0}_{1:02d}'.format(item, count_dict[item])
            elif mat_list.count(item) > 1:
                count_dict[item] = 0
                new_item = '{0}_{1:02d}'.format(item, count_dict[item])
            else:
                new_item = item
            mat_new_list.append(new_item)
            

        for idx ,rename in enumerate(mat_new_list):
            if mat_new_list.count(rename) <= 1:
                ix.cmds.RenameItem(mat_full_path[idx], rename)

        sl_items = ix.api.OfObjectArray()
        ix.application.get_factory().get_all_objects('ShadingLayer', sl_items)

        sl_filter_is_sg_name = []
        sl_material_full_path = []

        for i in range(sl_items.get_count()):
            sl_item = sl_items[i]
            sl_item_module_info = sl_item.get_module()
            for j in range(sl_item_module_info.get_rules().get_count()):
                active_filter = sl_item_module_info.get_rule_value(j, 'is_active')
                sl_filter = sl_item_module_info.get_rule_value(j, 'filter')          
                sl_material = sl_item_module_info.get_rule_value(j, 'material')
                if active_filter == '1' and sl_material and sl_material != 'default://material' and ix.get_item(sl_material).get_type() in mat_type:
                    sl_filter_is_sg_name.append(sl_filter)
                    sl_material_full_path.append(sl_material)

        
        sl_filter_is_abc_sg_name_split = []

        for i in sl_filter_is_sg_name:
            if '>' in i and  '*' not in i:
                sl_filter_is_abc_sg_name_split.append(i.split('>')[-1])

        remove_idx = []
        new_abc_sg_list = []

        for idx, value in enumerate(abc_sg_list):
            if value not in sl_filter_is_abc_sg_name_split:
                remove_idx.append(idx)
            else:
                new_abc_sg_list.append(value)
        
        for i in sorted(remove_idx, reverse=True):
            del abc_mesh_name_list[i]
        
        abc_sg_list = [value for idx, value in enumerate(abc_sg_list) if idx not in remove_idx]

        remove_idx = []
        new_sl_filter_is_abc_sg_name_split = []

        for idx, value in enumerate(sl_filter_is_abc_sg_name_split):
            if value not in abc_sg_list:
                remove_idx.append(idx)
            else:
                new_sl_filter_is_abc_sg_name_split.append(value)
        
        for i in sorted(remove_idx, reverse=True):
            del sl_material_full_path[i]
        
        sl_filter_is_abc_sg_name_split = [value for idx, value in enumerate(sl_filter_is_abc_sg_name_split) if idx not in remove_idx]


        new_abc_material_name_list = []
        new_abc_material_full_name_list = []

        for idx, value in enumerate(abc_sg_list):
            i = sl_filter_is_abc_sg_name_split.index(value)
            new_abc_material_full_name_list.insert(idx, sl_material_full_path[i])

        for i in new_abc_material_full_name_list:
            new_abc_material_name_list.append(i.split('/')[-1])
        
        new_obj_material_name_list = []

        for i in obj_mat_list:
            new_obj_material_name_list.append(str(i).split('/')[-1])

        
        abc_txt_file_name_list = []
        abc_uv_info_list = []

        for i, value in enumerate(new_abc_material_full_name_list):
            material = ix.get_item(value)
            if material.get_type() == 'MaterialPhysicalLayered':
                base = material.get_attribute('base')
                base_next_00 = ix.get_item(str(base.get_item())) 
                if base_next_00.get_type() == 'MaterialPhysicalStandard':
                    base_next_01 = base_next_00.get_attribute('diffuse_front_color')
                    txt_map_file01 = base_next_01.get_texture()
                    if txt_map_file01 is not None and txt_map_file01.get_type() in ['TextureMapFile', 'TextureStreamedMapFile']:
                        abc_txt_file_name_list.append(txt_map_file01.get_attribute('filename').get_string())
                        uv_constant = txt_map_file01.get_attribute('uv_scale').get_texture()
                        if uv_constant is not None and uv_constant.get_type() == 'TextureConstantColor':
                            abc_uv_info_list.append(txt_map_file01.get_attribute('uv_scale').get_texture().get_attribute('color').get_vec2d())
                        else:
                            abc_uv_info_list.append(txt_map_file01.get_attribute('uv_scale').get_vec2d())
                    else:
                        abc_txt_file_name_list.append('')
                        abc_uv_info_list.append((1,1))
                elif base_next_00.get_type() == 'MaterialPhysicalLayered':
                    base_next_01 = base_next_00.get_attribute('base')
                    base_next_02 = ix.get_item(str(base_next_01.get_item()))
                    if base_next_02.get_type() == 'MaterialPhysicalStandard':
                        base_next_03 = base_next_02.get_attribute('diffuse_front_color')
                        txt_map_file02 = base_next_03.get_texture()
                        if txt_map_file02 is not None and txt_map_file02.get_type() in ['TextureMapFile', 'TextureStreamedMapFile']:
                            abc_txt_file_name_list.append(txt_map_file02.get_attribute('filename').get_string())
                            uv_constant = txt_map_file02.get_attribute('uv_scale').get_texture()
                            if uv_constant is not None and uv_constant.get_type() == 'TextureConstantColor':
                                abc_uv_info_list.append(txt_map_file02.get_attribute('uv_scale').get_texture().get_attribute('color').get_vec2d())
                            else:
                                abc_uv_info_list.append(txt_map_file02.get_attribute('uv_scale').get_vec2d())
                        else:
                            abc_txt_file_name_list.append('')
                            abc_uv_info_list.append((1,1))
                elif base_next_00.get_type() in ['MaterialPhysicalDisneyPrincipled', 'MaterialPhysicalAutodeskStandardSurface']:
                    base_next_01 = base_next_00.get_attribute('base_color')
                    txt_map_file01 = base_next_01.get_texture()
                    if txt_map_file01 is not None and txt_map_file01.get_type() in ['TextureMapFile', 'TextureStreamedMapFile']: 
                        abc_txt_file_name_list.append(txt_map_file01.get_attribute('filename').get_string())
                        uv_constant = txt_map_file01.get_attribute('uv_scale').get_texture()
                        if uv_constant is not None and uv_constant.get_type() == 'TextureConstantColor':
                            abc_uv_info_list.append(txt_map_file01.get_attribute('uv_scale').get_texture().get_attribute('color').get_vec2d())
                        else:
                            abc_uv_info_list.append(txt_map_file01.get_attribute('uv_scale').get_vec2d())
                    else:
                        abc_txt_file_name_list.append('')
                        abc_uv_info_list.append((1,1))
            elif material.get_type() == 'MaterialPhysicalStandard':
                diffuse_clr = material.get_attribute('diffuse_front_color')
                txt_map_file = diffuse_clr.get_texture()
                if txt_map_file is not None and txt_map_file.get_type() in ['TextureMapFile', 'TextureStreamedMapFile']:
                    abc_txt_file_name_list.append(txt_map_file.get_attribute('filename').get_string())
                    uv_constant = txt_map_file.get_attribute('uv_scale').get_texture()
                    if uv_constant is not None and uv_constant.get_type() == 'TextureConstantColor':
                        abc_uv_info_list.append(txt_map_file.get_attribute('uv_scale').get_texture().get_attribute('color').get_vec2d())
                    else:
                        abc_uv_info_list.append(txt_map_file.get_attribute('uv_scale').get_vec2d())
                else:
                    abc_txt_file_name_list.append('')
                    abc_uv_info_list.append((1,1))
            elif material.get_type() in ['MaterialPhysicalDisneyPrincipled', 'MaterialPhysicalAutodeskStandardSurface']:
                base_clr = material.get_attribute('base_color')
                txt_map_file = base_clr.get_texture()
                if txt_map_file is not None and txt_map_file.get_type() in ['TextureMapFile', 'TextureStreamedMapFile']:
                    abc_txt_file_name_list.append(txt_map_file.get_attribute('filename').get_string())
                    uv_constant = txt_map_file.get_attribute('uv_scale').get_texture()
                    if uv_constant is not None and uv_constant.get_type() == 'TextureConstantColor':
                        abc_uv_info_list.append(txt_map_file.get_attribute('uv_scale').get_texture().get_attribute('color').get_vec2d())
                    else:
                        abc_uv_info_list.append(txt_map_file.get_attribute('uv_scale').get_vec2d())
                else:
                    abc_txt_file_name_list.append('')
                    abc_uv_info_list.append((1,1))
        
        obj_txt_file_name_list = []
        obj_uv_info_list = []

        for j, value in enumerate(obj_mat_list):
            material = value
            if material.get_type() == 'MaterialPhysicalLayered':
                base = material.get_attribute('base')
                base_next_00 = ix.get_item(str(base.get_item())) 
                if base_next_00.get_type() == 'MaterialPhysicalStandard':
                    base_next_01 = base_next_00.get_attribute('diffuse_front_color')
                    txt_map_file01 = base_next_01.get_texture()
                    if txt_map_file01 is not None and txt_map_file01.get_type() in ['TextureMapFile', 'TextureStreamedMapFile']:
                        obj_txt_file_name_list.append(txt_map_file01.get_attribute('filename').get_string())
                        uv_constant = txt_map_file01.get_attribute('uv_scale').get_texture()
                        if uv_constant is not None and uv_constant.get_type() == 'TextureConstantColor':
                            obj_uv_info_list.append(txt_map_file01.get_attribute('uv_scale').get_texture().get_attribute('color').get_vec2d())
                        else:
                            obj_uv_info_list.append(txt_map_file01.get_attribute('uv_scale').get_vec2d())
                    else:
                        obj_txt_file_name_list.append('')
                        obj_uv_info_list.append((1,1))
                elif base_next_00.get_type() == 'MaterialPhysicalLayered':
                    base_next_01 = base_next_00.get_attribute('base')
                    base_next_02 = ix.get_item(str(base_next_01.get_item()))
                    if base_next_02.get_type() == 'MaterialPhysicalStandard':
                        base_next_03 = base_next_02.get_attribute('diffuse_front_color')
                        txt_map_file02 = base_next_03.get_texture()
                        if txt_map_file02 is not None and txt_map_file02.get_type() in ['TextureMapFile', 'TextureStreamedMapFile']:
                            obj_txt_file_name_list.append(txt_map_file02.get_attribute('filename').get_string())
                            uv_constant = txt_map_file02.get_attribute('uv_scale').get_texture()
                            if uv_constant is not None and uv_constant.get_type() == 'TextureConstantColor':
                                obj_uv_info_list.append(txt_map_file02.get_attribute('uv_scale').get_texture().get_attribute('color').get_vec2d())
                            else:
                                obj_uv_info_list.append(txt_map_file02.get_attribute('uv_scale').get_vec2d())
                        else:
                            obj_txt_file_name_list.append('')
                            obj_uv_info_list.append((1,1))
                elif base_next_00.get_type() in ['MaterialPhysicalDisneyPrincipled', 'MaterialPhysicalAutodeskStandardSurface']:
                    base_next_01 = base_next_00.get_attribute('base_color')
                    txt_map_file01 = base_next_01.get_texture()
                    if txt_map_file01 is not None and txt_map_file01.get_type() in ['TextureMapFile', 'TextureStreamedMapFile']:
                        obj_txt_file_name_list.append(txt_map_file01.get_attribute('filename').get_string())
                        uv_constant = txt_map_file01.get_attribute('uv_scale').get_texture()
                        if uv_constant is not None and uv_constant.get_type() == 'TextureConstantColor':
                            obj_uv_info_list.append(txt_map_file01.get_attribute('uv_scale').get_texture().get_attribute('color').get_vec2d())
                        else:
                            obj_uv_info_list.append(txt_map_file01.get_attribute('uv_scale').get_vec2d())
                    else:
                        obj_txt_file_name_list.append('')
                        obj_uv_info_list.append((1,1))
            elif material.get_type() == 'MaterialPhysicalStandard':
                diffuse_clr = material.get_attribute('diffuse_front_color')
                txt_map_file = diffuse_clr.get_texture()
                if txt_map_file is not None and txt_map_file.get_type() in ['TextureMapFile', 'TextureStreamedMapFile']:
                    obj_txt_file_name_list.append(txt_map_file.get_attribute('filename').get_string())
                    uv_constant = txt_map_file.get_attribute('uv_scale').get_texture()
                    if uv_constant is not None and uv_constant.get_type() == 'TextureConstantColor':
                        obj_uv_info_list.append(txt_map_file.get_attribute('uv_scale').get_texture().get_attribute('color').get_vec2d())
                    else:
                        obj_uv_info_list.append(txt_map_file.get_attribute('uv_scale').get_vec2d())
                else:
                    obj_txt_file_name_list.append('')
                    obj_uv_info_list.append((1,1))
            elif material.get_type() in ['MaterialPhysicalDisneyPrincipled', 'MaterialPhysicalAutodeskStandardSurface']:
                base_clr = material.get_attribute('base_color')
                txt_map_file = base_clr.get_texture()
                if txt_map_file is not None and txt_map_file.get_type() in ['TextureMapFile', 'TextureStreamedMapFile']:
                    obj_txt_file_name_list.append(txt_map_file.get_attribute('filename').get_string())
                    uv_constant = txt_map_file.get_attribute('uv_scale').get_texture()
                    if uv_constant is not None and uv_constant.get_type() == 'TextureConstantColor':
                        obj_uv_info_list.append(txt_map_file.get_attribute('uv_scale').get_texture().get_attribute('color').get_vec2d())
                    else:
                        obj_uv_info_list.append(txt_map_file.get_attribute('uv_scale').get_vec2d())
                else:
                    obj_txt_file_name_list.append('')
                    obj_uv_info_list.append((1,1))
        
        abc_mesh_name_list.extend(obj_mesh_name_list)
        new_abc_material_name_list.extend(new_obj_material_name_list)
        abc_txt_file_name_list.extend(obj_txt_file_name_list)
        abc_uv_info_list.extend(obj_uv_info_list)

        
        for idx, value in enumerate(abc_txt_file_name_list):
            if value == '':
                del abc_txt_file_name_list[idx]
                del abc_mesh_name_list[idx]
                del new_abc_material_name_list[idx]
                del abc_uv_info_list[idx]
                idx -= 1

        uv_scale_x = []
        uv_scale_y = []

        for i in abc_uv_info_list:
            uv_scale_x.append(i[0])
            uv_scale_y.append(i[1])

        png_data_list = []

        for i in abc_txt_file_name_list:
            dir_name = os.path.dirname(i)

            project = ix.application.get_current_project_filename()
            project_name = os.path.splitext(project)[0]
            project_name = project_name.split('/')[-1]
            png_dir = os.path.join('/storenext/show/virtual/unreal_projects/Jaruwon/json', project_name)

            if not os.path.exists(png_dir):
                os.makedirs(png_dir)
                os.chmod(png_dir, 0o777)

            png_file_name = os.path.splitext(os.path.basename(i))[0] + '.png'

            if i is '':
                png_data = ''
            else:
                png_data = os.path.join(png_dir, png_file_name)

            file_name = os.path.basename(png_file_name)

            if '<UDIM>' in file_name:
                for j in os.listdir(dir_name):
                    ext = os.path.splitext(j)[-1]
                    if ext in ['.tx', '.tif']:
                        tx_origin_full_path = os.path.join(dir_name,j)

                        file_split = j.split('.')

                        if ext == '.tx':
                            png_full_path = '{0}/{1}.{2}.{3}'.format(png_dir, file_split[0], file_split[1], 'png')
                        elif ext == '.tif':
                            png_full_path = '{0}/{1}.{2}'.format(png_dir, file_split[0], 'png')

                        if not os.path.exists(png_full_path):
                            shutil.copyfile(tx_origin_full_path, png_full_path)
                            os.chmod(png_full_path, 0o777)

            elif not os.path.exists(png_data) and png_data != '':
                shutil.copyfile(i, png_data)
                os.chmod(png_data, 0o777)

            png_data_list.append(png_data)

        dict_list = []

        for i in range(len(abc_mesh_name_list)):
            item = {
                str(i): {
                    "mesh": abc_mesh_name_list[i],
                    "mat": new_abc_material_name_list[i],
                    "dif": png_data_list[i],
                    "x": str(uv_scale_x[i]),
                    "y": str(uv_scale_y[i])
                }
            }
            
            dict_list.append(item)

        root_dir = rootPathLineEdit.get_text()

        if root_dir:
            project = ix.application.get_current_project_filename()
            project_name = os.path.splitext(project)[0]
            project_name = project_name.split('/')[-1]

            json_file_path = '{0}{1}_mesh_info.json'.format(root_dir, project_name)
            with open(json_file_path, 'w') as file:
                json.dump(dict_list, file, indent=4)
            
            print('Work is Done.')
        else:
            print('Path is empty.')

    def CloseWindow(self, sender, evtid):
        sender.get_window().hide()


clarisse_win = ix.application.get_event_window()
window = ix.api.GuiWindow(clarisse_win, 900, 400, 400, 80)
window.set_title('Mesh Info Exporter')

panel = ix.api.GuiPanel(window, 0, 0, window.get_width(), window.get_height())
panel.set_constraints(ix.api.GuiWidget.CONSTRAINT_LEFT, ix.api.GuiWidget.CONSTRAINT_TOP,
                      ix.api.GuiWidget.CONSTRAINT_RIGHT, ix.api.GuiWidget.CONSTRAINT_BOTTOM)

rootPathLabel = ix.api.GuiLabel(panel, 10, 10, 150, 22, "Save Path")

rootPathLineEdit = ix.api.GuiLineEdit(panel, 160, 10, 235, 22)
rootPathLineEdit.set_constraints(ix.api.GuiWidget.CONSTRAINT_LEFT, ix.api.GuiWidget.CONSTRAINT_TOP, 
                              ix.api.GuiWidget.CONSTRAINT_RIGHT, rootPathLineEdit.get_height())

browseBtn = ix.api.GuiPushButton(panel, 80, 10, 70, 22, "Browse")

exportBtn = ix.api.GuiPushButton(panel, 245, 50, 70, 22, "Export")
exportBtn.set_constraints(exportBtn.get_x(), exportBtn.get_height() , 
                            ix.api.GuiWidget.CONSTRAINT_RIGHT, ix.api.GuiWidget.CONSTRAINT_BOTTOM)
cancelButton = ix.api.GuiPushButton(panel, 325, 50, 70, 22, "Cancel")
cancelButton.set_constraints(cancelButton.get_x(), cancelButton.get_height(), 
                             ix.api.GuiWidget.CONSTRAINT_RIGHT, ix.api.GuiWidget.CONSTRAINT_BOTTOM)

event_rewire = EventReWire()
event_rewire.connect(browseBtn, 'EVT_ID_PUSH_BUTTON_CLICK', event_rewire.SearchDirectory)
event_rewire.connect(exportBtn, 'EVT_ID_PUSH_BUTTON_CLICK', event_rewire.ExportJson)
event_rewire.connect(cancelButton, 'EVT_ID_PUSH_BUTTON_CLICK', event_rewire.CloseWindow)

window.show()
while window.is_shown():
    ix.application.check_for_events()
window.destroy()


'''
1. sl_filter_is_sg_name와 sl_material_list가 두 개의 구성이 완벽하게 같은 건 지워버린다. 리스트를 다시 구성한다.
2. abc의 shading group과 shading layer의 shading group에 이름이 일치하는지를 찾아서 일치하면 diffuse texture map file을 적어준다. 
3. sl_filter_is_sg_name와 sg_list를 비교해서 sg_list에 있는 중복 요소를 sl_material_list , sl_filter_is_sg_name에도 추가해준다.
4. texture map파일에서 경로를 찾도록 다 링크 값들을 뽑아낼 것
5. json파일로 정리

json 형식 예시
[
    {
    "0": {
        "mesh": "SM_a_mesh",
        "mat": "a_mtl",
        "dif": "a_diffuse.jpg",
        "x": "1",
        "y": "1"
        }
    },

    {"1": {
        "mesh": "SM_b_mesh",
        "mat": "b_mtl",
        "dif": "b_diffuse.jpg",
        "x": "1",
        "y": "1"
        }
    },
        
    {"2": {
        "mesh": "SM_c_mesh",
        "mat": "c_mtl",
        "dif": "c_diffuse.jpg",
        "x": "1",
        "y": "1"
        }
    },

    {"3": {
        "mesh": "SM_d_mesh",
        "mat": "d_mtl",
        "dif": "d_diffuse.jpg",
        "x": "1",
        "y": "1"
        }
    },

    {"4": {
        "mesh": "SM_d_mesh",
        "mat": "d_mtl",
        "dif": "d_diffuse.jpg",
        "x": "1",
        "y": "1"
        }
    }
]
'''





