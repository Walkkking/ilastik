'''
Created on Oct 27, 2012

@author: fredo
'''
from lazyflow.graph import Operator,InputSlot, OutputSlot
import logging
#import NativeUtil as nativeOperations
from opCalcDepth import OpCalcDepth
from ilastik.utility import OperatorSubView


class LightfieldOperator(Operator):
    """
    @author: Frederik Claus
    @summary: Performs various operations on a lightfield
    """
    
    name="OpLightfield"
    
    InputImage = InputSlot()    
    outerScale = InputSlot()
    innerScale = InputSlot()

    Output = OutputSlot()
    
    logger = logging.getLogger(__name__)
    
    def __init__(self, *args, **kwargs):
        super(LightfieldOperator, self).__init__(*args, **kwargs)
        #=======================================================================
        # connect inputs
        #=======================================================================
        self.opDepth = OpCalcDepth(parent = self)
        self.opDepth.inputLF.connect(self.InputImage)
        self.opDepth.outerScale.connect(self.outerScale)
        self.opDepth.innerScale.connect(self.innerScale)
        #=======================================================================
        # connect outputs
        #=======================================================================
#        self.opDepth.outputLF.connect(self.Output)
        self.Output.connect(self.opDepth.outputLF)
        
    
    def setupOutputs(self):
        pass
        

        
    def execute(self, slot, subindex, roi, result):
        pass

    
    def propagateDirty(self, slot, subindex, roi):
        pass
    

    def addLane(self, laneIndex):
        numLanes = len(self.InputImage)
        assert numLanes == laneIndex, "Image lanes must be appended."        
        self.InputImage.resize(numLanes+1)
        
    def removeLane(self, laneIndex, finalLength):
        self.InputImage.removeSlot(laneIndex, finalLength)

    def getLane(self, laneIndex):
        return OperatorSubView(self, laneIndex)
         
        
    

        
        
        