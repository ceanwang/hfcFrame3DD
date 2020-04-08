#

__title__ = "FreeCAD hFrame3DDfc library"
__author__ = "CeanWang@gmail.com" 

import FreeCAD,FreeCADGui
import FreeCAD,FreeCADGui
import Fem
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
		
#  Node    X-dsp       Y-dsp       Z-dsp       X-rot       Y-rot       Z-rot
class Displacement:
    def __init__(self, id , xdsp,ydsp,zdsp,xrot,yrot,zrot):
        self.xdsp = xdsp
        self.ydsp = ydsp
        self.zdsp = zdsp
        self.xrot = xrot
        self.yrot = yrot
        self.zrot = zrot
        self.id = str(id)

		
def SeekNextSec(fp,tStr):	
	while 1:
		line = fp.readline().strip()
		if line==tStr:
			return line
		else:
			#print (line)
			continue

def SeekOne(fp):	
	while 1:
		line = fp.readline().strip()
		data = line.split()

		if data[0]=="1":
			return line
		else:
			#print (line)
			continue
			
class hFrame3DDfcResult:
	"Frame3DD result object"
	def GetResources(self):
		return {"MenuText": "My Result",
				"Accel": "Ctrl+t",
				"ToolTip": "Show Frame3DD result",
				"Pixmap": os.path.dirname(__file__)+"./resources/cap.svg"
		}

	def IsActive(self):

		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True

	def Activated(self):
		import feminout.importToolsFem as toolsFem
		import ObjectsFem
		
		analysis=None

		path = FreeCAD.getHomePath()+"/bin/"
		fName = path+'hFrame3DDfc.out'
		
		NodeList = {}
		MemberList = {}                                  

		DisplacementList = {}  
		
		NodeEndList = {}
		MemberEndList = {}                                  

		ProjectDescription = ''
		
		nodes = {}
		results = []
		mode_results = {}
		mode_disp = {}
		iFilled=[]


		nDisp=0
		mDisp=0
		numNode = 0
		isDebug=1
		
		#factor = 25.42
		factor = 1
		
		factorZoom = 100
		

		#000000000000000000000000000000000000000000000000000000000000000000
		femmesh = Fem.FemMesh()
		#femResult = Fem.FemResultObject()
		
		fp = open(fName)
		Frame3DD_file=fp.readlines()
		fp.close()
		
		tline=[]
		for line in Frame3DD_file:
			tline.append(line.strip())
			
		for i in range(len(tline)):

			tStrNode="In 2D problems the Y-axis is vertical.  In 3D problems the Z-axis is vertical."	
			if tline[i].strip() == tStrNode:
				#Console.PrintError("FEM: nodes found.\n")
				
				i=i+1
				i=i+1
				data = tline[i].split()
				#12 NODES             12 FIXED NODES       21 FRAME ELEMENTS   2 LOAD CASES   
				numNode =  int(data[0])
				numFixedNode =  int(data[2])
				numMember =  int(data[5])
				numLC =  int(data[8])
				
				for id in range(numNode): # node
					iFilled.append(0)
		
				i=i+1 # = fp.readline().strip()
				i=i+1 # = fp.readline().strip()
				i=i+1 # = fp.readline().strip()
				
				if isDebug==1:
					print ("")			
					print ("numNode: "+str(numNode))
				for id in range(numNode): # node
					#1       0.000000       0.000000       0.000000    0.000   1  1  1  1  1  0
					i=i+1
					#print (tline[i])
					dataNode = tline[i].split()
				
					elem = int(dataNode[0])
					nodes_x = float(dataNode[1])
					nodes_y = float(dataNode[2])
					nodes_z = float(dataNode[3])
					nodes[elem] = FreeCAD.Vector(nodes_x, nodes_y, nodes_z)
					NodeList[id] =  Node(str(id+1), nodes_x, nodes_y, nodes_z )

				i=i+1
				i=i+1
				
				if isDebug==1:
					print ("")			
					print ("numMember: "+str(numMember))
				for id in range(numMember): # Member
					i=i+1
					#print (tline[i])
					dataNode = tline[i].split()
					elem = int(dataNode[0])
					nd1 = int(dataNode[1])
					nd2 = int(dataNode[2])
					MemberList[id] =  Member(str(id+1) ,nd1, nd2)  

				#if isDebug==1:
				#	print ("")			
				#	print ("numFixedNode: "+str(numFixedNode))
				
				if isDebug==1:
					print ("")			
					print ("numLC: "+str(numLC))
			
				femmesh = Fem.FemMesh()
				# nodes
				#print ("Add nodes")
				for id in NodeList: # node
					#femmesh.addNode(NodeList[id].x,NodeList[id].y,NodeList[id].z, int(id)+1 )
					femmesh.addNode(NodeList[id].x,NodeList[id].y,NodeList[id].z, int(id)+1 )
				
				# elements
				for id in MemberList:
					n1 = MemberList[id].n1
					n2 = MemberList[id].n2
					femmesh.addEdge([int(n1), int(n2)], int(id)+1)
					
					
		result_mesh_object = None
		result_mesh_object = ObjectsFem.makeMeshResult(
			FreeCAD.ActiveDocument,
			"ResultMesh"
		)
		result_mesh_object.FemMesh = femmesh
		res_mesh_is_compacted = False
		nodenumbers_for_compacted_mesh = []
				
		isElastic=0
		isModal=0
		for i in range(len(tline)):
			tStrDis="E L A S T I C   S T I F F N E S S   A N A L Y S I S   via  L D L'  decomposition"
			if tline[i].strip() == tStrDis:
				#Console.PrintError("FEM: displacement found.\n")
				isElastic=1
				
			if (isElastic==1 and isModal==0):
				tStrDis="Node    X-dsp       Y-dsp       Z-dsp       X-rot       Y-rot       Z-rot"
				if tline[i].strip() == tStrDis:
					#Console.PrintError("FEM: displacement found.\n")
				
					print ("")			
					print ("Displacement"+str(nDisp))	
					
					for id in range(numNode): # node
						iFilled[id]=0
					
					for id in range(numNode): # node
						#Node    X-dsp       Y-dsp       Z-dsp       X-rot       Y-rot       Z-rot
						#1    0.0         0.0         0.0         0.0         0.0        -0.001254
						i=i+1
						#print (tline[i])
						dataNode = tline[i].split()
						#print (dataNode[0]+" "+str(numNode))
						if (dataNode[0].isdigit()):
							elem = int(dataNode[0])
							iFilled[elem-1] = 1
							mode_disp_x = float(dataNode[1])
							mode_disp_y = float(dataNode[2])
							mode_disp_z = float(dataNode[3])
							mode_disp[elem] = FreeCAD.Vector(mode_disp_x, mode_disp_y, mode_disp_z)
						else:
							break
					
					for id in range(numNode): # node
						if (iFilled[id] == 0):
							mode_disp[id+1] = FreeCAD.Vector(0., 0., 0.)
						#print (str(id)+" "+str(iFilled[id]))	
					
					#mode_results["disp"+str(nDisp)] = mode_disp
					mode_results["disp"] = mode_disp
					mode_disp = {}

					nDisp+=1	
					
					# append mode_results to results and reset mode_result
					results.append(mode_results)
					mode_results = {}

					
					
					
			#mode shapes	
			
			tStrDis="M O D A L   A N A L Y S I S   R E S U L T S"
			if tline[i].strip() == tStrDis:
				#Console.PrintError("FEM: displacement found.\n")
				isModal=1
				
			if (isModal==1):
				tStrDis="Node    X-dsp       Y-dsp       Z-dsp       X-rot       Y-rot       Z-rot"
				if tline[i].strip() == tStrDis:
					#Console.PrintError("FEM: displacement found.\n")
				
					print ("")			
					print ("Modal Displacement"+str(mDisp))			
				
					for id in range(numNode): # node
						iFilled[id]=0
					
					for id in range(numNode): # node
						#Node    X-dsp       Y-dsp       Z-dsp       X-rot       Y-rot       Z-rot
						#1    0.0         0.0         0.0         0.0         0.0        -0.001254
						#" %11.3e"
						#1 -1.#IOe+000 -1.#IOe+000 -1.#IOe+000 -1.#IOe+000 -1.#IOe+000 -1.#IOe+000
						i=i+1
						#print (tline[i])
						dataNode = tline[i].split()
						#print (dataNode[0]+" "+str(numNode))
						if (dataNode[0].isdigit()):
							elem = int(dataNode[0])
							iFilled[elem-1] = 1
							mode_disp_x = float(dataNode[1])
							mode_disp_y = float(dataNode[2])
							mode_disp_z = float(dataNode[3])
							mode_disp[elem] = FreeCAD.Vector(mode_disp_x, mode_disp_y, mode_disp_z)
						else:
							break
			
					for id in range(numNode): # node
						if (iFilled[id] == 0):
							mode_disp[id+1] = FreeCAD.Vector(0., 0., 0.)
						#print (str(id)+" "+str(iFilled[id]))	
					
					#mode_results["disp"+str(nDisp)] = mode_disp
					mode_results["disp"] = mode_disp
					mode_disp = {}

					mDisp+=1	
					
					# append mode_results to results and reset mode_result
					results.append(mode_results)
					mode_results = {}


		res_obj=[]		
		iLC=0
		iModal=0
		results_name="Elastic"

		for result_set in results:
			if (iLC<numLC):				
				results_name="Elastic"
				res_obj.append(ObjectsFem.makeResultMechanical(FreeCAD.ActiveDocument, results_name+str(iLC)))
			else:
				results_name="Modal"
				res_obj.append(ObjectsFem.makeResultMechanical(FreeCAD.ActiveDocument, results_name+str(iModal)))
				iModal+=1
						
			res_obj[iLC].Mesh = result_mesh_object
			#res_obj[iLC] = importToolsFem.fill_femresult_mechanical(res_obj[iLC], result_set)
			res_obj[iLC] = toolsFem.fill_femresult_mechanical(res_obj[iLC], result_set)
			if analysis:
				analysis.addObject(res_obj[iLC])

			# complementary result object calculations
			import femresult.resulttools as restools
			import femtools.femutils as femutils
			if not res_obj[iLC].MassFlowRate:
				if res_mesh_is_compacted is False:
					# first result set, compact FemMesh and NodeNumbers
					res_obj[iLC] = restools.compact_result(res_obj[iLC])
					res_mesh_is_compacted = True
					nodenumbers_for_compacted_mesh = res_obj[iLC].NodeNumbers
				else:
					# all other result sets, do not compact FemMesh, only set NodeNumbers
					res_obj[iLC].NodeNumbers = nodenumbers_for_compacted_mesh

			# fill DisplacementLengths
			res_obj[iLC] = restools.add_disp_apps(res_obj[iLC])
			# fill StressValues
			res_obj[iLC] = restools.add_von_mises(res_obj[iLC])
			if res_obj[iLC].getParentGroup():
				has_reinforced_mat = False
				for obj in res_obj[iLC].getParentGroup().Group:
					if obj.isDerivedFrom("App::MaterialObjectPython") \
							and femutils.is_of_type(obj, "Fem::MaterialReinforced"):
						has_reinforced_mat = True
						restools.add_principal_stress_reinforced(res_obj[iLC])
						break
				if has_reinforced_mat is False:
					# fill PrincipalMax, PrincipalMed, PrincipalMin, MaxShear
					res_obj[iLC] = restools.add_principal_stress_std(res_obj[iLC])
			else:
				# if a pure Frame3DD file was opened no analysis and thus no parent group
				# fill PrincipalMax, PrincipalMed, PrincipalMin, MaxShear
				res_obj[iLC] = restools.add_principal_stress_std(res_obj[iLC])
			# fill Stats
			res_obj[iLC] = restools.fill_femresult_stats(res_obj[iLC])

			iLC+=1
		
		
		

FreeCADGui.addCommand('hFrame3DDfcResult',hFrame3DDfcResult())