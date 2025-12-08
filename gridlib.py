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
        self.gridGen.build_grid()
    
    def _update_grid_properties(self):
        self.gridGen.__init__() # reset properties to default
        self.gridGen.number_of_rows = self.number_of_rows_spnbox.value()
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
        self.number_of_rows_spnbox = QtWidgets.QSpinBox()
        self.number_of_rows_spnbox.setValue(2)
        self.form_layout.addRow("Number of Rows", self.number_of_rows_spnbox)

    def _add_houses(self):
        self.number_of_houses_spnbox = QtWidgets.QSpinBox()
        self.number_of_houses_spnbox.setValue(1)
        self.number_of_houses_spnbox.setMinimum(1)
        self.number_of_houses_spnbox.setMaximum(8)
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
        self.number_of_rows = 3
        self.number_of_houses = 1

    #   for every number_of_rows, add another subdivision/scale the plane larger? 
    #   OR repeat the loop of creating and populating the plane with houses and shift the duplicate to the side

    def place_house(self):
        house1 = hs.House()
        house1.number_of_houses = self.number_of_houses
        house1.build()
        
    def rotate_house(self, house_z_pos):
        z_pos = house_z_pos*-1
        cmds.move( z_pos, z=True )

    def transform_row(self):
        cmds.move( 10, z=True )

    def build_grid(self):
        self.place_house()
        cmds.select( all=True )
        cmds.group( n='row' )

        for scale_num in range(self.number_of_rows-1):
            cmds.duplicate( st=True )
            self.transform_row()
            cmds.makeIdentity('row', apply=True, translate=True, rotate=True, 
                            scale=True, normal=False, preserveNormals=True)
         
        cmds.select( all=True )
        cmds.group( n=self.grpname )

# POLISH:
# figure out house randomization
# GUI should call the house generator at some point with a button, so that the user can fine tune how the houses look

if __name__ == "__main__":
    pass