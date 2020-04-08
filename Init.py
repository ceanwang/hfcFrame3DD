#

__title__ = "FreeCAD hFrame3DDfc library"
__author__ = "CeanWang@gmail.com" 

import FreeCAD

FreeCAD.addImportType("FEM result frame3DD (*.out)", "feminout.importFrame3DDResults")
FreeCAD.addImportType("FEM case frame3DD (*.3DD)", "feminout.importFrame3DDCase")