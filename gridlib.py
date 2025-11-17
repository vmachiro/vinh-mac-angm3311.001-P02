from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt


import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance

import maya.cmds as cmds
import houselib as hs

def get_maya_main_win():
    main_win = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_win), QtWidgets.QWidget)

# build a second GUI to be utilized that focuses on the map parameters rather than the house parameters.
class GridGenWin(QtWidgets.QDialog):
    def __init__(self):
        # runs the init code of the parent QDialog class
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

    def _mk_main_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self._add_name_label()
        self._add_form_layout()
        self._mk_btn_layout()
        self.setLayout(self.main_layout)

    def _add_name_label(self):
        self.name_lbl = QtWidgets.QLabel("Grid Generator")
        self.name_lbl.setStyleSheet("background-color: blue;"
                                    "color: white;"
                                    "font: bold 24px;")
        self.name_lbl.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.name_lbl)

    def _add_form_layout(self):
        self.form_layout = QtWidgets.QFormLayout()
        
        self.main_layout.addLayout(self.form_layout)

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
        # input most basic parameters to build the grid of houses
        # population of houses since we already have number of houses? roads
        
        self.population_scale = 1 # this determines how many houses are on each square/grid
        self.roads = 0 # for now, this just determines whether or not there are roads

    def create_plane(self):
        cmds.plane( p=(1, 1, 1), s=10 )
    #   transform the plane to be on level with the houses. or vice versa
    #   for every population_scale, add another subdivision/scale the plane larger? 
    #   OR repeat the loop of creating and populating the plane with houses and shift the duplicate to the side

    def place_house(self):
        house1 = hs.House()
        house1.number_of_houses = 3
        house1.build()

    def rotate_house(self):
        # TODO:
        # define a method that flips the groups of houses to face different directions
        #   can probably reuse the window rotation code
        pass

    def make_road(self):
        # TODO:
        # (LAST) define a method that puts a road on the map around the houses. 
        #   probably just a straight path for minimalization
        pass

    def build(self):
        self.create_plane()

        grid_list= []

        for scale_num in range(self.population_scale):
            self.place_house()
            # transform if needed

            grid_list.append()
            # rotate if necessary
            # (polish) add roads

        cmds.group(grid_list, name=Grid)

        cmds.makeIdentity(grid_list, apply=True, translate=True, rotate=True, 
                            scale=True, normal=False, preserveNormals=True)


# POLISH:
# figure out house randomization
# user customizability of the houses comes after roads 
# GUI should call the house generator at some point with a button, so that the user can fine tune how the houses look

if __name__ == "__main__":
    pass