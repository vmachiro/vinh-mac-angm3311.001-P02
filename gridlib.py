from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt


import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance

import maya.cmds as cmds
import houselib as hs

def get_maya_main_win():
    main_win = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_win), QtWidgets.QWidget)

class GridGenWin(QtWidgets.QDialog):
    def __init__(self):
        super().__init__(parent=get_maya_main_win())
        self.gridGen = Grid()
        self.setWindowTitle("Grid Generator")
        self.resize(500, 200)
        self._mk_main_layout()
        self._connect_signals()

    def _connect_signals(self):
        self.clear_btn.clicked.connect(self.clear)
        self.cancel_btn.clicked.connect(self.cancel)
        self.build_btn.clicked.connect(self.build)
        self.enable_grp_name_cb.stateChanged.connect(self.toggle_grpname)

    @QtCore.Slot()
    def toggle_grpname(self):
        is_custom_grpname_enabled = self.enable_grp_name_cb.isChecked()
        self.grp_name_ledit.setDisabled(not is_custom_grpname_enabled)

    @QtCore.Slot()
    def clear(self):
        cmds.select(cmds.ls(self.gridGen.grpname+"*"))        
        cmds.delete()

    @QtCore.Slot()
    def cancel(self):
        self.close()

    @QtCore.Slot()
    def build(self):
        self._update_grid_properties()
        self.gridGen.build()
    
    def _update_grid_properties(self):
        self.gridGen.__init__() # reset properties to default
        self.gridGen.population_scale = self.population_scale_spnbox.value()
        self.gridGen.number_of_houses = self.number_of_houses_spnbox.value()
        self.gridGen.grpname = self.grp_name_ledit.text()

    def _mk_main_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self._add_name_label()
        self._add_form_layout()
        self._mk_btn_layout()
        self.setLayout(self.main_layout)

    def _add_form_layout(self):
        self.form_layout = QtWidgets.QFormLayout()
        self._scale_pop()
        self._add_houses()
        self._add_custom_grpname()
        self.main_layout.addLayout(self.form_layout)    
    
    def _scale_pop(self):
        self.population_scale_spnbox = QtWidgets.QSpinBox()
        self.population_scale_spnbox.setValue(2)
        self.form_layout.addRow("Number of Rows", self.population_scale_spnbox)

    def _add_houses(self):
        self.number_of_houses_spnbox = QtWidgets.QSpinBox()
        self.number_of_houses_spnbox.setValue(1)
        self.form_layout.addRow("Number of Houses", self.number_of_houses_spnbox)

    def _add_custom_grpname(self):
        self.enable_grp_name_cb = QtWidgets.QCheckBox("Enable Custom Grid Name")
        self.grp_name_ledit = QtWidgets.QLineEdit("Grid")
        self.grp_name_ledit.setDisabled(True)
        self.form_layout.addRow(self.enable_grp_name_cb)
        self.form_layout.addRow("Group", self.grp_name_ledit)

    def _add_name_label(self):
        self.name_lbl = QtWidgets.QLabel("Grid Generator")
        self.name_lbl.setStyleSheet("background-color: blue;"
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


class Grid():
    def __init__(self):
        
        self.grpname = "grid"
        self.population_scale = 3
        self.number_of_houses = 1
        self.roads = 0 # for now, this just determines whether or not there are roads

    def create_plane(self, num_of_houses, house_width):
       
        scale = house_width*num_of_houses
        cmds.polyPlane(n='plane', sx=4, sy=4, w=(scale)*3, h=(scale)*2)

    #   for every population_scale, add another subdivision/scale the plane larger? 
    #   OR repeat the loop of creating and populating the plane with houses and shift the duplicate to the side

    def place_house(self):
        house1 = hs.House()
        house1.number_of_houses = self.number_of_houses
        house1.build()
        self.create_plane(house1.number_of_houses, house1.house_width)
        
    def rotate_house(self, house_x_pos):
        x_pos = house_x_pos*-1
        cmds.move( x_pos, x=True )

    def transform_window_to_back(self, window_z_pos):
        z_pos = window_z_pos*-1
        cmds.move( z_pos, z=True )

    def make_road(self):
        # TODO:
        # (LAST) define a method that puts a road on the map around the houses. 
        #   probably just a straight path for minimalization
        pass

    def transform_row(self, row):
        cmds.move( 10, z=True )
        cmds.makeIdentity(row, apply=True, translate=True, rotate=True, 
                            scale=True, normal=False, preserveNormals=True)

    def build(self):
        self.place_house()
        cmds.select( all=True )
        cmds.group( n='row' )

        for scale_num in range(self.population_scale):
            cmds.duplicate( 'row', st=True )
            cmds.select( all=True )
            world_pos = cmds.xform('row', query=True, worldSpace=True, translation=True)
                       
            if scale_num%2 != 0:
                self.rotate_house(world_pos[0])
            self.transform_row('row')

        cmds.select( all=True )
        cmds.group( n=self.grpname )

        

# POLISH:
# figure out house randomization
# user customizability of the houses comes after roads 
# GUI should call the house generator at some point with a button, so that the user can fine tune how the houses look

if __name__ == "__main__":
    pass