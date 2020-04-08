#

__title__ = "FreeCAD hFrame3DDfc library"
__author__ = "CeanWang@gmail.com" 

import FreeCAD,FreeCADGui
import os
import subprocess

class hFrame3DDfcRun:
	"hFrame3DDfcRun object"
	def GetResources(self):
        # return {'Pixmap': 'path_to_icon.svg', 'MenuText': 'my command', 'ToolTip': 'very short description'}
		return {"MenuText": "My Command run",
				"Accel": "Ctrl+R",
				"ToolTip": "Run Frame3DD to solve the case.",
				"Pixmap": os.path.dirname(__file__)+"./resources/template_resource.svg"
		}

	def IsActive(self):

		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True

	def Activated(self):

		process=subprocess.Popen(["frame3dd","hFrame3DDfc.3DD","hFrame3DDfc.out"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf8")
		out,err=process.communicate()
		print(out)
		print(err)


FreeCADGui.addCommand('hFrame3DDfcRun',hFrame3DDfcRun())