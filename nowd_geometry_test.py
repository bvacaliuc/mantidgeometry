# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

file1 = "NOWD_Definition_154x7.xml"
file2 = "NOWD_Definition_525x28.xml"

ws1 = CreateSampleWorkspace();
#inst1 = ws1.getInstrument();
#print("Default workspace has instrument: {0} with {1} parameters".format(inst1.getName(),len(inst1.getParameterNames())))
mon1 = LoadInstrument(ws1, Filename=file1, RewriteSpectraMap=True)
di1 = ws1.detectorInfo()
ci1 = ws1.componentInfo()
di1
ci1
inst1 = ws1.getInstrument();
print("Default workspace has instrument: {0} with {1} parameters".format(inst1.getName(),len(inst1.getParameterNames())))


ws2 = CreateSampleWorkspace();
mon2 = LoadInstrument(ws2, Filename=file2, RewriteSpectraMap=True)
di2 = ws2.detectorInfo()
ci2 = ws2.componentInfo()
di2
ci2
inst2 = ws2.getInstrument();
print("Default workspace has instrument: {0} with {1} parameters".format(inst2.getName(),len(inst2.getParameterNames())))
