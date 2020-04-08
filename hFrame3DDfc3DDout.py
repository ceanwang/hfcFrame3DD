#

__title__ = "FreeCAD hFrame3DDfc library"
__author__ = "CeanWang@gmail.com" 

import FreeCAD,FreeCADGui
import os


class Node:
    def __init__(self, id , x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.id = str(id)

# elmnt n1     n2    Ax     Asy     Asz     Jx     Iy     Iz     E     G     roll  density
class Member:
    def __init__(self, id , n1,n2):
        self.n1 = n1
        self.n2 = n2
        self.id = str(id)
		
def printChildren(objs = None, level = 0, baseline = ""):
    for cnt, obj in enumerate(objs,1):
#        print(baseline + " \_" + obj.Label + " {" + obj.TypeId.rsplit(':',1)[-1] + "} => ")
        print(baseline + " \_" + obj.Label + " {"+ "".join(filter(str.isalpha, obj.Name)) + "} => ")
        if cnt == len(objs):
            baselinechi = baseline +  "   "
        else:
            baselinechi = baseline + " | "
        printChildren(obj.ViewObject.claimChildren(), level+1, baselinechi)




class hFrame3DDfc3DDout:
	"hFrame3DDfc3DDout object"
	def GetResources(self):
        # return {'Pixmap': 'path_to_icon.svg', 'MenuText': 'my Result', 'ToolTip': 'very short description'}
		return {"MenuText": "Output 3DD file.",
				"Accel": "Ctrl+t",
				"ToolTip": "hFrame3DDfc3DDout",
				"Pixmap": os.path.dirname(__file__)+"./resources/filesave.svg"
		}

	def IsActive(self):

		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True

	def Activated(self):
	
		printChildren(FreeCADGui.Selection.getSelection())

FreeCADGui.addCommand('hFrame3DDfc3DDout',hFrame3DDfc3DDout())