import maya.cmds as mc
from core.MayaWidget import MayaWidget
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QLineEdit

class KeyframeController:
    def __init__(self):
        controller = mc.ls(sl=True) [0]
        anim_curves = mc.listConnections(controller, t='animCurve')
        print(anim_curves)

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

def Run():
    limbRiggerWidget = KeyframeRemoverWidget()
    limbRiggerWidget.show()

Run()