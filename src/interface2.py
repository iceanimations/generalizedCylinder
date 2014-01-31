import site
site.addsitedir(r"R:\Pipe_Repo\Users\Qurban\utilities")
from uiContainer import uic
from PyQt4.QtGui import *

site.addsitedir(r"R:\Pipe_Repo\Users\Hussain\packages")
import qtify_maya_window as qtfy

import os.path as osp
import sys

import polyRope as pr

selfPath = sys.modules[__name__].__file__
rootPath = osp.dirname(osp.dirname(selfPath))
uiPath = osp.join(rootPath, 'ui')
uiFile = osp.join(uiPath, 'window2.ui')

Form, Base = uic.loadUiType(uiFile)
class Window(Form, Base):
    def __init__(self, parent = qtfy.getMayaWindow()):
        super(Window, self).__init__(parent)
        self.setupUi(self)

        self.stop = False
        self.progressBar.hide()
        self.stopButton.hide()

        #connections
        self.createButton.clicked.connect(self.create)
        self.resetButton.clicked.connect(self.reset)
        self.stopButton.clicked.connect(self.setStop)

    def setStop(self):
        self.stop = True

    def create(self):
        selection = self.selectionButton.isChecked()
        curves = pr.pc.ls(sl = selection, type = 'nurbsCurve', dag = True,
                geometry = True)
        for curve in curves:
            if type(curve) != pr.pc.nt.NurbsCurve:
                curves.remove(curve)
        if not curves:
            if selection:
                pr.pc.warning("No curve selected")
            else:
                pr.pc.warning("No curve found in the scene")
            return
        self.progressBar.setMaximum(len(curves))
        self.progressBar.show()
        self.stopButton.show()
        self.createButton.hide()
        qApp.processEvents()
        done = []
        for curve in curves:
            pr.polyRope(curve, midSamplesPerLength=float(self.samplesPerLengthBox.value()),
                        midTwistRate=float(self.twistRateBox.value()),
                        midWidth=float(self.brushWidthBox.value()),
                        midRebuildSpansMult = 4,
                        midAdjustUVs=self.adjustUVsButton.isChecked(),
                        midCloseEnds=self.closeEndsButton.isChecked(),
                        numSideCyls=int(self.numOfCylindersBox.value()),
                        showMidCylinder=int(self.showButton.isChecked()),
                        sideSamplesPerLength=float(self.samplesPerLengthBox2.value()),
                        sideTwistRate=float(self.twistRateBox2.value()),
                        sideWidth=float(self.widthBox.value()),
                        sideRebuildSpansMult=4,
                        sideAdjustUVs=self.adjustUVsButton2.isChecked(),
                        sideCloseEnds=self.closeEndsButton2.isChecked(),
                        sideTubeSections=int(self.sectionsBox.value()))
            done.append(curve)
            self.progressBar.setValue(len(done))
            qApp.processEvents()
            if self.stop:
                self.stop = False
                break
        self.stopButton.hide()
        self.createButton.show()
        self.progressBar.hide()
        qApp.processEvents()


    def reset(self):
        self.selectionButton.setChecked(True)
        self.samplesPerLengthBox.setValue(2)
        self.twistRateBox.setValue(0.5)
        self.brushWidthBox.setValue(0.5)
        self.adjustUVsButton.setChecked(True)
        self.closeEndsButton.setChecked(True)
        self.showButton.setChecked(False)

        self.numOfCylindersBox.setValue(4)
        self.samplesPerLengthBox2.setValue(2)
        self.sectionsBox.setValue(4)
        self.twistRateBox2.setValue(1.0)
        self.widthBox.setValue(0.5)
        self.adjustUVsButton2.setChecked(True)
        self.closeEndsButton.setChecked(True)
