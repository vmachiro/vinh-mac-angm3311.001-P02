from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt


import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance


import random
import maya.cmds as cmds


def get_maya_main_win():
    main_win = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_win), QtWidgets.QWidget)

class HouseGenWin(QtWidgets.QDialog):
    """House Window Class"""

    def __init__(self):
        # runs the init code of the parent QDialog class
        super().__init__(parent=get_maya_main_win())
        self.houseGen = House()
        self.setWindowTitle("House Generator")
        self.resize(500, 200)
        self._mk_main_layout()
        self._connect_signals()

    def _connect_signals(self):
        self.number_of_floors_slider.valueChanged.connect(self._update_floors)
        self.wall_height_slider.valueChanged.connect(self._update_walls)        
        self.roof_height_slider.valueChanged.connect(self._update_roof)        
        self.enable_grp_name_cb.stateChanged.connect(self.toggle_grpname)
        self.enable_rand_cb.stateChanged.connect(self.toggle_random)
        self.clear_btn.clicked.connect(self.clear)
        self.cancel_btn.clicked.connect(self.cancel)
        self.build_btn.clicked.connect(self.build)

    def _update_floors(self, value):
        self.floor_result_lbl.setText(f'Current Value: {value}')
    
    def _update_walls(self, value):
        self.wall_result_lbl.setText(f'Current Value: {value}')

    def _update_roof(self, value):
        self.roof_result_lbl.setText(f'Current Value: {value}')

    @QtCore.Slot()
    def toggle_grpname(self):
        is_custom_grpname_enabled = self.enable_grp_name_cb.isChecked()
        self.grp_name_ledit.setDisabled(not is_custom_grpname_enabled)
    
    @QtCore.Slot()
    def toggle_random(self):
        is_random_houses_enabled = self.enable_rand_cb.isChecked()
        self.number_of_floors_slider.setDisabled(is_random_houses_enabled)
        return is_random_houses_enabled

    @QtCore.Slot()
    def clear(self):
        cmds.select(cmds.ls(self.houseGen.housename+"*"))        
        cmds.delete()

    @QtCore.Slot()
    def cancel(self):
        self.close()

    @QtCore.Slot()
    def build(self):
        self._update_housegen_properties()
        self.houseGen.build()

    def _update_housegen_properties(self):
        self.houseGen.__init__() # reset properties to default
        self.houseGen.number_of_houses = self.number_of_houses_spnbox.value()
        self.houseGen.roof_height = self.roof_height_slider.value()        
        self.houseGen.wall_height = self.wall_height_slider.value()
        self.houseGen.number_of_floors = self.number_of_floors_slider.value()
        self.houseGen.number_of_windows = self.number_of_windows_spnbox.value()
        self.houseGen.number_of_doors = self.door_spnbox.value()
        self.houseGen.housename = self.grp_name_ledit.text()

        if self.toggle_random() == True:
            random_floor_num = random.randint(1,5)
            self.houseGen.number_of_floors = random_floor_num

    def _mk_main_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self._add_name_label()
        self._add_form_layout()
        self._mk_btn_layout()
        self.setLayout(self.main_layout)

    def _add_form_layout(self):
        self.form_layout = QtWidgets.QFormLayout()
        self._add_houses()
        self._add_roof_height()
        self._add_wall_height()
        self._add_floors()     
        self._add_randomization()        
        self._add_windows()
        self._add_doors()
        self._add_custom_grpname()
        self.main_layout.addLayout(self.form_layout)

    def _add_randomization(self):
        self.enable_rand_cb = QtWidgets.QCheckBox("Choose floors for me!")
        self.form_layout.addRow(self.enable_rand_cb)

    def _add_houses(self):
        self.number_of_houses_spnbox = QtWidgets.QSpinBox()
        self.number_of_houses_spnbox.setValue(1)
        self.form_layout.addRow("Number of Houses", self.number_of_houses_spnbox)

    def _add_custom_grpname(self):
        self.enable_grp_name_cb = QtWidgets.QCheckBox("Enable Custom House Name")
        self.grp_name_ledit = QtWidgets.QLineEdit("House")
        self.grp_name_ledit.setDisabled(True)
        self.form_layout.addRow(self.enable_grp_name_cb)
        self.form_layout.addRow("Group", self.grp_name_ledit)

    def _add_windows(self):
        self.number_of_windows_spnbox = QtWidgets.QSpinBox()
        self.number_of_windows_spnbox.setValue(2)
        self.number_of_windows_spnbox.setMaximum(4)
        self.form_layout.addRow("Windows per floor", self.number_of_windows_spnbox)

    def _add_floors(self):
        self.number_of_floors_slider = QtWidgets.QSlider(Qt.Orientation.Horizontal, self)
        self.number_of_floors_slider.setRange(1,10)
        self.number_of_floors_slider.setValue(1)    
        self.form_layout.addRow("Number of Floors", self.number_of_floors_slider)

        self.floor_result_lbl = QtWidgets.QLabel('', self)
        self.floor_result_lbl.setAlignment(Qt.AlignCenter)
        self.form_layout.addRow(self.floor_result_lbl)

    def _add_roof_height(self):
        self.roof_height_slider = QtWidgets.QSlider(Qt.Orientation.Horizontal, self)
        self.roof_height_slider.setRange(0,5)
        self.roof_height_slider.setValue(1)          
        self.form_layout.addRow("Roof Height", self.roof_height_slider)

        self.roof_result_lbl = QtWidgets.QLabel('', self)
        self.roof_result_lbl.setAlignment(Qt.AlignCenter)
        self.form_layout.addRow(self.roof_result_lbl)

    def _add_doors(self):
        self.door_spnbox = QtWidgets.QSpinBox()
        self.door_spnbox.setValue(1)
        self.door_spnbox.setRange(0,2)
        self.form_layout.addRow("Door Number", self.door_spnbox)

    def _add_wall_height(self):
        self.wall_height_slider = QtWidgets.QSlider(Qt.Orientation.Horizontal, self)
        self.wall_height_slider.setValue(5)
        self.wall_height_slider.setRange(5,20)
        self.form_layout.addRow("Wall Height", self.wall_height_slider)

        self.wall_result_lbl = QtWidgets.QLabel('', self)        
        self.wall_result_lbl.setAlignment(Qt.AlignCenter)
        self.form_layout.addRow(self.wall_result_lbl)

    def _add_name_label(self):
        self.name_lbl = QtWidgets.QLabel("House Generator")
        self.name_lbl.setStyleSheet("background-color: purple;"
                                    "color: white;"
                                    "font: bold 24px;")
        self.name_lbl.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.name_lbl)

    def _mk_btn_layout(self):
        self.btn_layout = QtWidgets.QHBoxLayout()
        self.build_btn = QtWidgets.QPushButton("Build")
        self.clear_btn = QtWidgets.QPushButton("Clear all houses")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.btn_layout.addWidget(self.build_btn)
        self.btn_layout.addWidget(self.clear_btn)
        self.btn_layout.addWidget(self.cancel_btn)
        self.main_layout.addLayout(self.btn_layout)

