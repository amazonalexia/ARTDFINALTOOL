import maya.cmds as mc
from core.MayaWidget import MayaWidget
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QLineEdit

class KeyframeController:
    def __init__(self):
        controller = mc.ls(sl=True) [0]
        anim_curves = mc.listConnections(controller, t='animCurve')
        print(anim_curves)
        
    def isAnimationCurveFlat(animCurve):
        if not mc.objExists():
            raise ValueError(f"Object '{animCurve}' does not exist.")

            values = mc.keyframe(anim_curve, query=True, valueChange=True)
            if not values:
                return True

            first_val = values[0]
            return all(abs(v - first_val) < 1e-6 for v in values)
        
    def deleteKeyAtCurrentTime(currentTime):
         current_time = mc.currentTime(query=True)
    mc.cutKey(time=(deleteKeyAtCurrentTime), clear=True)
    print(f"Deleted keyframe(s) at frame: {deleteKeyAtCurrentTime}")

    def Run():
         keyframeRemoverWidget = KeyframeRemoverWidget()
         keyframeRemoverWidget.show()
            
    Run()


class KeyframeRemoverWidget(MayaWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Keyframe Remover")
        self.remover = KeyframeController()
        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)
        self.masterLayout.addWidget(QLabel("Select the control in which extra keyframes should be removed:"))

        self.infoLayout = QHBoxLayout() 
        self.masterLayout.addLayout(self.infoLayout)
        self.infoLayout.addWidget(QLabel("Controller Name:"))

        self.nameKeyframeEdit = QLineEdit()
        self.infoLayout.addWidget(self.nameKeyframeEdit)

        self.removeExcessKeyframesBtn = QPushButton("Remove Excess Keyframes")
        self.removeExcessKeyframesBtn.clicked.connect(self.removeExcessKeyframesBtnClicked)
        self.infoLayout.addWidget(self.removeExcessKeyframesBtn)

    def removeExcessKeyframesBtnClicked(self):
                selected_objects = mc.ls(selection=True)   
                if selected_objects:
                    mc.cutKey(selected_objects, clear=True)
                print("Excess Keyframes Removed!")


def Run():
    limbRiggerWidget = KeyframeRemoverWidget()
    limbRiggerWidget.show()

Run()