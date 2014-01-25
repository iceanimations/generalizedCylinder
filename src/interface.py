import site
site.addsitedir(r"R:\Pipe_Repo\Users\Qurban\utilities")
from uiContainer import uic
from PyQt4.QtGui import *

site.addsitedir(r"R:\Pipe_Repo\Users\Hussain\packages")
import qtify_maya_window as qtfy

import os.path as osp
import sys

import generalizedCylinder as gc

selfPath = sys.modules[__name__].__file__
rootPath = osp.dirname(osp.dirname(selfPath))
uiPath = osp.join(rootPath, 'ui')
uiFile = osp.join(uiPath, 'window.ui')

Form, Base = uic.loadUiType(uiFile)
class Window(Form, Base):
    def __init__(self, parent = qtfy.getMayaWindow()):
        super(Window, self).__init__(parent)
        self.setupUi(self)
        
        self.twistRateBox.setValue(0.5)
        
        #connections
        self.createButton.clicked.connect(self.create)
        self.resetButton.clicked.connect(self.reset)
        
    def create(self):
        selection = self.selectionButton.isChecked()
        print selection
        curves = gc.pc.ls(sl = selection, type = 'nurbsCurve',
                          dag = True, geometry = True)
        if not curves:
            if selection:
                gc.pc.warning("No curve selected")
            else:
                gc.pc.warning("No curve found in the scene")
            return
        samples = int(self.samplesPerLengthBox.value())
        sections = int(self.tubeSectionsBox.value())
        tRate = float(self.twistRateBox.value())
        bWidth = float(self.brushWidthBox.value())
        for curve in curves:
            gc.generalizedCylinder(curve, samplesPerLength=samples,
                                   tubeSections=sections,
                                   twistRate=tRate,
                                   brushWidth=bWidth)
    
    def reset(self):
        self.selectionButton.setChecked(True)
        self.samplesPerLengthBox.setValue(2)
        self.tubeSectionsBox.setValue(4)
        self.twistRateBox.setValue(0.5)
        self.brushWidthBox.setValue(0.5)