class House():

    def __init__(self):
        self.number_of_houses = 1
        self.number_of_floors = 2        
        self.wall_height = 8 
        self.house_width = 8
        self.roof_height = 1 
        self.number_of_windows = 4
        self.number_of_doors = 1
        self.housename = "House"
    
    def get_height_of_house(self):
        return self.wall_height * self.number_of_floors

    def get_curent_floor(self, floor_num):
        return self.wall_height*(floor_num)

    def get_base_of_house(self):
        base_height = self.wall_height/self.get_height_of_house() * self.number_of_floors
        return base_height

    def get_window_height_from_base(self):
        window_placement = self.wall_height/self.get_height_of_house() + (self.wall_height/2)
        return window_placement

    def get_center_of_wall(self):
        return self.house_width/2
    
    def mkhousebody(self):
        xform, shape = cmds.polyCube(height= self.get_height_of_house(),
                                    width = self.house_width,
                                    depth = self.house_width,
                                    name = "housebody")
        
        cmds.xform(xform, translation = [0,self.get_height_of_house()/2,0])          
        
        return xform

    def mkwindows(self):
        window_GRP = []

        for floor_num in range(self.number_of_floors):
            for windows_num in range(self.number_of_windows):
                xform, shape = cmds.polyCube(height= 2,
                                            width = 1,
                                            depth = 0.5,
                                            name = "window"+str(windows_num))
                
                self.transform_window(xform)
                world_pos = cmds.xform(xform, query=True, worldSpace=True, translation=True)

                if self.number_of_windows > 2:
                    if windows_num > 1:
                        cmds.xform( r=True, ro=(0,90,0) )
                        x_pos = world_pos[2] 
                        cmds.move( x_pos, x=True )

                        z_pos = world_pos[0]
                        cmds.move( z_pos, z=True )

                        if windows_num%2 == 1:
                            cmds.move( x_pos*-1, x=True )
                            cmds.move( z_pos*-1, z=True )
                    
                    world_pos = cmds.xform(xform, query=True, worldSpace=True, translation=True)

                if windows_num%2 == 1:
                    self.transform_window_to_back(world_pos[2])        
                    world_pos = cmds.xform(xform, query=True, worldSpace=True, translation=True)

                if floor_num > 0:
                    self.transform_window_up(floor_num, xform, world_pos) 
                
                window_GRP.append(xform)  

        return window_GRP

    def transform_window_up(self, floor_num, xform, world_pos):
        pos = [world_pos[0], (world_pos[1]+(self.get_curent_floor(floor_num))), world_pos[2]]
        cmds.xform( xform, translation=pos )

    def transform_window(self, window):
        z_pos = self.get_center_of_wall()
        y_pos = self.get_window_height_from_base()
        pos = [0, y_pos, z_pos]

        cmds.xform(window, translation=pos)

    def transform_window_to_back(self, window_z_pos):
        z_pos = window_z_pos*-1

        cmds.move( z_pos, z=True )

    def mkdoors(self):
        door_GRP = []        
        
        for door_num in range(self.number_of_doors):
            xform, shape = cmds.polyCube(height= self.wall_height/4,
                                        width = self.house_width/10,
                                        depth = .5,
                                        name = "door"+str(door_num))
            
            self.transform_door(xform)
            
            if door_num > 0:
                self.transform_door_to_back(xform)
            
            door_GRP.append(xform)
        
        return door_GRP

    def mkhouseflatroof(self):
        xform, shape = cmds.polyCube(height= self.roof_height,
                                    width = self.house_width*1.25,
                                    depth = self.house_width*1.25,
                                    name = "roof")

        cmds.xform(xform, translation = [0,self.get_height_of_house(),0])

        return xform
    
    def transform_door(self, door):
        z_pos = self.get_center_of_wall()
        y_pos = self.get_base_of_house()*.7
        pos = [0, y_pos, z_pos]

        cmds.xform(door, translation=pos)

    def transform_door_to_back(self, door):
        z_pos = self.get_center_of_wall()
        y_pos = self.get_base_of_house()
        pos = [0, y_pos, z_pos*-1]

        cmds.xform(door, translation=pos)

    def transform_house(self, house_x_pos, house_num, housename):
        x_pos = house_x_pos + self.house_width*house_num*1.5

        cmds.move( x_pos, housename, x=True )

    def build(self):

        house_things = []

        for house_num in range(self.number_of_houses):
            house_name = self.housename+str(house_num) 

            housebody = self.mkhousebody()
            house_things.append(housebody)

            if self.roof_height != 0:
                houseroof = self.mkhouseflatroof()
                house_things.append(houseroof)
            
            cmds.group(house_things, name=house_name)
            house_things.clear()

            doors_grp = self.mkdoors()
            cmds.group(doors_grp, name="doors_GRP", parent=house_name)
            
            windows_grp = self.mkwindows()
            cmds.group(windows_grp, name="windows_GRP", parent=house_name)
            
            world_pos = cmds.xform(house_name, query=True, worldSpace=True, translation=True)
      
            self.transform_house(world_pos[0],house_num,house_name)
            
            cmds.makeIdentity(house_name, apply=True, translate=True, rotate=True, 
                            scale=True, normal=False, preserveNormals=True)
            

if __name__ == "__main__":
    pass
     