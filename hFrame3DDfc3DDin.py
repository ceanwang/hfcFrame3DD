#

__title__ = "FreeCAD hFrame3DDfc library"
__author__ = "CeanWang@gmail.com" 

import FreeCAD,FreeCADGui
import os
import shutil

import PySide
from PySide import QtGui ,QtCore
from PySide.QtGui import *
from PySide.QtCore import *

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

def moveon(fp):	
	while 1:
		line = fp.readline().strip()
		if len(line)==0 or line[0]=='#':
			continue
		else:
			return line
				

class hFrame3DDfc3DDin:
	"Frame3DDfc3DDin"
	def GetResources(self):
        # return {'Pixmap': 'path_to_icon.svg', 'MenuText': 'my 3DDViewer', 'ToolTip': 'very short description'}
		return {"MenuText": "hFrame3DDfc3DDin",
				"Accel": "Ctrl+t",
				"ToolTip": "hFrame3DDfc3DDin",
				"Pixmap": os.path.dirname(__file__)+"./resources/folderIcon.svg"
		}

	def IsActive(self):

		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True
			

	def Activated(self):
	
		from FreeCAD import Base
		import Draft
		#import re
		#import math
		#import sys
		
		

		NodeList = {}
		MemberList = {}                                  

		ProjectDescription = ''

		numNode = 0

		#factor = 25.42
		factor = 1

		path = 'c:\\Frame3DD-master\\examples\\'
		try:
			fName = QFileDialog.getOpenFileName(None,QString.fromLocal8Bit("Read a Frame3DD's 3DD file"),path, "*.3DD") # PyQt4
		#                                                                     "here the text displayed on windows" "here the filter (extension)"   
		except Exception:
			fName, Filter = PySide.QtGui.QFileDialog.getOpenFileName(None, "Read a Frame3DD's 3DD file", path, "*.3DD") #PySide
		print ("src: "+fName)
		DesName = FreeCAD.getHomePath()+"bin/hFrame3DDfc.3DD"	
		print ("Des: "+DesName)	
		shutil.copyfile(fName,DesName)		

		#000000000000000000000000000000000000000000000000000000000000000000
		fp = open(fName)
		
		line = fp.readline().strip()
		print (line)
		
		#node 11111111111111111111111111111111111111111111111111	
		line=moveon(fp)
		print (line)
		data = line.split()
		numNode =  int(data[0])
		print ("numNode: "+str(numNode))
		
		line=moveon(fp)
		nodeCount = 1
		dataNode = line.split()
		NodeList[dataNode[0]] =  Node(dataNode[0], float(dataNode[1]) ,float( dataNode[2]) , float( dataNode[3]) )
		nodeCount+=1
		while 1:
			line = moveon(fp)
			dataNode = line.split()
			#print (dataNode[0])
			NodeList[dataNode[0]] =  Node(dataNode[0], float(dataNode[1]) ,float( dataNode[2]) , float( dataNode[3]) )
			nodeCount+=1
			if nodeCount>numNode:
				break
					
		#node 11111111111111111111111111111111111111111111111111111111111	
		GrpNode =FreeCAD.ActiveDocument.getObject('Nodes')
		if GrpNode!=None:
			GrpNode.removeObjectsFromDocument()
		else:
			FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","Nodes")
			GrpNode =FreeCAD.ActiveDocument.getObject('Nodes')
			
		for id in NodeList:
			#Msg(id ); Msg( iNode) ; Msg('\n')
			iPoint = Draft.makePoint(NodeList[id].x*factor,NodeList[id].y*factor,NodeList[id].z*factor)
			iPoint.Label = "N"+id
			iPoint.ViewObject.PointColor = (0.667,0.000,0.000)
			GrpNode.addObject(iPoint)
			#GrpNode.append(iPoint)

		#reaction 222222222222222222222222222222222222222222222222222222	
		line=moveon(fp)
		data = line.split()
		numReaction =  int(data[0])
		print ("numReaction: "+str(numReaction))

		if numReaction>0:

			for j in range(numReaction):
				line = moveon(fp)
				#data = line.split()
				
		# Member 333333333333333333333333333333333333333	
		line=moveon(fp)
		data = line.split()
		numMember =  int(data[0])
		print ("numMember: "+str(numMember))
		line=moveon(fp)		
			
		memberCount = 1
		dataMember = line.split()
		MemberList[dataMember[0]] =  Member(dataMember[0] ,dataMember[1] , dataMember[2])  
		memberCount+=1
		while 1:
			line = moveon(fp)
			dataMember = line.split()
			MemberList[dataMember[0]] =  Member(dataMember[0] ,dataMember[1] , dataMember[2])  
			memberCount+=1
			if memberCount>numMember:
				break

		#member	3333333333333333333333333333333333333333333333333333333
		GrpMember =FreeCAD.ActiveDocument.getObject('Members')
		if GrpMember!=None:
			GrpMember.removeObjectsFromDocument()
		else:
			FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","Members")
			GrpMember =FreeCAD.ActiveDocument.getObject('Members')
				
		for id in MemberList:
			n1 = MemberList[id].n1
			n2 = MemberList[id].n2
			points=[ Base.Vector(NodeList[n1].x*factor,NodeList[n1].y*factor,NodeList[n1].z*factor ) ,
                 Base.Vector(NodeList[n2].x*factor,NodeList[n2].y*factor,NodeList[n2].z*factor) ] 
			iMember = Draft.makeWire(points,closed=False,face=True,support=None)
			iMember.Label = "M"+id
			GrpMember.addObject(iMember)
			#GrpMember.append(iMember)
			
		# 444444444444444444444
		line = moveon(fp)		
		line = moveon(fp)
		line = moveon(fp)
		line = moveon(fp)
		line = moveon(fp)

		# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
		#Static
		line=moveon(fp)		
		data = line.split()
		print (line)
		numSLC =  int(data[0])
		print ("numSLC: "+str(numSLC))
		
		GLC=[]

		Larrow=100.0
		ULarrow=20.0
		
		
		GrpSLoadCase =FreeCAD.ActiveDocument.getObject('StaticLoadCases')
		if GrpSLoadCase!=None:
			GrpSLoadCase.removeObjectsFromDocument()
		else:
			FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","StaticLoadCases")
			GrpSLoadCase =FreeCAD.ActiveDocument.getObject('StaticLoadCases')
			
		for i in range(numSLC):
			# Begin Static Load Case 1 of 2

			# gravitational acceleration for self-weight loading (global)
			#.gX		gY		gZ
			#.in./s^2	in./s^2		in./s^2
			
			print (" ")
			print ("LC = "+str(i))
			print (" ")
			
			line=moveon(fp)		
			#0  		0		0

			iLoadCase=FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","SLC"+str(i))
			GLC.append(iLoadCase)
			GrpSLoadCase.addObject(GLC[i])
				
			# number of loaded nodes (Point Load) aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
			line=moveon(fp)		
			print (line)
			data = line.split()
			numLN =  int(data[0])
			print ("numLN: "+str(numLN))
			
			if numLN>0:
				#.n     Fx       Fy     Fz      Mxx     Myy     Mzz
				#.      kip      kip    kip     in.k    in.k    in.k

				GPLarrow=[]

				for j in range(numLN):
					#2 0 -10.0 0 0 0 0
					#3 0 -20.0 0 0 0 0
					
					print ("PL = "+str(j))
					
					tStr=""
					tStr="LC"+str(i)+"PL"+str(j)
					iPointLoad=FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",tStr)
					GPLarrow.append(iPointLoad)
					GLC[i].addObject(GPLarrow[j])

					line = moveon(fp)
					data = line.split()
				
					n1 = str(data[0])
					Fx=data[1]
					Fy=data[2]
					Fz=data[3]
					Mx=data[4]
					My=data[5]
					Mz=data[6]
					
					if Fx !="0" : 
						#Vertical
						pointsLN=[ Base.Vector(NodeList[n1].x*factor,NodeList[n1].y*factor,NodeList[n1].z*factor ), Base.Vector((NodeList[n1].x-Larrow)*factor,(NodeList[n1].y)*factor,(NodeList[n1].z)*factor) ] 
						iPointLoadV = Draft.makeWire(pointsLN,closed=False,face=True,support=None)
						iPointLoadV.Label ="LC"+str(i)+ "PL"+str(j)+"FxV"
						iPointLoadV.ViewObject.LineColor = (0.667,0.,0.000)
						GPLarrow[j].addObject(iPointLoadV)
						#Arrow Left
						pointsLNL=[ Base.Vector((NodeList[n1].x-Larrow)*factor,(NodeList[n1].y)*factor,NodeList[n1].z*factor ), Base.Vector((NodeList[n1].x-Larrow+Larrow/10.0)*factor,(NodeList[n1].y+Larrow/10.0)*factor,NodeList[n1].z*factor) ] 
						iPointLoadL = Draft.makeWire(pointsLNL,closed=False,face=True,support=None)
						iPointLoadL.Label = "LC"+str(i)+"PL"+str(j)+"FxL"
						iPointLoadL.ViewObject.LineColor = (0.667,0.,0.000)
						GPLarrow[j].addObject(iPointLoadL)
						#Arrow Right
						pointsLNR=[ Base.Vector((NodeList[n1].x-Larrow)*factor,(NodeList[n1].y)*factor,NodeList[n1].z*factor ), Base.Vector((NodeList[n1].x-Larrow+Larrow/10.0)*factor,(NodeList[n1].y-Larrow/10.0)*factor,NodeList[n1].z*factor) ] 
						iPointLoadR = Draft.makeWire(pointsLNR,closed=False,face=True,support=None)
						iPointLoadR.Label = "LC"+str(i)+"PL"+str(j)+"FxR"
						iPointLoadR.ViewObject.LineColor = (0.667,0.,0.000)
						GPLarrow[j].addObject(iPointLoadR)
					if Fy !="0" : 
						#Vertical
						pointsLN=[ Base.Vector(NodeList[n1].x*factor,NodeList[n1].y*factor,NodeList[n1].z*factor ), Base.Vector((NodeList[n1].x)*factor,(NodeList[n1].y-Larrow)*factor,(NodeList[n1].z)*factor) ] 
						iPointLoadV = Draft.makeWire(pointsLN,closed=False,face=True,support=None)
						iPointLoadV.Label ="LC"+str(i)+ "PL"+str(j)+"FyV"
						iPointLoadV.ViewObject.LineColor = (0.,0.667,0.000)
						GPLarrow[j].addObject(iPointLoadV)
						#Arrow Left
						pointsLNL=[ Base.Vector(NodeList[n1].x*factor,(NodeList[n1].y-Larrow)*factor,NodeList[n1].z*factor ), Base.Vector((NodeList[n1].x-Larrow/10.0)*factor,(NodeList[n1].y-Larrow+Larrow/10.0)*factor,NodeList[n1].z*factor) ] 
						iPointLoadL = Draft.makeWire(pointsLNL,closed=False,face=True,support=None)
						iPointLoadL.Label = "LC"+str(i)+"PL"+str(j)+"FyL"
						iPointLoadL.ViewObject.LineColor = (0.,0.667,0.000)
						GPLarrow[j].addObject(iPointLoadL)
						#Arrow Right
						pointsLNR=[ Base.Vector(NodeList[n1].x*factor,(NodeList[n1].y-Larrow)*factor,NodeList[n1].z*factor ), Base.Vector((NodeList[n1].x+Larrow/10.0)*factor,(NodeList[n1].y-Larrow+Larrow/10.0)*factor,NodeList[n1].z*factor) ] 
						iPointLoadR = Draft.makeWire(pointsLNR,closed=False,face=True,support=None)
						iPointLoadR.Label = "LC"+str(i)+"PL"+str(j)+"FyR"
						iPointLoadR.ViewObject.LineColor = (0.,0.667,0.000)
						GPLarrow[j].addObject(iPointLoadR)
					if Fz !="0" : 
						#Vertical
						pointsLN=[ Base.Vector(NodeList[n1].x*factor,NodeList[n1].y*factor,NodeList[n1].z*factor ), Base.Vector((NodeList[n1].x)*factor,(NodeList[n1].y)*factor,(NodeList[n1].z-Larrow)*factor) ] 
						iPointLoadV = Draft.makeWire(pointsLN,closed=False,face=True,support=None)
						iPointLoadV.Label ="LC"+str(i)+ "PL"+str(j)+"FzV"
						iPointLoadV.ViewObject.LineColor = (0.,0.,0.667)
						GPLarrow[j].addObject(iPointLoadV)
						#Arrow Left
						pointsLNL=[ Base.Vector(NodeList[n1].x*factor,(NodeList[n1].y)*factor,(NodeList[n1].z-Larrow)*factor ), Base.Vector((NodeList[n1].x-Larrow/10.0)*factor,(NodeList[n1].y)*factor,(NodeList[n1].z-Larrow+Larrow/10.0)*factor) ] 
						iPointLoadL = Draft.makeWire(pointsLNL,closed=False,face=True,support=None)
						iPointLoadL.Label = "LC"+str(i)+"PL"+str(j)+"FzL"
						iPointLoadL.ViewObject.LineColor = (0.,0.,0.667)
						GPLarrow[j].addObject(iPointLoadL)
						#Arrow Right
						pointsLNR=[ Base.Vector(NodeList[n1].x*factor,(NodeList[n1].y)*factor,(NodeList[n1].z-Larrow)*factor ), Base.Vector((NodeList[n1].x+Larrow/10.0)*factor,(NodeList[n1].y)*factor,(NodeList[n1].z-Larrow+Larrow/10.0)*factor) ] 
						iPointLoadR = Draft.makeWire(pointsLNR,closed=False,face=True,support=None)
						iPointLoadR.Label = "LC"+str(i)+"PL"+str(j)+"FzR"
						iPointLoadR.ViewObject.LineColor = (0.,0.,0.667)
						GPLarrow[j].addObject(iPointLoadR)
						
					if Mx !=0 : 
						iMx=1
					if My !=0 : 
						iMy=1
					if My !=0 : 
						iMy=1
					


			# number of uniform loads bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
			#line = fp.readline().strip()
			line=moveon(fp)		
			print (line)
			data = line.split()
			numUL =  int(data[0])
			print ("numUL: "+str(numUL))
			
			if numUL>0:
				#.e    Ux   Uy   Uz
				#     N/mm N/mm N/mm
				GULarrow=[]

				for j in range(numUL):
					#2    0   0.1    0
					#1    0    0    0.1 
					iuniformLoad=FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","UL"+str(j))
					GULarrow.append(iuniformLoad)
					GLC[i].addObject(GULarrow[j])

					line = moveon(fp)
					data = line.split()
				
					n0 = str(data[0])
					n1 = MemberList[n0].n1
					n2 = MemberList[n0].n2
					Ux=data[1]
					Uy=data[2]
					Uz=data[3]

					iUx=0
					iUy=0
					iUz=0
			
					if Ux !="0" : 
						#n1
						#Vertical
						pointsUL=[ Base.Vector(NodeList[n1].x*factor,NodeList[n1].y*factor,NodeList[n1].z*factor ), Base.Vector((NodeList[n1].x-ULarrow)*factor,(NodeList[n1].y)*factor,(NodeList[n1].z)*factor) ] 
						iuniformLoadV = Draft.makeWire(pointsUL,closed=False,face=True,support=None)
						iuniformLoadV.Label = "ULa"+str(j)+"V"
						iuniformLoadV.ViewObject.LineColor = (0.667,0.,0.)
						GULarrow[j].addObject(iuniformLoadV)
						#Arrow Left
						pointsULL=[ Base.Vector((NodeList[n1].x-ULarrow)*factor,(NodeList[n1].y)*factor,NodeList[n1].z*factor ), Base.Vector((NodeList[n1].x-ULarrow+Larrow/10.0)*factor,(NodeList[n1].y+Larrow/10.0)*factor,NodeList[n1].z*factor) ] 
						iuniformLoadL = Draft.makeWire(pointsULL,closed=False,face=True,support=None)
						iuniformLoadL.Label = "ULa"+str(j)+"L"
						iuniformLoadL.ViewObject.LineColor = (0.667,0.,0.)
						GULarrow[j].addObject(iuniformLoadL)
						#Arrow Right
						pointsULR=[ Base.Vector((NodeList[n1].x-ULarrow)*factor,(NodeList[n1].y)*factor,NodeList[n1].z*factor ), Base.Vector((NodeList[n1].x-ULarrow+Larrow/10.0)*factor,(NodeList[n1].y-Larrow/10.0)*factor,NodeList[n1].z*factor) ] 
						iuniformLoadR = Draft.makeWire(pointsULR,closed=False,face=True,support=None)
						iuniformLoadR.Label = "ULa"+str(j)+"R"
						iuniformLoadR.ViewObject.LineColor = (0.667,0.,0.)
						GULarrow[j].addObject(iuniformLoadR)
			
						#n2
						#Vertical
						pointsULn2=[ Base.Vector(NodeList[n2].x*factor,NodeList[n2].y*factor,NodeList[n2].z*factor ), Base.Vector((NodeList[n2].x-ULarrow)*factor,(NodeList[n2].y)*factor,(NodeList[n2].z)*factor) ] 
						iuniformLoadV = Draft.makeWire(pointsULn2,closed=False,face=True,support=None)
						iuniformLoadV.Label = "ULb"+str(j)+"V"
						iuniformLoadV.ViewObject.LineColor = (0.667,0.,0.)
						GULarrow[j].addObject(iuniformLoadV)
						#Arrow Left
						pointsULLn2=[ Base.Vector((NodeList[n2].x-ULarrow)*factor,(NodeList[n2].y)*factor,NodeList[n2].z*factor ), Base.Vector((NodeList[n2].x-ULarrow+Larrow/10.0)*factor,(NodeList[n2].y-Larrow/10.0)*factor,NodeList[n2].z*factor) ] 
						iuniformLoadL = Draft.makeWire(pointsULLn2,closed=False,face=True,support=None)
						iuniformLoadL.Label = "ULb"+str(j)+"L"
						iuniformLoadL.ViewObject.LineColor = (0.667,0.,0.)
						GULarrow[j].addObject(iuniformLoadL)
						#Arrow Right
						pointsULRn2=[ Base.Vector((NodeList[n2].x-ULarrow)*factor,(NodeList[n2].y)*factor,NodeList[n2].z*factor ), Base.Vector((NodeList[n2].x-ULarrow+Larrow/10.0)*factor,(NodeList[n2].y+Larrow/10.0)*factor,NodeList[n2].z*factor) ] 
						iuniformLoadR = Draft.makeWire(pointsULRn2,closed=False,face=True,support=None)
						iuniformLoadR.Label = "ULb"+str(j)+"R"
						iuniformLoadR.ViewObject.LineColor = (0.667,0.,0.)
						GULarrow[j].addObject(iuniformLoadR)
			
						#line linking n1 & n2
						pointsULn1n2=[ Base.Vector((NodeList[n1].x-ULarrow)*factor,(NodeList[n1].y)*factor,NodeList[n1].z*factor ), Base.Vector((NodeList[n2].x-ULarrow)*factor,(NodeList[n2].y)*factor,NodeList[n2].z*factor) ] 
						iuniformLoadLab = Draft.makeWire(pointsULn1n2,closed=False,face=True,support=None)
						iuniformLoadLab.Label = "ULab"+str(j)+"Link"
						iuniformLoadLab.ViewObject.LineColor = (0.667,0.,0.)
						GULarrow[j].addObject(iuniformLoadLab)
					if Uy !="0" : 
						#n1
						#Vertical
						pointsUL=[ Base.Vector(NodeList[n1].x*factor,NodeList[n1].y*factor,NodeList[n1].z*factor ), Base.Vector((NodeList[n1].x)*factor,(NodeList[n1].y-ULarrow)*factor,(NodeList[n1].z)*factor) ] 
						iuniformLoadV = Draft.makeWire(pointsUL,closed=False,face=True,support=None)
						iuniformLoadV.Label = "ULa"+str(j)+"V"
						iuniformLoadV.ViewObject.LineColor = (0.,0.667,0.)
						GULarrow[j].addObject(iuniformLoadV)
						#Arrow Left
						pointsULL=[ Base.Vector(NodeList[n1].x*factor,(NodeList[n1].y-ULarrow)*factor,NodeList[n1].z*factor ), Base.Vector((NodeList[n1].x-Larrow/10.0)*factor,(NodeList[n1].y-ULarrow+Larrow/10.0)*factor,NodeList[n1].z*factor) ] 
						iuniformLoadL = Draft.makeWire(pointsULL,closed=False,face=True,support=None)
						iuniformLoadL.Label = "ULa"+str(j)+"L"
						iuniformLoadL.ViewObject.LineColor = (0.,0.667,0.)
						GULarrow[j].addObject(iuniformLoadL)
						#Arrow Right
						pointsULR=[ Base.Vector(NodeList[n1].x*factor,(NodeList[n1].y-ULarrow)*factor,NodeList[n1].z*factor ), Base.Vector((NodeList[n1].x+Larrow/10.0)*factor,(NodeList[n1].y-ULarrow+Larrow/10.0)*factor,NodeList[n1].z*factor) ] 
						iuniformLoadR = Draft.makeWire(pointsULR,closed=False,face=True,support=None)
						iuniformLoadR.Label = "ULa"+str(j)+"R"
						iuniformLoadR.ViewObject.LineColor = (0.,0.667,0.)
						GULarrow[j].addObject(iuniformLoadR)
			
						#n2
						#Vertical
						pointsULn2=[ Base.Vector(NodeList[n2].x*factor,NodeList[n2].y*factor,NodeList[n2].z*factor ), Base.Vector((NodeList[n2].x)*factor,(NodeList[n2].y-ULarrow)*factor,(NodeList[n2].z)*factor) ] 
						iuniformLoadV = Draft.makeWire(pointsULn2,closed=False,face=True,support=None)
						iuniformLoadV.Label = "ULb"+str(j)+"V"
						iuniformLoadV.ViewObject.LineColor = (0.,0.667,0.)
						GULarrow[j].addObject(iuniformLoadV)
						#Arrow Left
						pointsULLn2=[ Base.Vector(NodeList[n2].x*factor,(NodeList[n2].y-ULarrow)*factor,NodeList[n2].z*factor ), Base.Vector((NodeList[n2].x-Larrow/10.0)*factor,(NodeList[n2].y-ULarrow+Larrow/10.0)*factor,NodeList[n2].z*factor) ] 
						iuniformLoadL = Draft.makeWire(pointsULLn2,closed=False,face=True,support=None)
						iuniformLoadL.Label = "ULb"+str(j)+"L"
						iuniformLoadL.ViewObject.LineColor = (0.,0.667,0.)
						GULarrow[j].addObject(iuniformLoadL)
						#Arrow Right
						pointsULRn2=[ Base.Vector(NodeList[n2].x*factor,(NodeList[n2].y-ULarrow)*factor,NodeList[n2].z*factor ), Base.Vector((NodeList[n2].x+Larrow/10.0)*factor,(NodeList[n2].y-ULarrow+Larrow/10.0)*factor,NodeList[n2].z*factor) ] 
						iuniformLoadR = Draft.makeWire(pointsULRn2,closed=False,face=True,support=None)
						iuniformLoadR.Label = "ULb"+str(j)+"R"
						iuniformLoadR.ViewObject.LineColor = (0.,0.667,0.)
						GULarrow[j].addObject(iuniformLoadR)
			
						#line linking n1 & n2
						pointsULn1n2=[ Base.Vector(NodeList[n1].x*factor,(NodeList[n1].y-ULarrow)*factor,NodeList[n1].z*factor ), Base.Vector(NodeList[n2].x*factor,(NodeList[n2].y-ULarrow)*factor,NodeList[n2].z*factor) ] 
						iuniformLoadLab = Draft.makeWire(pointsULn1n2,closed=False,face=True,support=None)
						iuniformLoadLab.Label = "ULab"+str(j)+"Link"
						iuniformLoadLab.ViewObject.LineColor = (0.,0.667,0.)
						GULarrow[j].addObject(iuniformLoadLab)
						
					if Uz !="0" : 
						
						#n1
						#Vertical
						pointsUL=[ Base.Vector(NodeList[n1].x*factor,NodeList[n1].y*factor,NodeList[n1].z*factor ), Base.Vector((NodeList[n1].x)*factor,(NodeList[n1].y)*factor,(NodeList[n1].z-ULarrow)*factor) ] 
						iuniformLoadV = Draft.makeWire(pointsUL,closed=False,face=True,support=None)
						iuniformLoadV.Label = "ULa"+str(j)+"V"
						iuniformLoadV.ViewObject.LineColor = (0.,0.,0.667)
						GULarrow[j].addObject(iuniformLoadV)
						#Arrow Left
						pointsULL=[ Base.Vector(NodeList[n1].x*factor,(NodeList[n1].y)*factor,(NodeList[n1].z-ULarrow)*factor ), Base.Vector((NodeList[n1].x-Larrow/10.0)*factor,(NodeList[n1].y-ULarrow+Larrow/10.0)*factor,NodeList[n1].z*factor) ] 
						iuniformLoadL = Draft.makeWire(pointsULL,closed=False,face=True,support=None)
						iuniformLoadL.Label = "ULa"+str(j)+"L"
						iuniformLoadL.ViewObject.LineColor = (0.,0.,0.667)
						GULarrow[j].addObject(iuniformLoadL)
						#Arrow Right
						pointsULR=[ Base.Vector(NodeList[n1].x*factor,(NodeList[n1].y)*factor,(NodeList[n1].z-ULarrow)*factor ), Base.Vector((NodeList[n1].x+Larrow/10.0)*factor,(NodeList[n1].y-ULarrow+Larrow/10.0)*factor,NodeList[n1].z*factor) ] 
						iuniformLoadR = Draft.makeWire(pointsULR,closed=False,face=True,support=None)
						iuniformLoadR.Label = "ULa"+str(j)+"R"
						iuniformLoadR.ViewObject.LineColor = (0.,0.,0.667)
						GULarrow[j].addObject(iuniformLoadR)
			
						#n2
						#Vertical
						pointsULn2=[ Base.Vector(NodeList[n2].x*factor,NodeList[n2].y*factor,NodeList[n2].z*factor ), Base.Vector((NodeList[n2].x)*factor,(NodeList[n2].y)*factor,(NodeList[n2].z-ULarrow)*factor) ] 
						iuniformLoadV = Draft.makeWire(pointsULn2,closed=False,face=True,support=None)
						iuniformLoadV.Label = "ULb"+str(j)+"V"
						iuniformLoadV.ViewObject.LineColor = (0.,0.,0.667)
						GULarrow[j].addObject(iuniformLoadV)
						#Arrow Left
						pointsULLn2=[ Base.Vector(NodeList[n2].x*factor,(NodeList[n2].y)*factor,(NodeList[n2].z-ULarrow)*factor ), Base.Vector((NodeList[n2].x-Larrow/10.0)*factor,(NodeList[n2].y)*factor,(NodeList[n2].z-ULarrow+Larrow/10.0)*factor) ] 
						iuniformLoadL = Draft.makeWire(pointsULLn2,closed=False,face=True,support=None)
						iuniformLoadL.Label = "ULb"+str(j)+"L"
						iuniformLoadL.ViewObject.LineColor = (0.,0.,0.667)
						GULarrow[j].addObject(iuniformLoadL)
						#Arrow Right
						pointsULRn2=[ Base.Vector(NodeList[n2].x*factor,(NodeList[n2].y)*factor,(NodeList[n2].z-ULarrow)*factor ), Base.Vector((NodeList[n2].x+Larrow/10.0)*factor,(NodeList[n2].y)*factor,(NodeList[n2].z-ULarrow+Larrow/10.0)*factor) ] 
						iuniformLoadR = Draft.makeWire(pointsULRn2,closed=False,face=True,support=None)
						iuniformLoadR.Label = "ULb"+str(j)+"R"
						iuniformLoadR.ViewObject.LineColor = (0.,0.,0.667)
						GULarrow[j].addObject(iuniformLoadR)
			
						#line linking n1 & n2
						pointsULn1n2=[ Base.Vector(NodeList[n1].x*factor,(NodeList[n1].y)*factor,(NodeList[n1].z-ULarrow)*factor ), Base.Vector(NodeList[n2].x*factor,(NodeList[n2].y)*factor,(NodeList[n2].z-ULarrow)*factor) ] 
						iuniformLoadLab = Draft.makeWire(pointsULn1n2,closed=False,face=True,support=None)
						iuniformLoadLab.Label = "ULab"+str(j)+"Link"
						iuniformLoadLab.ViewObject.LineColor = (0.,0.,0.667)
						GULarrow[j].addObject(iuniformLoadLab)
					
					
			# number of trapezoidal loads ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
			#line = fp.readline().strip()
			line=moveon(fp)		
			print (line)
			data = line.split()
			numTL =  int(data[0])
			print ("numTL: "+str(numTL))
			
			if numTL>0:
				#.e     x1       x2        w1      w2
				#       mm       mm       N/mm    N/mm
				GTLarrow=[]

				for j in range(numTL):
					#	3     20       80       0.01    0.05    # location and loading - local x-axis
					#         0        0        0       0      # location and loading - local y-axis
					#        80      830      -0.05    0.07    # location and loading - local z-axis

					itrapezoidalLoad=FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","trapezoidalL"+str(j))
					GTLarrow.append(itrapezoidalLoad)
					GLC[i].addObject(GTLarrow[j])
					
					line = moveon(fp)
					line = moveon(fp)
					line = moveon(fp)
			
			# number of internal concentrated loads ddddddddddddddddddddddddddddddddddddddddddddd
			line = moveon(fp)
			print (line)
			data = line.split()
			numICL =  int(data[0])
			print ("numICL: "+str(numICL))
			
			if numICL>0:
				#.e    Px   Py    Pz   x    
				#      N    N     N    mm
				GICLarrow=[]

				for j in range(numICL):
					#  1    0    100  -900  600
					#  2    0   -200   200  800
					iICLoad=FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","ICL"+str(j))
					GICLarrow.append(iICLoad)
					GLC[i].addObject(GICLarrow[j])

					line = moveon(fp)
			
			# number of temperature loads eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
			#line = fp.readline().strip()
			line=moveon(fp)		
			print (line)
			data = line.split()
			numTempL =  int(data[0])
			print ("numTempL: "+str(numTempL))
			
			if numTempL>0:
				#.e  alpha   hy   hz   Ty+  Ty-  Tz+  Tz-
				#    /degC   mm   mm   degC degC degC degC

				GTempLarrow=[]

				for j in range(numTempL):
					#1   12e-6    10   10  20   10   10  -10
					iTempLoad=FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","TempL"+str(j))
					GTempLarrow.append(iTempLoad)
					GLC[i].addObject(GTempLarrow[j])

					line = moveon(fp)
						
					#print (line)
					data = line.split()
				
					n0 = str(data[0])
					n1 = MemberList[n0].n1
					n2 = MemberList[n0].n2

					#n1,n2
					#points=[ Base.Vector(NodeList[n1].x*factor,NodeList[n1].y*factor,NodeList[n1].z*factor ), Base.Vector(NodeList[n2].x*factor,NodeList[n2].y*factor,NodeList[n2].z*factor) ] 
					#iTempLoadV = Draft.makeWire(points,closed=False,face=True,support=None)
					#iTempLoadV.Label = "TempLa"+str(j)+"V"
					#iTempLoadV.ViewObject.LineColor = (1.,0.,0.)
					#GTempLarrow[j].addObject(iTempLoadV)

					#MemberList[n0].ViewObject.LineColor = (1.,0.,0.)
					#print ('M'+n0)
					#tMember =FreeCAD.ActiveDocument.getObject('M1')
					#print (tMember)
					#tMember.ViewObject.LineColor = (1.,0.,0.)
	
			# number of nodes with prescribed displacements ffffffffffffffffffffffffffffffffffffffffffffffffffffff
			#line = fp.readline().strip()
			line=moveon(fp)		
			print (line)
			data = line.split()
			numPD =  int(data[0])
			print ("numPD: "+str(numPD))
			
			if numPD>0:
				#.n    Dx      Dy      Dz      Dxx     Dyy     Dzz
				#.     in      in      in      rad.    rad.    rad.
			
				GPDarrow=[]
				
				for j in range(numPD):
					#  8 	0.1	0.0	0.0	0.0	0.0	0.0
					
					print ("PD = "+str(j))
					tStr=""
					tStr="PD"+str(j)
					print (tStr)
					iPD=FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",tStr)
					GPDarrow.append(iPD)
					GLC[i].addObject(GPDarrow[j])
					
					line = moveon(fp)
					#data = line.split()



		# BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
		# dynamic
		#6				# number of desired dynamic modes of vibration
		
		print (" ")
		
		line=moveon(fp)		
		data = line.split()
		print (line)
		numDLC =  int(data[0])
		print ("numDLC: "+str(numDLC))
		
		GDLC=[]
		
		if numDLC>0:
			#1                               # 1: subspace Jacobi     2: Stodola
			#0				# 0: consistent mass ... 1: lumped mass matrix
			#1e-9				# mode shape tolerance
			#0.0				# shift value ... for unrestrained structures
			#10.0                            # exaggerate modal mesh deformations
			line = moveon(fp)
			line = moveon(fp)
			line = moveon(fp)
			line = moveon(fp)
			line = moveon(fp)
		
			#11111111111111111111111111111111111111111111111111111111111111111111111                               
			# number of nodes with extra inertia
			line=moveon(fp)		
			data = line.split()
			print (line)
			numExtInertia =  int(data[0])
			print ("numExtInertia: "+str(numExtInertia))
		
			if numExtInertia>0:
				#.n      Mass   Ixx      Iyy      Izz 
				#        ton    ton.mm^2 ton.mm^2 ton.mm^2
				for j in range(numExtInertia):
					#1        0.1    0        0        0
					line = moveon(fp)
					#data = line.split()
			
			#22222222222222222222222222222222222222222222222222222222222222222222
			# frame elements with extra mass			
			line=moveon(fp)		
			data = line.split()
			print (line)
			numExtMass =  int(data[0])
			print ("numExtMass: "+str(numExtMass))
		
			if numExtMass>0:
				#.n      Mass   Ixx      Iyy      Izz 
				#        ton    ton.mm^2 ton.mm^2 ton.mm^2
				for j in range(numExtMass):
					#1        0.1    0        0        0
					line = moveon(fp)
					#data = line.split()
		
		
			#33333333333333333333333333333333333333333333333333333333333333333333333333333
			# number of modes to animate, nA		
			line=moveon(fp)		
			data = line.split()
			print (line)
			numModesAni =  int(data[0])
			print ("numModesAni: "+str(numModesAni))
		
			if numModesAni>0:
				# 1  2  3  4 5 6 		# list of modes to animate - omit if nA == 0
				line = moveon(fp)
				
			#2                               # pan rate during animation
			line = moveon(fp)
		
		#Msg('Done!!\n\n')
		
		FreeCAD.ActiveDocument.recompute()
		FreeCADGui.activeDocument().activeView().viewAxonometric()
		FreeCADGui.SendMsgToActiveView("ViewFit")
		
		#Msg ("Well done.")

FreeCADGui.addCommand('hFrame3DDfc3DDin',hFrame3DDfc3DDin())