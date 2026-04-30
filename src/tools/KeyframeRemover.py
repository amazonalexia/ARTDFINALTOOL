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
        currentTime = mc.currentTime(query=True)
        mc.cutKey(time=(currentTime), clear=True)

        currentFrame = mc.currentTime(query=True)
        selection = mc.ls(selection=True)
        print(f"Deleted keyframe(s) at frame: {currentTime}")

        if not selection:
            mc.warning("No objects selected.")
            return 
        deletedCount = 0

        for obj in selection:
            anim_curves = mc.listConnections(obj, type="animCurve") or []
            for curve in anim_curves:
                keyIndex = mc.keyframe(curve, query=True, time=(currentFrame, currentFrame), indexValue=True)
                if not keyIndex:
                    continue

                idx = keyIndex[0]
                prevVal = mc.keyframe(curve, query=True, index=(idx-1, idx-1), valueChange=True)
                currVal = mc.keyframe(curve, query=True, index=(idx, idx), valueChange=True)
                nextVal = mc.keyframe(curve, query=True, index=(idx+1, idx+1), valueChange=True)
                if prevVal and nextVal and currVal:
                    if abs(prevVal[0] - currVal[0]) < 1e-6 and abs(nextVal[0] - currVal[0]) < 1e-6:
                        mc.cutKey(curve, time=(currentFrame, currentFrame))
                        deletedCount += 1

        if deletedCount:
            mc.inViewMessage(amg=f"<hl>{deletedCount}</hl> flat key(s) deleted.", pos="midCenter", fade=True)
        else:
            mc.inViewMessage(amg="No flat keys found at current frame.", pos="midCenter", fade=True)


    def getPreviousKeyframe(self, frame):
        return mc.findKeyframe(t=(f"{frame}pal",), which="previous")
            

    def getNextKeyframe(self, frame):
        return mc.findKeyframe(t=(f"{frame+1}pal",), which="next")
    
    def deleteFlatKeyframeAtFrame(self, obj, frame):
        attrs = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']
        attrStatus = {}
        for attr in attrs:
            if not mc.listConnections(f"{obj}.{attr}", type='animCurve'):
                continue
            val_curr = mc.keyframe(obj, at=attr, q=True, time=(frame,), eval=True)[0]
                
            val_prev = mc.keyframe(obj, at=attr, q=True, time=(self.getPreviousKeyframe(frame),), eval=True)[0]
            val_next = mc.keyframe(obj, at=attr, q=True, time=(self.getNextKeyframe(frame),), eval=True)[0]
            
            if abs(val_curr - val_prev) < 0.001 and abs(val_curr - val_next) < 0.001:
                attrStatus[attr] = True
            else:
                attrStatus[attr] = False
                
        if all(attrStatus.values()) and len(attrStatus) > 0:
            mc.cutKey(obj, time=(frame,), option="keys")
            print(f"Keyframe removed on {obj} at frame {frame} (all channels flat).")
        else:
            print(f"Keyframe NOT removed on {obj} at frame {frame} (not all channels flat).")

    def GetKeyFrameNumbers(self, obj):
        keys = mc.keyframe(obj, query=True, timeChange=True)
        if not keys:
            return []
        keyNumbers = sorted(set(int(round(t)) for t in keys))
        return keyNumbers
    
    def deleteFlatKeyframe(self):
        selection = mc.ls(sl=True)

        if not selection:
            mc.warning("Please select an object.")
       
        obj = selection[0]
            
        currentTime = mc.currentTime(q=True)
        self.deleteFlatKeyframeAtFrame(obj, currentTime)
        
        
    def deleteAllFlatKeyframes(self):
        selection = mc.ls(sl=True)

        if not selection:
            mc.warning("Please select an object.")
        for curve in selection:
            keys = self.GetKeyFrameNumbers(curve)
            for key in keys:
                self.deleteFlatKeyframeAtFrame(curve, key)
            

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

        self.removeExcessKeyframesBtn = QPushButton("Remove Excess Keyframes On One Frame")
        self.removeExcessKeyframesBtn.clicked.connect(self.removeExcessKeyframesBtnClicked)
        self.infoLayout.addWidget(self.removeExcessKeyframesBtn)

        self.removeExcessKeyframesBtn = QPushButton("Remove Excess Keyframes Across All the Animation")
        self.removeExcessKeyframesBtn.clicked.connect(self.removeAllExcessKeyframesBtnClicked)
        self.infoLayout.addWidget(self.removeExcessKeyframesBtn)

    def removeExcessKeyframesBtnClicked(self):
        self.remover.deleteFlatKeyframe()
        print("Excess Keyframes Removed!")

    def removeAllExcessKeyframesBtnClicked(self):
        self.remover.deleteAllFlatKeyframes()
        print("Excess Keyframes Removed Across All of the Animation!")



def Run():
    keyframeRemoverWidget = KeyframeRemoverWidget()
    keyframeRemoverWidget.show()

Run()