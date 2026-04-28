import maya.cmds as mc
from core.MayaWidget import MayaWidget
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QLineEdit

class KeyframeController:
    def __init__(self):
        controller = mc.ls(sl=True) [0]
        anim_curves = mc.listConnections(controller, t='animCurve')
        print(anim_curves)
        
    def isAnimationCurveFlat(self, animCurve):
        if not mc.objExists():
            raise ValueError(f"Object '{animCurve}' does not exist.")

        values = mc.keyframe(animCurve, query=True, valueChange=True)
        if not values:
            return True

        first_val = values[0]
        return all(abs(v - first_val) < 1e-6 for v in values)
        
    def deleteKeyAtCurrentTime(self, currentTime):
        current_time = mc.currentTime(query=True)
        mc.cutKey(time=(current_time), clear=True)
        print(f"Deleted keyframe(s) at frame: {current_time}")

    def deleteFlatKeyframe(self):
        selection = mc.ls(sl=True)

        if not selection:
            mc.warning("Please select an object.")
       
    
        obj = selection[0]
        return
        
    obj = deleteFlatKeyframe(self = deleteFlatKeyframe)
        
    currentTime = mc.currentTime(q=True)
    attrs = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
    attrStatus = {}
    for attr in attrs:
        if not mc.listConnections(f"{obj}.{attr}", type='animCurve'):
             continue
        val_curr = mc.keyframe(obj, at=attr, q=True, t=(currentTime,), eval=True)[0]
        
       
        prev_keys = mc.keyframe(obj, at=attr, q=True, t=(currentTime,), tcli=True, prev=True)
        
        next_keys = mc.keyframe(obj, at=attr, q=True, t=(currentTime,), tcli=True, next=True)
        
        if not prev_keys or not next_keys:
            
            attrStatus[attr] = False
            continue
            
        val_prev = mc.keyframe(obj, at=attr, q=True, t=(prev_keys[0],), eval=True)[0]
        val_next = mc.keyframe(obj, at=attr, q=True, t=(next_keys[0],), eval=True)[0]
        
        if abs(val_curr - val_prev) < 0.001 and abs(val_curr - val_next) < 0.001:
            attrStatus[attr] = True
        else:
            attrStatus[attr] = False
            
    if all(attrStatus.values()) and len(attrStatus) > 0:
        mc.cutKey(obj, t=(currentTime,), option="keys")
        print(f"Keyframe removed on {obj} at frame {currentTime} (all channels flat).")
    else:
        print(f"Keyframe NOT removed on {obj} at frame {currentTime} (not all channels flat).")

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