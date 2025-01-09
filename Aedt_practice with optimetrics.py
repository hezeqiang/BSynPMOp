from ansys.aedt.core import Desktop, Maxwell3d, Hfss
import ansys.aedt.core.downloads as downloads
import os,time,json
import pyaedt
from ansys.aedt.core.visualization.plot.pdf import AnsysReport
from SimuMotorPara import HBCPMConcentratedWindingParameters
from GeneratePhaseCoil import generate_three_phases
from GeneratePhaseCoil import generate_two_phases

# Launch AEDT
AedtVersion = "2024.1"  # Replace with your installed AEDT version
ProjectFullName = pyaedt.generate_unique_project_name()
ProjectName=os.path.basename(ProjectFullName)
print(ProjectName+"**************************")
DesignName = "HBCPM"
desktop = Desktop(version=AedtVersion,new_desktop=True, non_graphical=False, close_on_exit=True)
# print(desktop.odesktop)


HBCPM = Maxwell3d(
                design=DesignName,
                solution_type="",
                version=AedtVersion,
                new_desktop=True, 
                non_graphical=False, 
                close_on_exit=True)

params = {
    "NumPolePairs": 8,
    "StatorPoleNumber": 12,
    "RadialPM": True,
	"RadialPMPoleArcRatio": 0.8,
	
    "RadialPMThickness": 2,

    "RotorInnerRadius": 16.6,
    "RotorCenterThickness": 8,
    "RotorOuterRadius": 25,

    "RotorPMAxialThickness": 2,
    "RotorPMAxialRadialWidth": 3,

    "RotorIronOuterRadius": 25,
    "RotorIronThickness": 1.5,

    "StatorInnerRadius": 27,
    "StatorAxialThickness": 8,
    "StatorOuterRadius": 56,
    "StatorPoleWidthArcRatio": 0.57,
    "StatorYokeWidth": 8,

    "StatorPMRadialWidth": 3,
    "StatorPMThickness": 2,
    "StatorIronThickness": 1.5,

    "StatorPoleToothWidthArcRatio": 1 / 4,
    "StatorPoleTeethAngle": 45,

    "WindingRadialLength": 13.3,

    "rpm": 3000,
    "turnm": 90,
    "turns": 100,
    "Im": 2,
    "R_phase": 0.6,

	"Is_a":1,
    "Is_b":1,
}

HBCPMSimuPara = HBCPMConcentratedWindingParameters(params)

HBCPM.solution_type = HBCPM.SOLUTIONS.Maxwell3d.Transient

oProject =desktop.odesktop.GetActiveProject()
oProject.Rename("C:/he/HBCPM/"+ProjectName, True)
# "C:/he/HBCPM/HBCPMProject.aedt"


oDesign = oProject.GetActiveDesign()

oEditor = oDesign.SetActiveEditor("3D Modeler")

print(oDesign)
print(oProject)
print(oEditor)

# Define variables and expressions in a dictionary
variables = {
	"RadialPMNumber":str(HBCPMSimuPara.NumPolePairs),
	"StatorPoleNumber":str(HBCPMSimuPara.StatorPoleNumber),
	"RadialPMAngle": str(HBCPMSimuPara.RadialPMAngle)+"deg",

    "RotorInnerRadius": str(HBCPMSimuPara.RotorInnerRadius)+"mm",
    "RotorCenterThickness": str(HBCPMSimuPara.RotorCenterThickness)+"mm",
    "RotorOuterRadius": str(HBCPMSimuPara.RotorOuterRadius)+"mm",
    "RadialPMThickness": str(HBCPMSimuPara.RadialPMThickness)+"mm",
    "RotorPMAxialThickness": str(HBCPMSimuPara.RotorPMAxialThickness)+"mm",

    "RotorIronOuterRadius": str(HBCPMSimuPara.RotorIronOuterRadius)+"mm",
    "RotorIronThickness": str(HBCPMSimuPara.RotorIronThickness)+"mm",
    
	"RotorPMAxialOuterRadius": str(HBCPMSimuPara.RotorPMAxialOuterRadius)+"mm",
    "RotorPMInnerRadius": str(HBCPMSimuPara.RotorPMInnerRadius)+"mm",

    "StatorYokeWidth": str(HBCPMSimuPara.StatorYokeWidth)+"mm",
    "StatorInnerRadius": str(HBCPMSimuPara.StatorInnerRadius)+"mm",
    "StatorAxialThickness": str(HBCPMSimuPara.StatorAxialThickness)+"mm",
    "StatorOuterRadius": str(HBCPMSimuPara.StatorOuterRadius)+"mm",

    "StatorPoleWidth": str(HBCPMSimuPara.StatorPoleWidth)+"mm",
    "StatorPMOuterRadius": str(HBCPMSimuPara.StatorPMOuterRadius)+"mm",
    "StatorPMThickness": str(HBCPMSimuPara.StatorPMThickness)+"mm",
    "StatorIronThickness": str(HBCPMSimuPara.StatorIronThickness)+"mm",
    "StatorIronOuterRadius": str(HBCPMSimuPara.StatorIronOuterRadius)+"mm",
    "RotorIronInnerRadius": str(HBCPMSimuPara.RotorIronInnerRadius)+"mm",

    "StatorPoleTeethAdditionLength": str(HBCPMSimuPara.StatorPoleWidth/4)+"mm",
	"StatorPoleTeethAngle":  str(HBCPMSimuPara.StatorPoleTeethAngle)+"deg",

    "StatorPoleTeethStartX": str(HBCPMSimuPara.StatorPoleTeethStartX)+"mm",


	"SusWindThickness": str(HBCPMSimuPara.SusWindThickness)+"mm",
    "SusWindingLength": str(HBCPMSimuPara.SusWindLength)+"mm",
	"WindingThickness": str(HBCPMSimuPara.WindingThickness)+"mm",
    "WindingRadialLength": str(HBCPMSimuPara.WindingRadialLength)+"mm",
    "rpm": str(HBCPMSimuPara.rpm),

    "turnm": str(HBCPMSimuPara.turnm),
    "turns": str(HBCPMSimuPara.turns),
    "Im": str(HBCPMSimuPara.Im)+"A",
	"Is_a": str(HBCPMSimuPara.Is_a)+"A",
	"Is_b": str(HBCPMSimuPara.Is_b)+"A",

    "ImA": "Im*cos(rpm/60*2*pi*time*RadialPMNumber+pi/2)",
    "ImB": "Im*cos(rpm/60*2*pi*time*RadialPMNumber+pi/2-2*pi/3)",
    "ImC": "Im*cos(rpm/60*2*pi*time*RadialPMNumber+pi/2+2*pi/3)",

    "NumPolePairs":str(HBCPMSimuPara.NumPolePairs),

    "R_phase":str(HBCPMSimuPara.R_phase)+"Ohm"
}

# Save the dictionary as a JSON file
with open("Para.json", "w") as json_file:
    json.dump(variables, json_file, indent=4)

print("Parameters saved to Para.json successfully!")

# This call returns the VariableManager class
# Iterate through the dictionary and set each variable
for var_name, expression in variables.items():
    HBCPM.variable_manager.set_variable(var_name, expression=expression)

# Define new materials
# Load from JSON file
with open('JFE_Steel_35JNE300_lamination_data.json', 'r') as f:
    JFE_Steel_35JNE300_lamination_data = json.load(f)


oDefinitionManager = oProject.GetDefinitionManager()

oDefinitionManager.AddMaterial(
	[
		"NAME:TDK_NEOREC40TH_60cel_Radial",
		"CoordinateSystemType:=", "Cylindrical",
		"BulkOrSurfaceType:="	, 1,
		[
			"NAME:PhysicsTypes",
			"set:="			, ["Electromagnetic"]
		],
		"permeability:="	, "1.04035644080587",
		"conductivity:="	, "769230.769",
		[
			"NAME:magnetic_coercivity",
			"property_type:="	, "VectorProperty",
			"Magnitude:="		, "-956678.252234359A_per_meter",
			"DirComp1:="		, "1",
			"DirComp2:="		, "0",
			"DirComp3:="		, "0",
		]
	])

oDefinitionManager.AddMaterial(
	[
		"NAME:TDK_NEOREC40TH_60cel_Down",
		"CoordinateSystemType:=", "Cartesian",
		"BulkOrSurfaceType:="	, 1,
		[
			"NAME:PhysicsTypes",
			"set:="			, ["Electromagnetic"]
		],
		"permeability:="	, "1.04035644080587",
		"conductivity:="	, "769230.769",
		[
			"NAME:magnetic_coercivity",
			"property_type:="	, "VectorProperty",
			"Magnitude:="		, "-956678.252234359A_per_meter",
			"DirComp1:="		, "0",
			"DirComp2:="		, "0",
			"DirComp3:="		, "-1"
		]
	])

oDefinitionManager.AddMaterial(
	[
		"NAME:TDK_NEOREC40TH_60cel_Up",
		"CoordinateSystemType:=", "Cartesian",
		"BulkOrSurfaceType:="	, 1,
		[
			"NAME:PhysicsTypes",
			"set:="			, ["Electromagnetic"]
		],
		"permeability:="	, "1.04035644080587",
		"conductivity:="	, "769230.769",
		[
			"NAME:magnetic_coercivity",
			"property_type:="	, "VectorProperty",
			"Magnitude:="		, "-956678.252234359A_per_meter",
			"DirComp1:="		, "0",
			"DirComp2:="		, "0",
			"DirComp3:="		, "1"
		]
	])

oDefinitionManager.AddMaterial(JFE_Steel_35JNE300_lamination_data)


# Create 3D model
# define the object in Create, Duplicate function
# the object is actually the name or namelist of the each instance

# Rotor main body
###################################################################################

BuildMotor=True
CreateMesh=True
AssignBoundryBand=True
CreateExcitation=True
Createsetup=True
Postprocessing=True
BuildInOptimization=False

if (BuildMotor==True):
	print("BuildMotor")

	oEditor = oDesign.SetActiveEditor("3D Modeler")

	Rotor = oEditor.CreateRectangle(
		[
			"NAME:RectangleParameters",
			"IsCovered:="		, True,
			"XStart:="		, "RotorInnerRadius",
			"YStart:="		, "-RotorCenterThickness/2",
			"ZStart:="		, "0mm",
			"Width:="		, "RotorOuterRadius-RotorInnerRadius",
			"Height:="		, "RotorCenterThickness",
			"WhichAxis:="		, "Z"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "Rotor",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"JFE_Steel_35JNE300_lamination\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"ReferenceTemperature:=", "20cel",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])

	oEditor.SweepAroundAxis(
		[
			"NAME:Selections",
			"Selections:="		, Rotor,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:AxisSweepParameters",
			"DraftAngle:="		, "0deg",
			"DraftType:="		, "Round",
			"CheckFaceFaceIntersection:=", False,
			"ClearAllIDs:="		, False,
			"SweepAxis:="		, "Y",
			"SweepAngle:="		, "360deg",
			"NumOfSegments:="	, "0"
		])

	# Rotor radial PM
	if (HBCPMSimuPara.RadialPM == True):
		RotorRadialPM = oEditor.CreateRectangle(
			[
				"NAME:RectangleParameters",
				"IsCovered:="		, True,
				"XStart:="		, "RotorOuterRadius-RadialPMThickness",
				"YStart:="		, "-RotorCenterThickness/2",
				"ZStart:="		, "0mm",
				"Width:="		, "RadialPMThickness",
				"Height:="		, "RotorCenterThickness",
				"WhichAxis:="		, "Z"
			], 
			[
				"NAME:Attributes",
				"Name:="		, "RotorRadialPM",
				"Flags:="		, "",
				"Color:="		, "(143 175 143)",
				"Transparency:="	, 0,
				"PartCoordinateSystem:=", "Global",
				"UDMId:="		, "",
				"MaterialValue:="	, "\"TDK_NEOREC40TH_60cel_Radial\"",
				"SurfaceMaterialValue:=", "\"\"",
				"SolveInside:="		, True,
				"ShellElement:="	, False,
				"ShellElementThickness:=", "0mm",
				"ReferenceTemperature:=", "20cel",
				"IsMaterialEditable:="	, True,
				"UseMaterialAppearance:=", False,
				"IsLightweight:="	, False
			])
	else:
		RotorRadialPM = oEditor.CreateRectangle(
			[
				"NAME:RectangleParameters",
				"IsCovered:="		, True,
				"XStart:="		, "RotorOuterRadius-RadialPMThickness",
				"YStart:="		, "-RotorCenterThickness/2",
				"ZStart:="		, "0mm",
				"Width:="		, "RadialPMThickness",
				"Height:="		, "RotorCenterThickness",
				"WhichAxis:="		, "Z"
			], 
			[
				"NAME:Attributes",
				"Name:="		, "RotorRadialPM",
				"Flags:="		, "",
				"Color:="		, "(143 175 143)",
				"Transparency:="	, 0,
				"PartCoordinateSystem:=", "Global",
				"UDMId:="		, "",
				"MaterialValue:="	, "\"vacuum\"",
				"SurfaceMaterialValue:=", "\"\"",
				"SolveInside:="		, True,
				"ShellElement:="	, False,
				"ShellElementThickness:=", "0mm",
				"ReferenceTemperature:=", "20cel",
				"IsMaterialEditable:="	, True,
				"UseMaterialAppearance:=", False,
				"IsLightweight:="	, False
			])


	oEditor.SweepAroundAxis(
		[
			"NAME:Selections",
			"Selections:="		, RotorRadialPM,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:AxisSweepParameters",
			"DraftAngle:="		, "0deg",
			"DraftType:="		, "Round",
			"CheckFaceFaceIntersection:=", False,
			"ClearAllIDs:="		, False,
			"SweepAxis:="		, "Y",
			"SweepAngle:="		, "RadialPMAngle/2",
			"NumOfSegments:="	, "0"
		])

	RotorRadialPMhalf = oEditor.DuplicateMirror(
		[
			"NAME:Selections",
			"Selections:="		, RotorRadialPM,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:DuplicateToMirrorParameters",
			"DuplicateMirrorBaseX:=", "0mm",
			"DuplicateMirrorBaseY:=", "0mm",
			"DuplicateMirrorBaseZ:=", "0mm",
			"DuplicateMirrorNormalX:=", "0mm",
			"DuplicateMirrorNormalY:=", "0mm",
			"DuplicateMirrorNormalZ:=", "1mm"
		], 
		[
			"NAME:Options",
			"DuplicateAssignments:=", True
		], 
		[
			"CreateGroupsForNewObjects:=", False
		])

	RotorRadialPMhalfList=[RotorRadialPM]
	RotorRadialPMhalfList.extend(RotorRadialPMhalf)

	oEditor.Unite(
		[
			"NAME:Selections",
			"Selections:="		, ",".join(map(str, RotorRadialPMhalfList))
		], 
		[
			"NAME:UniteParameters",
			"KeepOriginals:="	, False,
			"TurnOnNBodyBoolean:="	, True
		])

	RotorRadialPMDupt = oEditor.DuplicateAroundAxis(
		[
			"NAME:Selections",
			"Selections:="		, RotorRadialPM,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:DuplicateAroundAxisParameters",
			"CreateNewObjects:="	, True,
			"WhichAxis:="		, "Y",
			"AngleStr:="		, "(360/RadialPMNumber)deg",
			"NumClones:="		, "RadialPMNumber"
		], 
		[
			"NAME:Options",
			"DuplicateAssignments:=", True
		], 
		[
			"CreateGroupsForNewObjects:=", False
		])

	#  define all object of PM
	RotorRadialPMList=[RotorRadialPM]
	RotorRadialPMList.extend(RotorRadialPMDupt)
	# print(RotorRadialPMList)

	oEditor.Subtract(
		[
			"NAME:Selections",
			"Blank Parts:="		, "Rotor",
			"Tool Parts:="		, ",".join(map(str, RotorRadialPMList))
		], 
		[
			"NAME:SubtractParameters",
			"KeepOriginals:="	, True,
			"TurnOnNBodyBoolean:="	, True
		])

	print("Create "+ Rotor + " successful")

	# Rotor axial PM
	RotorAxialPM = oEditor.CreateRectangle(
		[
			"NAME:RectangleParameters",
			"IsCovered:="		, True,
			"XStart:="		, "RotorPMInnerRadius",
			"YStart:="		, "RotorCenterThickness/2",
			"ZStart:="		, "0mm",
			"Width:="		, "RotorPMAxialOuterRadius-RotorPMInnerRadius",
			"Height:="		, "RotorPMAxialThickness",
			"WhichAxis:="		, "Z"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "RotorAxialPM",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"TDK_NEOREC40TH_60cel_Down\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"ReferenceTemperature:=", "20cel",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])

	oEditor.SweepAroundAxis(
		[
			"NAME:Selections",
			"Selections:="		, RotorAxialPM,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:AxisSweepParameters",
			"DraftAngle:="		, "0deg",
			"DraftType:="		, "Round",
			"CheckFaceFaceIntersection:=", False,
			"ClearAllIDs:="		, False,
			"SweepAxis:="		, "Y",
			"SweepAngle:="		, "360deg",
			"NumOfSegments:="	, "0"
		])

	RotorAxialPMDupt = oEditor.DuplicateMirror(
		[
			"NAME:Selections",
			"Selections:="		, RotorAxialPM,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:DuplicateToMirrorParameters",
			"DuplicateMirrorBaseX:=", "0mm",
			"DuplicateMirrorBaseY:=", "0mm",
			"DuplicateMirrorBaseZ:=", "0mm",
			"DuplicateMirrorNormalX:=", "0mm",
			"DuplicateMirrorNormalY:=", "-1mm",
			"DuplicateMirrorNormalZ:=", "0mm"
		], 
		[
			"NAME:Options",
			"DuplicateAssignments:=", True
		], 
		[
			"CreateGroupsForNewObjects:=", False
		])

	RotorAxialPMList=[RotorAxialPM]

	RotorAxialPMList.extend(RotorAxialPMDupt)
	# print(RotorAxialPMList)

	oEditor.ChangeProperty(
		[
			"NAME:AllTabs",
			[
				"NAME:Geometry3DAttributeTab",
				[
					"NAME:PropServers", 
					RotorAxialPMList[1], 
				],
				[
					"NAME:ChangedProps",
					[
						"NAME:Material",
						"Value:="		, "\"TDK_NEOREC40TH_60cel_Up\""
					]
				]
			]
		])

	print("Create "+ str(RotorAxialPMList) + " successful")

	# Rotor axial Iron
	RotorAxialIron = oEditor.CreateRectangle(
		[
			"NAME:RectangleParameters",
			"IsCovered:="		, True,
			"XStart:="		, "RotorIronOuterRadius",
			"YStart:="		, "RotorCenterThickness/2+RotorPMAxialThickness",
			"ZStart:="		, "0mm",
			"Width:="		, "-(RotorIronOuterRadius-RotorIronInnerRadius)",
			"Height:="		, "RotorIronThickness",
			"WhichAxis:="		, "Z"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "RotorAxialIron",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"iron\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"ReferenceTemperature:=", "20cel",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])

	oEditor.SweepAroundAxis(
		[
			"NAME:Selections",
			"Selections:="		, RotorAxialIron,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:AxisSweepParameters",
			"DraftAngle:="		, "0deg",
			"DraftType:="		, "Round",
			"CheckFaceFaceIntersection:=", False,
			"ClearAllIDs:="		, False,
			"SweepAxis:="		, "Y",
			"SweepAngle:="		, "360deg",
			"NumOfSegments:="	, "0"
		])

	RotorAxialIronDupt = oEditor.DuplicateMirror(
		[
			"NAME:Selections",
			"Selections:="		, RotorAxialIron,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:DuplicateToMirrorParameters",
			"DuplicateMirrorBaseX:=", "0mm",
			"DuplicateMirrorBaseY:=", "0mm",
			"DuplicateMirrorBaseZ:=", "25mm",
			"DuplicateMirrorNormalX:=", "0mm",
			"DuplicateMirrorNormalY:=", "-1mm",
			"DuplicateMirrorNormalZ:=", "0mm"
		], 
		[
			"NAME:Options",
			"DuplicateAssignments:=", True
		], 
		[
			"CreateGroupsForNewObjects:=", False
		])

	RotorAxialIronList=[RotorAxialIron]
	RotorAxialIronList.extend(RotorAxialIronDupt)

	print("Create " + str(RotorAxialIronList) + " successful")

	###################################################################################

	# Stator axial PM
	StatorAxialPM = oEditor.CreateRectangle(
		[
			"NAME:RectangleParameters",
			"IsCovered:="		, True,
			"XStart:="		, "StatorInnerRadius",
			"YStart:="		, "StatorAxialThickness/2",
			"ZStart:="		, "0mm",
			"Width:="		, "StatorPMOuterradius-StatorInnerRadius",
			"Height:="		, "StatorPMThickness",
			"WhichAxis:="		, "Z"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "StatorAxialPM",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"TDK_NEOREC40TH_60cel_Up\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"ReferenceTemperature:=", "20cel",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])

	oEditor.SweepAroundAxis(
		[
			"NAME:Selections",
			"Selections:="		, StatorAxialPM,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:AxisSweepParameters",
			"DraftAngle:="		, "0deg",
			"DraftType:="		, "Round",
			"CheckFaceFaceIntersection:=", False,
			"ClearAllIDs:="		, False,
			"SweepAxis:="		, "Y",
			"SweepAngle:="		, "360deg",
			"NumOfSegments:="	, "0"
		])

	StatorAxialPMDupt = oEditor.DuplicateMirror(
		[
			"NAME:Selections",
			"Selections:="		,  StatorAxialPM,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:DuplicateToMirrorParameters",
			"DuplicateMirrorBaseX:=", "0mm",
			"DuplicateMirrorBaseY:=", "0mm",
			"DuplicateMirrorBaseZ:=", "0mm",
			"DuplicateMirrorNormalX:=", "0mm",
			"DuplicateMirrorNormalY:=", "-1mm",
			"DuplicateMirrorNormalZ:=", "0mm"
		], 
		[
			"NAME:Options",
			"DuplicateAssignments:=", True
		], 
		[
			"CreateGroupsForNewObjects:=", False
		])

	StatorAxialPMList=[StatorAxialPM]

	StatorAxialPMList.extend(StatorAxialPMDupt)
	# print(RotorAxialPMList)

	oEditor.ChangeProperty(
		[
			"NAME:AllTabs",
			[
				"NAME:Geometry3DAttributeTab",
				[
					"NAME:PropServers", 
					StatorAxialPMList[1], 
				],
				[
					"NAME:ChangedProps",
					[
						"NAME:Material",
						"Value:="		, "\"TDK_NEOREC40TH_60cel_Down\""
					]
				]
			]
		])

	print("Create "+ str(StatorAxialPMList) + " successful")


	# Stator axial Iron
	StatorAxialIron = oEditor.CreateRectangle(
		[
			"NAME:RectangleParameters",
			"IsCovered:="		, True,
			"XStart:="		, "StatorInnerRadius",
			"YStart:="		, "StatorAxialThickness/2+StatorPMThickness",
			"ZStart:="		, "0mm",
			"Width:="		, "StatorIronOuterRadius-StatorInnerRadius",
			"Height:="		, "StatorIronThickness",
			"WhichAxis:="		, "Z"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "StatorAxialIron",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"iron\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"ReferenceTemperature:=", "20cel",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])

	oEditor.SweepAroundAxis(
		[
			"NAME:Selections",
			"Selections:="		, StatorAxialIron,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:AxisSweepParameters",
			"DraftAngle:="		, "0deg",
			"DraftType:="		, "Round",
			"CheckFaceFaceIntersection:=", False,
			"ClearAllIDs:="		, False,
			"SweepAxis:="		, "Y",
			"SweepAngle:="		, "360deg",
			"NumOfSegments:="	, "0"
		])

	StatorAxialIronDupt = oEditor.DuplicateMirror(
		[
			"NAME:Selections",
			"Selections:="		, StatorAxialIron,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:DuplicateToMirrorParameters",
			"DuplicateMirrorBaseX:=", "0mm",
			"DuplicateMirrorBaseY:=", "0mm",
			"DuplicateMirrorBaseZ:=", "25mm",
			"DuplicateMirrorNormalX:=", "0mm",
			"DuplicateMirrorNormalY:=", "-1mm",
			"DuplicateMirrorNormalZ:=", "0mm"
		], 
		[
			"NAME:Options",
			"DuplicateAssignments:=", True
		], 
		[
			"CreateGroupsForNewObjects:=", False
		])

	StatorAxialIronList=[StatorAxialIron]
	StatorAxialIronList.extend(StatorAxialIronDupt)

	print("Create " + str(StatorAxialIron) + " successful")


	# Create stator Pole and Yoke

	# Stator Yoke
	Stator = oEditor.CreateRectangle(
		[
			"NAME:RectangleParameters",
			"IsCovered:="		, True,
			"XStart:="		, "StatorOuterRadius-StatorYokeWidth",
			"YStart:="		, "-StatorAxialThickness/2",
			"ZStart:="		, "0mm",
			"Width:="		, "StatorYokeWidth",
			"Height:="		, "StatorAxialThickness",
			"WhichAxis:="		, "Z"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "Stator",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"JFE_Steel_35JNE300_lamination\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"ReferenceTemperature:=", "20cel",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])

	oEditor.SweepAroundAxis(
		[
			"NAME:Selections",
			"Selections:="		, Stator,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:AxisSweepParameters",
			"DraftAngle:="		, "0deg",
			"DraftType:="		, "Round",
			"CheckFaceFaceIntersection:=", False,
			"ClearAllIDs:="		, False,
			"SweepAxis:="		, "Y",
			"SweepAngle:="		, "360deg",
			"NumOfSegments:="	, "0"
		])

	print("Create " + str(Stator) + " successful")

	# Stator Pole
	StatorPole = oEditor.CreateRectangle(
		[
			"NAME:RectangleParameters",
			"IsCovered:="		, True,
			"XStart:="		, "0mm",
			"YStart:="		, "-StatorAxialThickness/2",
			"ZStart:="		, "0mm",
			"Width:="		, "StatorOuterRadius",
			"Height:="		, "StatorAxialThickness",
			"WhichAxis:="		, "Z"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "StatorPole",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"JFE_Steel_35JNE300_lamination\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"ReferenceTemperature:=", "20cel",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])

	oEditor.SweepAlongVector(
		[
			"NAME:Selections",
			"Selections:="		, StatorPole,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:VectorSweepParameters",
			"DraftAngle:="		, "0deg",
			"DraftType:="		, "Round",
			"CheckFaceFaceIntersection:=", False,
			"ClearAllIDs:="		, False,
			"SweepVectorX:="	, "0mm",
			"SweepVectorY:="	, "0mm",
			"SweepVectorZ:="	, "StatorPoleWidth/2"
		])


	StatorPolehalfDupt = oEditor.DuplicateMirror(
		[
			"NAME:Selections",
			"Selections:="		, StatorPole,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:DuplicateToMirrorParameters",
			"DuplicateMirrorBaseX:=", "0mm",
			"DuplicateMirrorBaseY:=", "-4mm",
			"DuplicateMirrorBaseZ:=", "0mm",
			"DuplicateMirrorNormalX:=", "0mm",
			"DuplicateMirrorNormalY:=", "0mm",
			"DuplicateMirrorNormalZ:=", "-1mm"
		], 
		[
			"NAME:Options",
			"DuplicateAssignments:=", True
		], 
		[
			"CreateGroupsForNewObjects:=", False
		])
	# return StatorPolehalfDupt is a list

	StatorPoleList=[StatorPole]

	StatorPoleList.extend(StatorPolehalfDupt)

	oEditor.Unite(
		[
			"NAME:Selections",
			"Selections:="		, ",".join(map(str, StatorPoleList))
		], 
		[
			"NAME:UniteParameters",
			"KeepOriginals:="	, False,
			"TurnOnNBodyBoolean:="	, True
		])

	StatorPoleIntersector = oEditor.CreateRectangle(
		[
			"NAME:RectangleParameters",
			"IsCovered:="		, True,
			"XStart:="		, "StatorInnerRadius",
			"YStart:="		, "-StatorAxialThickness/2",
			"ZStart:="		, "0mm",
			"Width:="		, "StatorOuterRadius-StatorInnerRadius-StatorYokeWidth",
			"Height:="		, "StatorAxialThickness",
			"WhichAxis:="		, "Z"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "StatorPoleIntersector",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"ReferenceTemperature:=", "20cel",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])
	# return StatorPoleIntersector is a single str

	oEditor.SweepAroundAxis(
		[
			"NAME:Selections",
			"Selections:="		, StatorPoleIntersector,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:AxisSweepParameters",
			"DraftAngle:="		, "0deg",
			"DraftType:="		, "Round",
			"CheckFaceFaceIntersection:=", False,
			"ClearAllIDs:="		, False,
			"SweepAxis:="		, "Y",
			"SweepAngle:="		, "360deg",
			"NumOfSegments:="	, "0"
		])

	StatorPoleIntersectorList=[StatorPole,StatorPoleIntersector]
	# print(StatorPoleIntersectorList)

	oEditor.Intersect(
		[
			"NAME:Selections",
			"Selections:="		, ",".join(map(str, StatorPoleIntersectorList))
		], 
		[
			"NAME:IntersectParameters",
			"KeepOriginals:="	, False,
			"TurnOnNBodyBoolean:="	, True
		])

	print("Create " + str(StatorPole) + " successful")

	# Stator tooth
	StatorTooth = oEditor.CreateRectangle(
		[
			"NAME:RectangleParameters",
			"IsCovered:="		, True,
			"XStart:="		, "0mm",
			"YStart:="		, "-StatorAxialThickness/2",
			"ZStart:="		, "StatorPoleWidth/2",
			"Width:="		, "StatorOuterRadius",
			"Height:="		, "StatorAxialThickness",
			"WhichAxis:="		, "Z"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "StatorTooth",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"JFE_Steel_35JNE300_lamination\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"ReferenceTemperature:=", "20cel",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])

	oEditor.SweepAlongVector(
		[
			"NAME:Selections",
			"Selections:="		, "StatorTooth",
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:VectorSweepParameters",
			"DraftAngle:="		, "0deg",
			"DraftType:="		, "Round",
			"CheckFaceFaceIntersection:=", False,
			"ClearAllIDs:="		, False,
			"SweepVectorX:="	, "0mm",
			"SweepVectorY:="	, "0mm",
			"SweepVectorZ:="	, "StatorPoleTeethAdditionLength"
		])

	StatorToothIntersector1 = oEditor.CreateRectangle(
		[
			"NAME:RectangleParameters",
			"IsCovered:="		, True,
			"XStart:="		, "StatorInnerRadius",
			"YStart:="		, "-StatorAxialThickness/2",
			"ZStart:="		, "0",
			"Width:="		, "StatorPMOuterRadius-StatorInnerRadius",
			"Height:="		, "StatorAxialThickness",
			"WhichAxis:="		, "Z"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "StatorToothIntersector1",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"ReferenceTemperature:=", "20cel",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])

	oEditor.SweepAroundAxis(
		[
			"NAME:Selections",
			"Selections:="		, StatorToothIntersector1,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:AxisSweepParameters",
			"DraftAngle:="		, "0deg",
			"DraftType:="		, "Round",
			"CheckFaceFaceIntersection:=", False,
			"ClearAllIDs:="		, False,
			"SweepAxis:="		, "Y",
			"SweepAngle:="		, "360deg",
			"NumOfSegments:="	, "0"
		])

	StatorToothIntersector2 = oEditor.CreatePolyline(
		[
			"NAME:PolylineParameters",
			"IsPolylineCovered:="	, True,
			"IsPolylineClosed:="	, False,
			[
				"NAME:PolylinePoints",
				[
					"NAME:Point1",
					"X:="			, "StatorPoleTeethStartX",
					"Y:="			, "-StatorAxialThickness/2",
					"Z:="			, "StatorPoleWidth/2"
				],
				[
					"NAME:Point2",
					"X:="			, "StatorPoleTeethStartX",
					"Y:="			, "-StatorAxialThickness/2",
					"Z:="			, "20mm"

				]
			],
			[
				"NAME:PolylineSegments",
				[
					"NAME:PLSegment",
					"SegmentType:="		, "Line",
					"StartIndex:="		, 0,
					"NoOfPoints:="		, 2
				]
			],
			[
				"NAME:PolylineXSection",
				"XSectionType:="	, "None",
				"XSectionOrient:="	, "Auto",
				"XSectionWidth:="	, "0mm",
				"XSectionTopWidth:="	, "0mm",
				"XSectionHeight:="	, "0mm",
				"XSectionNumSegments:="	, "0",
				"XSectionBendType:="	, "Corner"
			]
		], 
		[
			"NAME:Attributes",
			"Name:="		, "StatorToothIntersector2",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"ReferenceTemperature:=", "20cel",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])

	oEditor.SweepAlongVector(
		[
			"NAME:Selections",
			"Selections:="		, StatorToothIntersector2,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:VectorSweepParameters",
			"DraftAngle:="		, "0deg",
			"DraftType:="		, "Round",
			"CheckFaceFaceIntersection:=", False,
			"ClearAllIDs:="		, False,
			"SweepVectorX:="	, "0mm",
			"SweepVectorY:="	, "StatorAxialThickness",
			"SweepVectorZ:="	, "0mm"
		])

	oEditor.SweepAlongVector(
		[
			"NAME:Selections",
			"Selections:="		, StatorToothIntersector2,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:VectorSweepParameters",
			"DraftAngle:="		, "0deg",
			"DraftType:="		, "Round",
			"CheckFaceFaceIntersection:=", False,
			"ClearAllIDs:="		, False,
			"SweepVectorX:="	, "-4mm",
			"SweepVectorY:="	, "0mm",
			"SweepVectorZ:="	, "0mm"
		])

	oEditor.Move(
		[
			"NAME:Selections",
			"Selections:="		, StatorToothIntersector2,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:TranslateParameters",
			"TranslateVectorX:="	, "-StatorPoleTeethStartX",
			"TranslateVectorY:="	, "0mm",
			"TranslateVectorZ:="	, "-StatorPoleWidth/2"
		])

	oEditor.Rotate(
		[
			"NAME:Selections",
			"Selections:="		, StatorToothIntersector2,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:RotateParameters",
			"RotateAxis:="		, "Y",
			"RotateAngle:="		, "-StatorPoleTeethAngle"
		])

	oEditor.Move(
		[
			"NAME:Selections",
			"Selections:="		, StatorToothIntersector2,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:TranslateParameters",
			"TranslateVectorX:="	, "StatorPoleTeethStartX",
			"TranslateVectorY:="	, "0mm",
			"TranslateVectorZ:="	, "StatorPoleWidth/2"
		])

	StatorToothList=[StatorTooth,StatorToothIntersector1,StatorToothIntersector2]

	oEditor.Intersect(
		[
			"NAME:Selections",
			"Selections:="		, ",".join(map(str, StatorToothList))
		], 
		[
			"NAME:IntersectParameters",
			"KeepOriginals:="	, False,
			"TurnOnNBodyBoolean:="	, True
		])

	print("Create " + str(StatorTooth) + " successful")

	StatorToothDul=oEditor.DuplicateMirror(
		[
			"NAME:Selections",
			"Selections:="		, StatorTooth,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:DuplicateToMirrorParameters",
			"DuplicateMirrorBaseX:=", "0mm",
			"DuplicateMirrorBaseY:=", "0mm",
			"DuplicateMirrorBaseZ:=", "0mm",
			"DuplicateMirrorNormalX:=", "0mm",
			"DuplicateMirrorNormalY:=", "0mm",
			"DuplicateMirrorNormalZ:=", "-1mm"
		], 
		[
			"NAME:Options",
			"DuplicateAssignments:=", True
		], 
		[
			"CreateGroupsForNewObjects:=", False
		])

	StatorToothUnionList = [StatorPole,StatorTooth]
	StatorToothUnionList.extend(StatorToothDul)

	print(StatorToothUnionList)

	oEditor.Unite(
		[
			"NAME:Selections",
			"Selections:="		, ",".join(map(str, StatorToothUnionList))
		], 
		[
			"NAME:UniteParameters",
			"KeepOriginals:="	, False,
			"TurnOnNBodyBoolean:="	, True
		])

	StatorToothUnion = oEditor.DuplicateAroundAxis(
		[
			"NAME:Selections",
			"Selections:="		, StatorToothUnionList[0],
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:DuplicateAroundAxisParameters",
			"CreateNewObjects:="	, True,
			"WhichAxis:="		, "Y",
			"AngleStr:="		, "(360/StatorPoleNumber)deg",
			"NumClones:="		, "StatorPoleNumber"
		], 
		[
			"NAME:Options",
			"DuplicateAssignments:=", True
		], 
		[
			"CreateGroupsForNewObjects:=", False
		])

	StatorList=[Stator,StatorToothUnionList[0]]
	StatorList.extend(StatorToothUnion)

	oEditor.Unite(
		[
			"NAME:Selections",
			"Selections:="		, ",".join(map(str, StatorList))
		], 
		[
			"NAME:UniteParameters",
			"KeepOriginals:="	, False,
			"TurnOnNBodyBoolean:="	, True
		])

	print("Create " + str(StatorList) + " successful")



	###################################################################
	#Create Armature Windings

	ArmatureWindingsubtractor = oEditor.CreateRectangle(
		[
			"NAME:RectangleParameters",
			"IsCovered:="		, True,
			"XStart:="		, "-StatorPoleWidth/2-0.3mm",
			"YStart:="		, "-StatorAxialThickness/2-0.3mm",
			"ZStart:="		, "0mm",
			"Width:="		, "StatorPoleWidth+0.6mm",
			"Height:="		, "StatorAxialThickness+0.6mm",
			"WhichAxis:="		, "Z"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "ArmatureWindingsubtractor",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"copper\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"ReferenceTemperature:=", "20cel",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])

	ArmatureWinding = oEditor.CreateRectangle(
		[
			"NAME:RectangleParameters",
			"IsCovered:="		, True,
			"XStart:="		, "-StatorPoleWidth/2-0.3mm-WindingThickness",
			"YStart:="		, "-StatorAxialThickness/2-0.3mm-WindingThickness",
			"ZStart:="		, "0mm",
			"Width:="		, "StatorPoleWidth+0.6mm+2*WindingThickness",
			"Height:="		, "StatorAxialThickness+0.6mm+2*WindingThickness",
			"WhichAxis:="		, "Z"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "ArmatureWinding",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"copper\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"ReferenceTemperature:=", "20cel",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])

	oEditor.Subtract(
		[
			"NAME:Selections",
			"Blank Parts:="		, ArmatureWinding,
			"Tool Parts:="		, ArmatureWindingsubtractor
		], 
		[
			"NAME:SubtractParameters",
			"KeepOriginals:="	, False,
			"TurnOnNBodyBoolean:="	, True
		])

	oEditor.SweepAlongVector(
		[
			"NAME:Selections",
			"Selections:="		, ArmatureWinding,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:VectorSweepParameters",
			"DraftAngle:="		, "0deg",
			"DraftType:="		, "Round",
			"CheckFaceFaceIntersection:=", False,
			"ClearAllIDs:="		, False,
			"SweepVectorX:="	, "0mm",
			"SweepVectorY:="	, "0",
			"SweepVectorZ:="	, "WindingRadialLength"
		])

	oEditor.Move(
		[
			"NAME:Selections",
			"Selections:="		, ArmatureWinding,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:TranslateParameters",
			"TranslateVectorX:="	, "0mm",
			"TranslateVectorY:="	, "0mm",
			"TranslateVectorZ:="	, "StatorPMOuterRadius+0.5mm"
		])

	ArmatureWindingDup = oEditor.DuplicateAroundAxis(
		[
			"NAME:Selections",
			"Selections:="		, ArmatureWinding,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:DuplicateAroundAxisParameters",
			"CreateNewObjects:="	, True,
			"WhichAxis:="		, "Y",
			"AngleStr:="		, "(360/StatorPoleNumber)deg",
			"NumClones:="		, "StatorPoleNumber"
		], 
		[
			"NAME:Options",
			"DuplicateAssignments:=", True
		], 
		[
			"CreateGroupsForNewObjects:=", False
		])

	ArmatureWindingList=[ArmatureWinding]
	ArmatureWindingList.extend(ArmatureWindingDup)

	print("Create " + str(ArmatureWindingList) + " successful")

	ArmatureWindingSectionList= oEditor.Section(
		[
			"NAME:Selections",
			"Selections:="		, ",".join(map(str, ArmatureWindingList)),
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:SectionToParameters",
			"CreateNewObjects:="	, True,
			"SectionPlane:="	, "ZX",
			"SectionCrossObject:="	, False
		])

	# print(ArmatureWindingSectionList)

	ArmatureWindingSectionSeparateList = oEditor.SeparateBody(
		[
			"NAME:Selections",
			"Selections:="		, ",".join(map(str, ArmatureWindingSectionList)),
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"CreateGroupsForNewObjects:=", False
		])

	# Create a new list with strings ending with "Separate1"
	ArmatureWindingSectionDeleteList = [s for s in ArmatureWindingSectionSeparateList if s.endswith("Separate1")]

	# print(ArmatureWindingSectionDeleteList)

	oEditor.Delete(
		[
			"NAME:Selections",
			"Selections:="		, ",".join(map(str, ArmatureWindingSectionDeleteList))
		])

	##################################################################
	#Create Suspension Windings
	SuspensionWindingsubtractor = oEditor.CreateRectangle(
		[
			"NAME:RectangleParameters",
			"IsCovered:="		, True,
			"XStart:="		, "-StatorYokeWidth/2-0.5mm",
			"YStart:="		, "-StatorAxialThickness/2-0.3mm",
			"ZStart:="		, "0mm",
			"Width:="		, "StatorYokeWidth+1mm",
			"Height:="		, "StatorAxialThickness+0.6mm",
			"WhichAxis:="		, "Z"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "SuspensionWindingsubtractor",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"copper\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"ReferenceTemperature:=", "20cel",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])

	SuspensionWinding = oEditor.CreateRectangle(
		[
			"NAME:RectangleParameters",
			"IsCovered:="		, True,
			"XStart:="		, "-StatorYokeWidth/2-SusWindThickness-0.5mm",
			"YStart:="		, "-StatorAxialThickness/2-SusWindThickness-0.3mm",
			"ZStart:="		, "0mm",
			"Width:="		, "StatorYokeWidth+2*SusWindThickness+1mm",
			"Height:="		, "StatorAxialThickness+2*SusWindThickness+0.6mm",
			"WhichAxis:="		, "Z"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "SuspensionWinding",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"copper\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"ReferenceTemperature:=", "20cel",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])

	oEditor.Subtract(
		[
			"NAME:Selections",
			"Blank Parts:="		, SuspensionWinding,
			"Tool Parts:="		, SuspensionWindingsubtractor
		], 
		[
			"NAME:SubtractParameters",
			"KeepOriginals:="	, False,
			"TurnOnNBodyBoolean:="	, True
		])

	oEditor.SweepAlongVector(
		[
			"NAME:Selections",
			"Selections:="		, SuspensionWinding,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:VectorSweepParameters",
			"DraftAngle:="		, "0deg",
			"DraftType:="		, "Round",
			"CheckFaceFaceIntersection:=", False,
			"ClearAllIDs:="		, False,
			"SweepVectorX:="	, "0mm",
			"SweepVectorY:="	, "0",
			"SweepVectorZ:="	, "SusWindingLength"
		])

	oEditor.Move(
		[
			"NAME:Selections",
			"Selections:="		, SuspensionWinding,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:TranslateParameters",
			"TranslateVectorX:="	, "0mm",
			"TranslateVectorY:="	, "0mm",
			"TranslateVectorZ:="	, "-SusWindingLength/2"
		])
	
	oEditor.Rotate(
		[
			"NAME:Selections",
			"Selections:="		, SuspensionWinding,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:RotateParameters",
			"RotateAxis:="		, "Y",
			"RotateAngle:="		, "45deg"
		])

	oEditor.Move(
		[
			"NAME:Selections",
			"Selections:="		, SuspensionWinding,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:TranslateParameters",
			"TranslateVectorX:="	, "(StatorOuterRadius-StatorYokeWidth/2)*0.707-0.3mm",# 1/sqrt(2)=0.707
			"TranslateVectorY:="	, "0mm",
			"TranslateVectorZ:="	, "-(StatorOuterRadius-StatorYokeWidth/2)*0.707+0.3mm"
		])

	oEditor.Rotate(
		[
			"NAME:Selections",
			"Selections:="		, SuspensionWinding,
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:RotateParameters",
			"RotateAxis:="		, "Y",
			"RotateAngle:="		, "-45deg"
		])

	if(HBCPMSimuPara.SuspensionWindingFullSlot == False):
		oEditor.Rotate(
			[
				"NAME:Selections",
				"Selections:="		, SuspensionWinding,
				"NewPartsModelFlag:="	, "Model"
			], 
			[
				"NAME:RotateParameters",
				"RotateAxis:="		, "Y",
				"RotateAngle:="		, "45deg"
			])

		SuspensionWindingDup = oEditor.DuplicateAroundAxis(
			[
				"NAME:Selections",
				"Selections:="		, SuspensionWinding,
				"NewPartsModelFlag:="	, "Model"
			], 
			[
				"NAME:DuplicateAroundAxisParameters",
				"CreateNewObjects:="	, True,
				"WhichAxis:="		, "Y",
				"AngleStr:="		, "90deg",
				"NumClones:="		, "4"
			], 
			[
				"NAME:Options",
				"DuplicateAssignments:=", True
			], 
			[
				"CreateGroupsForNewObjects:=", False
			])
	else:
		oEditor.Rotate(
			[
				"NAME:Selections",
				"Selections:="		, SuspensionWinding,
				"NewPartsModelFlag:="	, "Model"
			], 
			[
				"NAME:RotateParameters",
				"RotateAxis:="		, "Y",
				"RotateAngle:="		, "(360/StatorPoleNumber/2)deg"
			])

		SuspensionWindingDup = oEditor.DuplicateAroundAxis(
			[
				"NAME:Selections",
				"Selections:="		, SuspensionWinding,
				"NewPartsModelFlag:="	, "Model"
			], 
			[
				"NAME:DuplicateAroundAxisParameters",
				"CreateNewObjects:="	, True,
				"WhichAxis:="		, "Y",
				"AngleStr:="		, "(360/StatorPoleNumber)deg",
				"NumClones:="		, "StatorPoleNumber"
			], 
			[
				"NAME:Options",
				"DuplicateAssignments:=", True
			], 
			[
				"CreateGroupsForNewObjects:=", False
			])

	SuspensionWindingList=[SuspensionWinding]
	SuspensionWindingList.extend(SuspensionWindingDup)

	print("Create " + str(SuspensionWindingList) + " successful")

	SuspensionWindingSectionList= oEditor.Section(
		[
			"NAME:Selections",
			"Selections:="		, ",".join(map(str, SuspensionWindingList)),
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"NAME:SectionToParameters",
			"CreateNewObjects:="	, True,
			"SectionPlane:="	, "ZX",
			"SectionCrossObject:="	, False
		])

	# print(ArmatureWindingSectionList)

	SuspensionWindingSectionSeparateList = oEditor.SeparateBody(
		[
			"NAME:Selections",
			"Selections:="		, ",".join(map(str, SuspensionWindingSectionList)),
			"NewPartsModelFlag:="	, "Model"
		], 
		[
			"CreateGroupsForNewObjects:=", False
		])

	# Create a new list with strings ending with "Separate1"
	SuspensionWindingSectionDeleteList = [s for s in SuspensionWindingSectionSeparateList if s.endswith("Separate1")]

	# print(ArmatureWindingSectionDeleteList)

	oEditor.Delete(
		[
			"NAME:Selections",
			"Selections:="		, ",".join(map(str, SuspensionWindingSectionDeleteList))
		])

	################################################################
	# air boundry, band, air gap segment

	Air = oEditor.CreateCylinder(
		[
			"NAME:CylinderParameters",
			"XCenter:="		, "0mm",
			"YCenter:="		, "-20mm",
			"ZCenter:="		, "0mm",
			"Radius:="		, "70mm",
			"Height:="		, "40mm",
			"WhichAxis:="		, "Y",
			"NumSides:="		, "0"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "Air",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 1,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"ReferenceTemperature:=", "20cel",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])

	Band = oEditor.CreateCylinder(
		[
			"NAME:CylinderParameters",
			"XCenter:="		, "0mm",
			"YCenter:="		, "-13mm",
			"ZCenter:="		, "0mm",
			"Radius:="		, "StatorInnerRadius/2+RotorOuterRadius/2",
			"Height:="		, "26mm",
			"WhichAxis:="		, "Y",
			"NumSides:="		, "0"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "Band",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 1,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"ReferenceTemperature:=", "20cel",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])

	Airgap1 = oEditor.CreateCylinder(
		[
			"NAME:CylinderParameters",
			"XCenter:="		, "0mm",
			"YCenter:="		, "-12mm",
			"ZCenter:="		, "0mm",
			"Radius:="		, "1*StatorInnerRadius/8+7*RotorOuterRadius/8",
			"Height:="		, "24mm",
			"WhichAxis:="		, "Y",
			"NumSides:="		, "0"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "Airgap1",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 1,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"ReferenceTemperature:=", "20cel",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])

	Airgap2 = oEditor.CreateCylinder(
		[
			"NAME:CylinderParameters",
			"XCenter:="		, "0mm",
			"YCenter:="		, "-12mm",
			"ZCenter:="		, "0mm",
			"Radius:="		, "3*StatorInnerRadius/8+5*RotorOuterRadius/8",
			"Height:="		, "24mm",
			"WhichAxis:="		, "Y",
			"NumSides:="		, "0"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "Airgap2",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 1,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"ReferenceTemperature:=", "20cel",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])

	Airgap3 = oEditor.CreateCylinder(
		[
			"NAME:CylinderParameters",
			"XCenter:="		, "0mm",
			"YCenter:="		, "-12mm",
			"ZCenter:="		, "0mm",
			"Radius:="		, "4*StatorInnerRadius/8+4*RotorOuterRadius/8",
			"Height:="		, "24mm",
			"WhichAxis:="		, "Y",
			"NumSides:="		, "0"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "Airgap3",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 1,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"ReferenceTemperature:=", "20cel",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])

	Airgap4 = oEditor.CreateCylinder(
		[
			"NAME:CylinderParameters",
			"XCenter:="		, "0mm",
			"YCenter:="		, "-12mm",
			"ZCenter:="		, "0mm",
			"Radius:="		, "6*StatorInnerRadius/8+2*RotorOuterRadius/8",
			"Height:="		, "24mm",
			"WhichAxis:="		, "Y",
			"NumSides:="		, "0"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "Airgap4",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 1,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"ReferenceTemperature:=", "20cel",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])

	Airgap5 = oEditor.CreateCylinder(
		[
			"NAME:CylinderParameters",
			"XCenter:="		, "0mm",
			"YCenter:="		, "-12mm",
			"ZCenter:="		, "0mm",
			"Radius:="		, "8*StatorInnerRadius/8+0*RotorOuterRadius/8",
			"Height:="		, "24mm",
			"WhichAxis:="		, "Y",
			"NumSides:="		, "0"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "Airgap5",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 1,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"ReferenceTemperature:=", "20cel",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])

	AirgapSubtractorList=[Airgap1,Airgap2,Airgap3,Airgap4,Airgap5]

	oEditor.Subtract(
		[
			"NAME:Selections",
			"Blank Parts:="		, AirgapSubtractorList[4],
			"Tool Parts:="		, AirgapSubtractorList[3]
		], 
		[
			"NAME:SubtractParameters",
			"KeepOriginals:="	, True,
			"TurnOnNBodyBoolean:="	, True
		])

	oEditor.Subtract(
		[
			"NAME:Selections",
			"Blank Parts:="		, AirgapSubtractorList[3],
			"Tool Parts:="		, AirgapSubtractorList[2]
		], 
		[
			"NAME:SubtractParameters",
			"KeepOriginals:="	, True,
			"TurnOnNBodyBoolean:="	, True
		])

	oEditor.Subtract(
		[
			"NAME:Selections",
			"Blank Parts:="		, AirgapSubtractorList[1],
			"Tool Parts:="		, AirgapSubtractorList[0]
		], 
		[
			"NAME:SubtractParameters",
			"KeepOriginals:="	, True,
			"TurnOnNBodyBoolean:="	, True
		])

	AirgapList=[AirgapSubtractorList[4],AirgapSubtractorList[3],AirgapSubtractorList[1]]

	AirgapDeleteList=[AirgapSubtractorList[2],AirgapSubtractorList[0]]

	oEditor.Delete(
		[
			"NAME:Selections",
			"Selections:="		, ",".join(map(str, AirgapDeleteList))
		])

	print("Create " + str(AirgapList) + " successful")

	desktop.save_project()
##################################################### 
# Mesh Operation

if (CreateMesh==True):
	print("CreateMesh")

	oModule = oDesign.GetModule("MeshSetup")

	oModule.InitialMeshSettings(
		[
			"NAME:MeshSettings",
			[
				"NAME:GlobalSurfApproximation",
				"CurvedSurfaceApproxChoice:=", "UseSlider",
				"SliderMeshSettings:="	, 8
			],
			[
				"NAME:GlobalCurvilinear",
				"Apply:="		, True
			],
			[
				"NAME:GlobalModelRes",
				"UseAutoLength:="	, True
			],
			"MeshMethod:="		, "Auto",
			"UseLegacyFaceterForTauVolumeMesh:=", False,
			"DynamicSurfaceResolution:=", False,
			"UseFlexMeshingForTAUvolumeMesh:=", False,
			"UseAlternativeMeshMethodsAsFallBack:=", True,
			"AllowPhiForLayeredGeometry:=", False
		])

	TotalPMList = RotorRadialPMList+RotorAxialPMList+StatorAxialPMList
	TotalIronList = RotorAxialIronList+StatorAxialIronList

	SteelList=[Rotor]
	SteelList.append(Stator)

	# HBCPM.mesh.assign_length_mesh(assignment=AirgapList, maximum_length=0.7, maximum_elements=None, name="Airgap")

	# HBCPM.mesh.assign_length_mesh(assignment=ArmatureWindingList, maximum_length=2, maximum_elements=None, name="Winding")

	# HBCPM.mesh.assign_length_mesh(assignment=TotalPMList, maximum_length=1, maximum_elements=None, name="PMs")

	# HBCPM.mesh.assign_length_mesh(assignment=TotalPMList, maximum_length=1, maximum_elements=None, name="PMs")

	# HBCPM.mesh.assign_length_mesh(assignment=TotalIronList, maximum_length=1, maximum_elements=None, name="Iron")

	# HBCPM.mesh.assign_length_mesh(assignment=Rotor, maximum_length=2.5, maximum_elements=None, name="Rotor")

	# HBCPM.mesh.assign_length_mesh(assignment=Stator, maximum_length=2.5, maximum_elements=None, name="Stator")

	oModule.AssignLengthOp(
		[
			"NAME:Airgap",
			"RefineInside:="	, True,
			"Enabled:="		, True,
			"Objects:="		, AirgapList,
			"RestrictElem:="	, False,
			"NumMaxElem:="		, "1000",
			"RestrictLength:="	, True,
			"MaxLength:="		, "0.7mm"
		])

	oModule.AssignLengthOp(
		[
			"NAME:Winding",
			"RefineInside:="	, True,
			"Enabled:="		, True,
			"Objects:="		, ArmatureWindingList,
			"RestrictElem:="	, False,
			"NumMaxElem:="		, "1000",
			"RestrictLength:="	, True,
			"MaxLength:="		, "2mm"
		])

	oModule.AssignLengthOp(
		[
			"NAME:PM",
			"RefineInside:="	, True,
			"Enabled:="		, True,
			"Objects:="		, TotalPMList,
			"RestrictElem:="	, False,
			"NumMaxElem:="		, "1000",
			"RestrictLength:="	, True,
			"MaxLength:="		, "1mm"
		])

	oModule.AssignLengthOp(
		[
			"NAME:Iron",
			"RefineInside:="	, True,
			"Enabled:="		, True,
			"Objects:="		, TotalIronList,
			"RestrictElem:="	, False,
			"NumMaxElem:="		, "1000",
			"RestrictLength:="	, True,
			"MaxLength:="		, "1mm"
		])

	oModule.AssignLengthOp(
		[
			"NAME:Steel",
			"RefineInside:="	, True,
			"Enabled:="		, True,
			"Objects:="		, SteelList,
			"RestrictElem:="	, False,
			"NumMaxElem:="		, "1000",
			"RestrictLength:="	, True,
			"MaxLength:="		, "3mm"
		])


	###################################################################
	# Set force and torque

	oModule = oDesign.GetModule("MaxwellParameterSetup")

	RotorList=RotorAxialIronList+RotorRadialPMList+RotorAxialPMList
	RotorList.append(Rotor)

	oModule.AssignForce(
		[
			"NAME:Force",
			"Reference CS:="	, "Global",
			"Is Virtual:="		, True,
			"Objects:="		, RotorList
		])
	oModule.AssignTorque(
		[
			"NAME:TorqueRotation",
			"Is Virtual:="		, True,
			"Coordinate System:="	, "Global",
			"Axis:="		, "Y",
			"Is Positive:="		, True,
			"Objects:="		, RotorList
		])
	oModule.AssignTorque(
		[
			"NAME:TorqueTilt",
			"Is Virtual:="		, True,
			"Coordinate System:="	, "Global",
			"Axis:="		, "X",
			"Is Positive:="		, True,
			"Objects:="		, RotorList
		])

#############################################################
if (AssignBoundryBand==True):  
	print("AssignBoundryBand")
		
	# Setup boundry and band
	AirSurfaceList = HBCPM.modeler.get_object_faces(assignment=Air)

	print(AirSurfaceList)

	oModule = oDesign.GetModule("BoundarySetup")

	oModule.AssignZeroTangentialHField(
		[
			"NAME:ZeroTangentialHField",
			"Faces:="		, AirSurfaceList
		])

	HBCPM.assign_rotate_motion(
		assignment=Band,
		coordinate_system="Global",
		axis="Y",
		positive_movement=True,
		start_position="0deg",
		angular_velocity="3000rpm",
	)
###################################################################

if (CreateExcitation==True):
	print("CreateExcitation")

	# Winding configuration
	oModule = oDesign.GetModule("BoundarySetup")

	# print(ArmatureWindingSectionList)

	# Define the phase configurations
	ArmaturePhases = generate_three_phases(HBCPMSimuPara.Armature_coil_number)

	if(HBCPMSimuPara.SuspensionWindingFullSlot == False):
		SuspensionPhases = generate_two_phases(4)
	else:
		SuspensionPhases = generate_two_phases(HBCPMSimuPara.Armature_coil_number)

	# ArmaturePhases = [
	# 	{"name": "Phase_A", "current": "ImA", "group": ["A_1", "A_2", "A_3", "A_4"]},
	# 	{"name": "Phase_B", "current": "ImB", "group": ["B_1", "B_2", "B_3", "B_4"]},
	# 	{"name": "Phase_C", "current": "ImC", "group": ["C_1", "C_2", "C_3", "C_4"]},
	# ]

	# SuspensionPhases [{'name': 'Phase_sa', 'current': 'Is_a', 'group': ['sa_1', 'sa_2']},
	#                   {'name': 'Phase_sb', 'current': 'Is_b', 'group': ['sb_1', 'sb_2']}]
	ArmaturePhasedivisor = len(ArmaturePhases) # 3
	SuspensionPhasedivisor = len(SuspensionPhases) # 2

	# Process each phase
	for phase_index, phase in enumerate(ArmaturePhases):
		winding_group = phase["group"]

		# Assign coils for the current phase
		for index, element in enumerate(ArmatureWindingSectionList):
			if index % ArmaturePhasedivisor == phase_index:
				HBCPM.assign_coil(
					assignment=ArmatureWindingSectionList[index],
					conductors_number="turnm",
					polarity="Nagative",
					name=winding_group[int((index - phase_index) / ArmaturePhasedivisor)],
				)

		# Assign the winding
		HBCPM.assign_winding(
			assignment=None,
			winding_type="Current",
			is_solid=False,
			current=phase["current"],
			parallel_branches=1,
			name=phase["name"],
		)

		# Add winding coils
		HBCPM.add_winding_coils(
			assignment=phase["name"], coils=winding_group
		)

		# Process each phase
	
	for phase_index, phase in enumerate(SuspensionPhases):
		winding_group = phase["group"]
		winding_group_index=0

		# Assign coils for the current phase
		for index, element in enumerate(SuspensionWindingSectionList):
			
			if(HBCPMSimuPara.SuspensionWindingFullSlot == False):
				if index % SuspensionPhasedivisor == phase_index:
					if index in (1, 2):
						HBCPM.assign_coil(
							assignment=SuspensionWindingSectionList[index],
							conductors_number="turns",
							polarity="Positive",
							name=winding_group[winding_group_index],
						)
					else:
						HBCPM.assign_coil(
							assignment=SuspensionWindingSectionList[index],
							conductors_number="turns",
							polarity="Nagative",
							name=winding_group[winding_group_index],
						)
						
					winding_group_index+=1
				
			else: 

				if (((index-HBCPMSimuPara.StatorPoleNumber/2/2*float(phase_index)) % float(HBCPMSimuPara.StatorPoleNumber/2)) < float(HBCPMSimuPara.StatorPoleNumber/2/2)):
					print(index)
					print("enter loop, winding_group_index+1 **************************")


					if index in range(int(HBCPMSimuPara.StatorPoleNumber/2/2), int(HBCPMSimuPara.StatorPoleNumber/2)+3):
						
						HBCPM.assign_coil(
							assignment=SuspensionWindingSectionList[index],
							conductors_number="turns",
							polarity="Positive",
							name=winding_group[winding_group_index],
						)
					else:
						HBCPM.assign_coil(
							assignment=SuspensionWindingSectionList[index],
							conductors_number="turns",
							polarity="Nagative",
							name=winding_group[winding_group_index],
						)

					winding_group_index+=1

		# Assign the winding
		HBCPM.assign_winding(
			assignment=None,
			winding_type="Current",
			is_solid=False,
			current=phase["current"],
			parallel_branches=1,
			name=phase["name"],
		)

		# Add winding coils
		HBCPM.add_winding_coils(
			assignment=phase["name"], coils=winding_group
		)

	################################################################
	# Turn core loss, inductance cal
	HBCPM.set_core_losses(SteelList, core_loss_on_field=True)

	HBCPM.eddy_effects_on(SteelList)

	HBCPM.change_inductance_computation(
		compute_transient_inductance=True, incremental_matrix=False
	)

#################################################################

if(Createsetup==True):
	print("Createsetup")
	# Setup generation

	setup_name = "MySetupAuto"
	setup = HBCPM.create_setup(name=setup_name)
	setup.props["StopTime"] = "5ms"
	setup.props["TimeStep"] = "0.5ms"
	setup.props["SaveFieldsType"] = "None"
	setup.props["OutputPerObjectCoreLoss"] = True
	setup.props["OutputPerObjectSolidLoss"] = True
	setup.props["OutputError"] = True
	setup.update()
	HBCPM.validate_simple()

#################################################################
# generate report

if(Postprocessing==True):
	print("postprocessing")

		
	# postprocessing
	output_vars = {
		
		"Current_A": "InputCurrent(Phase_A)",
		"Current_B": "InputCurrent(Phase_B)",
		"Current_C": "InputCurrent(Phase_C)",
		"Flux_A": "FluxLinkage(Phase_A)",
		"Flux_B": "FluxLinkage(Phase_B)",
		"Flux_C": "FluxLinkage(Phase_C)",
		
		
		"pos": "(Moving1.Position) *NumPolePairs",
		
		"cos0": "cos(pos)",
		"cos1": "cos(pos-2*PI/3)",
		"cos2": "cos(pos-4*PI/3)",
		"sin0": "sin(pos)",
		"sin1": "sin(pos-2*PI/3)",
		"sin2": "sin(pos-4*PI/3)",
		
		"Flux_d": "2/3*(Flux_A*cos0+Flux_B*cos1+Flux_C*cos2)",
		"Flux_q": "-2/3*(Flux_A*sin0+Flux_B*sin1+Flux_C*sin2)",
		
		"I_d": "2/3*(Current_A*cos0 + Current_B*cos1 + Current_C*cos2)",
		"I_q": "-2/3*(Current_A*sin0 + Current_B*sin1 + Current_C*sin2)",
		
		"Irms": "sqrt(I_d^2+I_q^2)/sqrt(2)",
		
		"ArmatureOhmicLoss_DC": "Irms^2*R_phase",
		
		"Lad": "L(Phase_A,Phase_A)*cos0 + L(Phase_A,Phase_B)*cos1 + L(Phase_A,Phase_C)*cos2",
		"Laq": "L(Phase_A,Phase_A)*sin0 + L(Phase_A,Phase_B)*sin1 + L(Phase_A,Phase_C)*sin2",
		"Lbd": "L(Phase_B,Phase_A)*cos0 + L(Phase_B,Phase_B)*cos1 + L(Phase_B,Phase_C)*cos2",
		"Lbq": "L(Phase_B,Phase_A)*sin0 + L(Phase_B,Phase_B)*sin1 + L(Phase_B,Phase_C)*sin2",
		"Lcd": "L(Phase_C,Phase_A)*cos0 + L(Phase_C,Phase_B)*cos1 + L(Phase_C,Phase_C)*cos2",
		"Lcq": "L(Phase_C,Phase_A)*sin0 + L(Phase_C,Phase_B)*sin1 + L(Phase_C,Phase_C)*sin2",
		
		"L_d": "(Lad*cos0 + Lbd*cos1 + Lcd*cos2) * 2/3",
		"L_q": "(Laq*sin0 + Lbq*sin1 + Lcq*sin2) * 2/3",
		
		"OutputPower": "Moving1.Speed*TorqueRotation.Torque",
		
		"Ui_A": "InducedVoltage(Phase_A)",
		"Ui_B": "InducedVoltage(Phase_B)",
		"Ui_C": "InducedVoltage(Phase_C)",
		
		"Ui_d": "2/3*(Ui_A*cos0 + Ui_B*cos1 + Ui_C*cos2)",
		"Ui_q": "-2/3*(Ui_A*sin0 + Ui_B*sin1 + Ui_C*sin2)",
		
		"U_A": "Ui_A+R_Phase*Current_A",
		"U_B": "Ui_B+R_Phase*Current_B",
		"U_C": "Ui_C+R_Phase*Current_C",
		
		"U_d": "2/3*(U_A*cos0 + U_B*cos1 + U_C*cos2)",
		"U_q": "-2/3*(U_A*sin0 + U_B*sin1 + U_C*sin2)",   
	}

	for k, v in output_vars.items():
		HBCPM.create_output_variable(k, v)

	# Single plot
	post_params = {"TorqueRotation.Torque": "TorquePlots",
				"TorqueTilt.Torque": "TorqueTilt",}

	# multiple plot
	post_params_multiplot = {  # reports

		("Force.Force_x","Force.Force_y","Force.Force_z"): "Force",
		("CoreLoss", "SolidLoss", "ArmatureOhmicLoss_DC"): "Losses",
		
		(
			"InputCurrent(Phase_A)",
			"InputCurrent(Phase_B)",
			"InputCurrent(Phase_C)",
		): "PhaseCurrents",
		
		(
			"FluxLinkage(Phase_A)",
			"FluxLinkage(Phase_B)",
			"FluxLinkage(Phase_C)",
		): "PhaseFluxes",
		
		("I_d", "I_q"): "Currents_dq",
		("Flux_d", "Flux_q"): "Fluxes_dq",
		("Ui_d", "Ui_q"): "InducedVoltages_dq",
		("U_d", "U_q"): "Voltages_dq",
		
		(
			"L(Phase_A,Phase_A)",
			"L(Phase_B,Phase_B)",
			"L(Phase_C,Phase_C)",
			"L(Phase_A,Phase_B)",
			"L(Phase_A,Phase_C)",
			"L(Phase_B,Phase_C)",
		): "PhaseInductances",
		
		("L_d", "L_q"): "Inductances_dq",
		
		("CoreLoss", "CoreLoss(Stator)", "CoreLoss(Rotor)"): "CoreLosses",

		(
			"EddyCurrentLoss",
			"EddyCurrentLoss(Stator)",
			"EddyCurrentLoss(Rotor)",
		): "EddyCurrentLosses (Core)",

		(
			"HysteresisLoss",
			"HysteresisLoss(Stator)",
			"HysteresisLoss(Rotor)",
		): "HysteresisLoss (Core)",
		
		("ExcessLoss", "ExcessLoss(Stator)", "ExcessLoss(Rotor)"): "ExcessLosses (Core)",
		
		(
			"HysteresisLoss",
			"HysteresisLoss(Stator)",
			"HysteresisLoss(Rotor)",
		): "HysteresisLosses (Core)",
	}

	# generate single plot report
	for k, v in post_params.items():
		HBCPM.post.create_report(expressions=k, setup_sweep_name="",
							domain="Sweep", variations=None,
							primary_sweep_variable="Time", secondary_sweep_variable=None,
							report_category=None, plot_type="Rectangular Plot",
							context=None, subdesign_id=None,
							polyline_points=1001, plotname=v)

	# generate multi plot report
	for k, v in post_params_multiplot.items():
		HBCPM.post.create_report(expressions=list(k), setup_sweep_name="",
							domain="Sweep", variations=None,
							primary_sweep_variable="Time", secondary_sweep_variable=None,
							report_category=None, plot_type="Rectangular Plot",
							context=None, subdesign_id=None,
							polyline_points=1001, plotname=v)


#################################################################
# Using builtin optimizer or selfdefine optimizer

"""	
if(BuildInOptimization==True):
  # Set Optimization  

	oModule = oDesign.GetModule("Optimetrics")

	oModule.InsertSetup("OptiOptimization", 
		[
			"NAME:OptimizationSetup1",
			"IsEnabled:="		, True,
			[
				"NAME:ProdOptiSetupDataV2",
				"SaveFields:="		, False,
				"CopyMesh:="		, False,
				"SolveWithCopiedMeshOnly:=", False
			],
			"InterpolationPoints:="	, 0,
			[
				"NAME:StartingPoint",
				"RotorCenterThickness:=", "8mm",
				"RotorInnerRadius:="	, "16.6mm",
				"RotorIronOuterdarius:=", "25mm",
				"RotorIronThickness:="	, "1.5mm",
				"RotorOuterRadius:="	, "25mm",
				"RotorPMAxialThickness:=", "2mm",
				"StatorAxialThickness:=", "8mm",
				"StatorInnerRadius:="	, "27mm",
				"StatorIronOuterradius:=", "29mm",
				"StatorIronThickness:="	, "1.5mm",
				"StatorOuterDRadius:="	, "56mm",
				"StatorPMOuterradius:="	, "29.5mm",
				"StatorPMThickness:="	, "2mm",
				"StatorPoleLength:="	, "8.5mm",
				"StatorPoleWidth:="	, "8mm"
			],
			"Optimizer:="		, "DX MOGA",
			[
				"NAME:AnalysisStopOptions",
				"StopForNumIteration:="	, True,
				"StopForElapsTime:="	, False,
				"StopForSlowImprovement:=", False,
				"StopForGrdTolerance:="	, False,
				"MaxNumIteration:="	, 1100,
				"MaxSolTimeInSec:="	, 3600,
				"RelGradientTolerance:=", 0,
				"MinNumIteration:="	, 10
			],
			"CostFuncNormType:="	, "L2",
			"PriorPSetup:="		, "",
			"PreSolvePSetup:="	, True,
			[
				"NAME:Variables",
				"RotorCenterThickness:=", [				"i:="			, False,				"int:="			, False,				"Min:="			, "4mm",				"Max:="			, "12mm",				"MinStep:="		, "0.08mm",				"MaxStep:="		, "0.8mm",				"MinFocus:="		, "4mm",				"MaxFocus:="		, "12mm",				"UseManufacturableValues:=", "false",				"Level:="		, "[4: 12] mm"],
				"RotorInnerRadius:="	, [				"i:="			, False,				"int:="			, False,				"Min:="			, "8mm",				"Max:="			, "24mm",				"MinStep:="		, "0.16mm",				"MaxStep:="		, "1.6mm",				"MinFocus:="		, "8mm",				"MaxFocus:="		, "24mm",				"UseManufacturableValues:=", "false",				"Level:="		, "[8: 24] mm"],
				"RotorIronOuterdarius:=", [				"i:="			, False,				"int:="			, False,				"Min:="			, "12.5mm",				"Max:="			, "37.5mm",				"MinStep:="		, "0.25mm",				"MaxStep:="		, "2.5mm",				"MinFocus:="		, "12.5mm",				"MaxFocus:="		, "37.5mm",				"UseManufacturableValues:=", "false",				"Level:="		, "[12.5: 37.5] mm"],
				"RotorIronThickness:="	, [				"i:="			, False,				"int:="			, False,				"Min:="			, "0.9mm",				"Max:="			, "2.7mm",				"MinStep:="		, "0.018mm",				"MaxStep:="		, "0.18mm",				"MinFocus:="		, "0.9mm",				"MaxFocus:="		, "2.7mm",				"UseManufacturableValues:=", "false",				"Level:="		, "[0.9: 2.7] mm"],
				"RotorOuterRadius:="	, [				"i:="			, False,				"int:="			, False,				"Min:="			, "12.5mm",				"Max:="			, "37.5mm",				"MinStep:="		, "0.25mm",				"MaxStep:="		, "2.5mm",				"MinFocus:="		, "12.5mm",				"MaxFocus:="		, "37.5mm",				"UseManufacturableValues:=", "false",				"Level:="		, "[12.5: 37.5] mm"],
				"RotorPMAxialThickness:=", [				"i:="			, False,				"int:="			, False,				"Min:="			, "1mm",				"Max:="			, "3mm",				"MinStep:="		, "0.02mm",				"MaxStep:="		, "0.2mm",				"MinFocus:="		, "1mm",				"MaxFocus:="		, "3mm",				"UseManufacturableValues:=", "false",				"Level:="		, "[1: 3] mm"],
				"StatorAxialThickness:=", [				"i:="			, False,				"int:="			, False,				"Min:="			, "4mm",				"Max:="			, "12mm",				"MinStep:="		, "0.08mm",				"MaxStep:="		, "0.8mm",				"MinFocus:="		, "4mm",				"MaxFocus:="		, "12mm",				"UseManufacturableValues:=", "false",				"Level:="		, "[4: 12] mm"],
				"StatorInnerRadius:="	, [				"i:="			, False,				"int:="			, False,				"Min:="			, "13.5mm",				"Max:="			, "40.5mm",				"MinStep:="		, "0.27mm",				"MaxStep:="		, "2.7mm",				"MinFocus:="		, "13.5mm",				"MaxFocus:="		, "40.5mm",				"UseManufacturableValues:=", "false",				"Level:="		, "[13.5: 40.5] mm"],
				"StatorIronOuterradius:=", [				"i:="			, False,				"int:="			, False,				"Min:="			, "15mm",				"Max:="			, "45mm",				"MinStep:="		, "0.3mm",				"MaxStep:="		, "3mm",				"MinFocus:="		, "15mm",				"MaxFocus:="		, "45mm",				"UseManufacturableValues:=", "false",				"Level:="		, "[15: 45] mm"],
				"StatorIronThickness:="	, [				"i:="			, False,				"int:="			, False,				"Min:="			, "1mm",				"Max:="			, "3mm",				"MinStep:="		, "0.02mm",				"MaxStep:="		, "0.2mm",				"MinFocus:="		, "1mm",				"MaxFocus:="		, "3mm",				"UseManufacturableValues:=", "false",				"Level:="		, "[1: 3] mm"],
				"StatorOuterDRadius:="	, [				"i:="			, False,				"int:="			, False,				"Min:="			, "27.5mm",				"Max:="			, "82.5mm",				"MinStep:="		, "0.55mm",				"MaxStep:="		, "5.5mm",				"MinFocus:="		, "27.5mm",				"MaxFocus:="		, "82.5mm",				"UseManufacturableValues:=", "false",				"Level:="		, "[27.5: 82.5] mm"],
				"StatorPMOuterradius:="	, [				"i:="			, False,				"int:="			, False,				"Min:="			, "15mm",				"Max:="			, "45mm",				"MinStep:="		, "0.3mm",				"MaxStep:="		, "3mm",				"MinFocus:="		, "15mm",				"MaxFocus:="		, "45mm",				"UseManufacturableValues:=", "false",				"Level:="		, "[15: 45] mm"],
				"StatorPMThickness:="	, [				"i:="			, False,				"int:="			, False,				"Min:="			, "1mm",				"Max:="			, "3mm",				"MinStep:="		, "0.02mm",				"MaxStep:="		, "0.2mm",				"MinFocus:="		, "1mm",				"MaxFocus:="		, "3mm",				"UseManufacturableValues:=", "false",				"Level:="		, "[1: 3] mm"],
				"StatorPoleLength:="	, [				"i:="			, False,				"int:="			, False,				"Min:="			, "5mm",				"Max:="			, "15mm",				"MinStep:="		, "0.1mm",				"MaxStep:="		, "1mm",				"MinFocus:="		, "5mm",				"MaxFocus:="		, "15mm",				"UseManufacturableValues:=", "false",				"Level:="		, "[5: 15] mm"],
				"StatorPoleWidth:="	, [				"i:="			, False,				"int:="			, False,				"Min:="			, "3.75mm",				"Max:="			, "11.25mm",				"MinStep:="		, "0.075mm",				"MaxStep:="		, "0.75mm",				"MinFocus:="		, "3.75mm",				"MaxFocus:="		, "11.25mm",				"UseManufacturableValues:=", "false",				"Level:="		, "[3.75: 11.25] mm"]
			],
			[
				"NAME:LCS"
			],
			[
				"NAME:Goals",
				[
					"NAME:ForceErrorAngle",
					"ReportType:="		, "Transient",
					"Solution:="		, "Setup1 : Transient",
					[
						"NAME:SimValueContext",
						"Domain:="		, "Sweep"
					],
					"Calculation:="		, "max(Force1.Force_x)/avg(Force1.Force_y)",
					"Name:="		, "max(Force1.Force_x)/avg(Force1.Force_y)",
					[
						"NAME:Ranges",
						"Range:="		, [						"Var:="			, "Time",						"Type:="		, "a"]
					],
					"Condition:="		, "<=",
					[
						"NAME:GoalValue",
						"GoalValueType:="	, "Independent",
						"Format:="		, "Real/Imag",
						"bG:="			, [						"v:="			, "[0.2;]"]
					],
					"Weight:="		, "[1;]"
				],
				[
					"NAME:Torque",
					"ReportType:="		, "Transient",
					"Solution:="		, "Setup1 : Transient",
					[
						"NAME:SimValueContext",
						"Domain:="		, "Sweep"
					],
					"Calculation:="		, "Moving1.Torque",
					"Name:="		, "Moving1.Torque",
					[
						"NAME:Ranges",
						"Range:="		, [						"Var:="			, "Time",						"Type:="		, "a"]
					],
					"Condition:="		, ">=",
					[
						"NAME:GoalValue",
						"GoalValueType:="	, "Independent",
						"Format:="		, "Real/Imag",
						"bG:="			, [						"v:="			, "[0.06;]"]
					],
					"Weight:="		, "[1;]"
				],
				# [
				# 	"NAME:TorqueVariance",
				# 	"ReportType:="		, "Transient",
				# 	"Solution:="		, "Setup1 : Transient",
				# 	[
				# 		"NAME:SimValueContext",
				# 		"Domain:="		, "Sweep"
				# 	],
				# 	"Calculation:="		, "variance(Moving1.Torque)",
				# 	"Name:="		, "variance(Moving1.Torque)",
				# 	[
				# 		"NAME:Ranges",
				# 		"Range:="		, [						"Var:="			, "Time",						"Type:="		, "a"]
				# 	],
				# 	"Condition:="		, "Minimize",
				# 	[
				# 		"NAME:GoalValue",
				# 		"GoalValueType:="	, "Independent",
				# 		"Format:="		, "Real/Imag",
				# 		"bG:="			, [						"v:="			, "[0.2;]"]
				# 	],
				# 	"Weight:="		, "[1;]"
				# ]
			],
			"Acceptable_Cost:="	, 0,
			"Noise:="		, 0.0001,
			"UpdateDesign:="	, False,
			"UpdateIteration:="	, 5,
			"KeepReportAxis:="	, True,
			"UpdateDesignWhenDone:=", True,
			[
				"NAME:DXOptimizerOptionData",
				"InitSamples:="		, 100,
				"SamplesPerIteration:="	, 50,
				"MaxAllowParetoPercentage:=", 70,
				"MaxIterations:="	, 20,
				"AllowableConvergence:=", 0.0001,
				"TypeOfDiscreteCrossover:=", "OnePoint",
				"SamplingType:="	, "Screening",
				"MutationProbability:="	, 0.01,
				"CrossoverProbability:=", 0.98
			]
		])
	oModule.SolveSetup("OptimizationSetup1")
else:
	pass
     
"""

desktop.save_project()
desktop.release_desktop()