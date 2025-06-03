import numpy as np
import math
from ansys.aedt.core import Desktop, Maxwell3d, Hfss
import ansys.aedt.core.downloads as downloads
import os,time,json
import pyaedt
from ansys.aedt.core.visualization.plot.pdf import AnsysReport
from utilis.generat_phases_coils import generate_three_phases
from utilis.generat_phases_coils import generate_two_phases
from pathlib import Path

class HBCPMWrapper:

    def __init__(self,default_json_file_name=None):    
        
        self.defaults_para = {

            "Proj_path": "F:/he/HBCPM",  # Path to save the project, you can change it to your own path
    
            "NumPolePairs": 4,
            "StatorPoleNumber": 12,  
               
            "RadialPM": True,
            "RadialPMPoleArcRatio": 0.9,
            "RadialPMThickness": 2,
            "RadialPMPoleArcEmpthRatio": 0.1,

            "RotorInnerRadius": 16.6,
            "RotorCenterThickness": 8,
            "RotorOuterRadius": 25,

            "RotorPMAxialThickness": 3,
            "RotorPMAxialRadialWidth": 3,

            "RotorIronOuterRadius": 25,
            "RotorIronThickness": 1.5,

            "StatorInnerRadius": 27,
            "StatorAxialThickness": 8,
            "StatorOuterRadius": 56,
            "StatorPoleWidthArcRatio": 0.57,
            "StatorYokeWidth": 8,

            "StatorPMRadialWidth": 3,
            "StatorPMThickness": 3,
            "StatorIronThickness": 1.5,

            "StatorPoleToothWidthArcRatio": 1 / 4,
            "StatorPoleTeethAngle": 45,

            "WindingRadialLength": 13.3,
            "SuspensionWindingFullSlot": True,

            "Velocity_rpm": 3000,
            "turnm": 90,
            "turns": 100,
            "Im": 0,
            "R_phase": 0.6,

            "Is_a":0,
            "Is_b":0,

            "BuildMotor":True,
            "CreateMesh":True,
            "AssignBoundryBand":True,
            "CreateExcitation":True,
            "Createsetup":True,
            "Postprocessing":True,
            "BuildInOptimization":False,


        }

        if default_json_file_name is not None:
            self.json_file_name = default_json_file_name[:-5]

            with open(default_json_file_name, "r") as file:
                default_read_params = json.load(file)

            if default_read_params is not None:
                self.defaults_para.update(default_read_params)      

        self.params={}
        self.params.update(self.defaults_para)
        # # Dynamically set attributes
        # for key, value in defaults.items():
        #     setattr(self, key, value)

        self.updata_params()

    def read_params(self,json_file_name):

        self.json_file_name = json_file_name[:-5]

        with open(json_file_name, "r") as file:
            read_params = json.load(file)
        
        if read_params is not None:
            self.params.update(read_params)

        # Save the dictionary to a JSON file
        # with open("para.json", "w") as file:
        #     json.dump(self.params, file, indent=4)

        self.updata_params()

    def updata_params(self):
        self.Proj_path = self.params["Proj_path"]  # Path to save the project, you can change it to your own path

        self.RadialPM = self.params["RadialPM"]
        self.RadialPMNumber = self.params["NumPolePairs"]
        self.StatorPoleNumber = self.params["StatorPoleNumber"]
        self.RadialPMAngle = 360 / 2 / self.params["NumPolePairs"] * self.params["RadialPMPoleArcRatio"]  # Percentage
        self.RadialPMEmptyAngle = 360 / 2 / self.params["NumPolePairs"] * (self.params["RadialPMPoleArcRatio"]+self.params["RadialPMPoleArcEmpthRatio"] ) # Percentage

        self.RotorInnerRadius = self.params["RotorInnerRadius"]
        self.RotorCenterThickness = self.params["RotorCenterThickness"]
        self.RotorOuterRadius = self.params["RotorOuterRadius"]
        self.RadialPMThickness = self.params["RadialPMThickness"]
        self.RotorPMAxialThickness = self.params["RotorPMAxialThickness"]

        self.RotorIronOuterRadius = self.params["RotorIronOuterRadius"]
        self.RotorIronThickness = self.params["RotorIronThickness"]
        self.RotorIronInnerRadius = (
            self.params["RotorIronOuterRadius"] - self.params["RotorPMAxialRadialWidth"] - self.params["RotorPMAxialRadialWidth"] + 1
        )

        self.RotorPMAxialOuterRadius = self.params["RotorOuterRadius"] - self.params["RadialPMThickness"]
        self.RotorPMInnerRadius = self.RotorPMAxialOuterRadius - self.params["RotorPMAxialRadialWidth"]

        self.StatorYokeWidth = self.params["StatorYokeWidth"]
        self.StatorInnerRadius = self.params["StatorInnerRadius"]
        self.StatorAxialThickness = self.params["StatorAxialThickness"]
        self.StatorOuterRadius = self.params["StatorOuterRadius"]

        self.StatorPoleWidth = (
            2 * np.sin(self.params["StatorPoleWidthArcRatio"] * np.pi / self.params["StatorPoleNumber"]) * self.params["StatorInnerRadius"]
        )
        self.StatorPMOuterRadius = self.params["StatorInnerRadius"] + self.params["StatorPMRadialWidth"]

        self.StatorPMThickness = self.params["StatorPMThickness"]
        self.StatorIronThickness = self.params["StatorIronThickness"]
        self.StatorIronOuterRadius = self.params["StatorInnerRadius"] + self.params["StatorPMRadialWidth"] - 1

        self.StatorPoleTeethAdditionLength = self.StatorPoleWidth * self.params["StatorPoleToothWidthArcRatio"]
        self.StatorPoleTeethAngle = self.params["StatorPoleTeethAngle"]
        self.StatorPoleTeethStartX = np.sqrt(
            self.StatorPMOuterRadius**2 - (self.StatorPoleWidth / 2)**2
        )

        self.WindingThickness = self.StatorPoleWidth / 3
        self.SusWindThickness = self.StatorYokeWidth / 4
        self.WindingRadialLength = self.params["WindingRadialLength"]
        self.SusWindLength = (2* np.pi * (self.StatorOuterRadius-self.StatorYokeWidth/2)/self.StatorPoleNumber-self.StatorPoleWidth)*0.72
        self.SuspensionWindingFullSlot = self.params["SuspensionWindingFullSlot"]

        self.Velocity_rpm = self.params["Velocity_rpm"]

        self.turnm = self.params["turnm"]
        self.turns = self.params["turns"]
        self.Im = self.params["Im"]

        self.NumPolePairs = self.params["NumPolePairs"]
        self.R_phase = self.params["R_phase"]

        self.Armature_coil_number=self.StatorPoleNumber

        self.Is_a=self.params["Is_a"]
        self.Is_b=self.params["Is_b"]

        self.BuildMotor=self.params["BuildMotor"]
        self.CreateMesh=self.params["CreateMesh"]
        self.AssignBoundryBand=self.params["AssignBoundryBand"]
        self.CreateExcitation=self.params["CreateExcitation"]
        self.Createsetup=self.params["Createsetup"]
        self.Postprocessing=self.params["Postprocessing"]
        self.BuildInOptimization=self.params["BuildInOptimization"]

        """
        self.RadialPMNumber = NumPolePairs
        self.StatorPoleNumber = StatorPoleNumber
        self.RadialPMAngle = 360/2/NumPolePairs*RadialPMPoleArcRatio # Percentage

        self.RotorInnerRadius = RotorInnerRadius
        self.RotorCenterThickness = RotorCenterThickness
        self.RotorOuterRadius = RotorOuterRadius
        self.RadialPMThickness = RadialPMThickness
        self.RotorPMAxialThickness = RotorPMAxialThickness

        self.RotorIronOuterRadius = RotorIronOuterRadius
        self.RotorIronThickness = RotorIronThickness
        self.RotorIronInnerRadius = RotorIronOuterRadius - RotorPMAxialRadialWidth - RotorPMAxialRadialWidth+1

        self.RotorPMAxialOuterRadius = RotorOuterRadius - RadialPMThickness
        self.RotorPMInnerRadius = self.RotorPMAxialOuterRadius - RotorPMAxialRadialWidth

        self.StatorYokeWidth = StatorYokeWidth
        self.StatorInnerRadius = StatorInnerRadius
        self.StatorAxialThickness = StatorAxialThickness
        self.StatorOuterRadius = StatorOuterRadius

        self.StatorPoleWidth = 2*np.sin(StatorPoleWidthArcRatio*np.pi/StatorPoleNumber) * StatorInnerRadius
        self.StatorPMOuterRadius = StatorInnerRadius + StatorPMRadialWidth
    
        self.StatorPMThickness = StatorPMThickness
        self.StatorIronThickness = StatorIronThickness
        self.StatorIronOuterRadius = StatorInnerRadius + StatorPMRadialWidth - 1

        self.StatorPoleTeethAdditionLength = self.StatorPoleWidth*StatorPoleToothWidthArcRatio
        self.StatorPoleTeethAngle = StatorPoleTeethAngle
        self.StatorPoleTeethStartX = np.sqrt(self.StatorPMOuterRadius**2-(self.StatorPoleWidth/2)**2)

        self.WindingThickness = self.StatorPoleWidth/3
        self.WindingRadialLength = WindingRadialLength
        self.Velocity_rpm = Velocity_rpm

        self.turnm = turnm
        self.turns = turns
        self.Im = Im

        self.NumPolePairs = NumPolePairs
        self.R_phase = R_phase
        """

    def create_project(self,json_file_name=None):
    	# HBCPMInstance=BuildHBCPM(params,filename[:-5])
        # prokect_name is for opening a existing project, str
        # example: C:/he/HBCPM/4p12s_HBCPM_with_radial_PM_four_slotProject_TZ8/Project_TZ8.aedt


            if json_file_name is not None:
                self.read_params(json_file_name)


            print("Parameters saved to Para.json successfully!")
            # Launch AEDT
            AedtVersion = "2024.1"  # Replace with your installed AEDT version
            ProjectFullName = pyaedt.generate_unique_project_name()
            self.ProjectName=os.path.basename(ProjectFullName)
            print(self.ProjectName+"**************************")

            path = Path(self.Proj_path)

            if path.exists():          # or:  if path.is_dir()
                print(f"{path} already exists")
            else:
                path.mkdir(parents=True)
                print(f"Created {path}")

            self.project_path=self.Proj_path+"/"+json_file_name[:-5]+self.ProjectName
            self.project_path = os.path.splitext(self.project_path)[0]  # This removes the file extension
            # example:self.project_path ="C:/he/HBCPM/4p12s_HBCPM_with_radial_PM_four_slotProject_TZ8"


            print(self.params)

            # build the dir
            try:
                os.makedirs(self.project_path, exist_ok=True)  
                # 'exist_ok=True' prevents error if the directory exists
            except Exception as e:
                print(f"An error occurred: {e}")

            # Save the dictionary as a JSON file
            with open(self.project_path+"/"+"Para.json", "w") as json_file:
                json.dump(self.params, json_file, indent=4)

            try:
                os.makedirs(self.project_path+"/"+"torque report", exist_ok=True)  
                    # 'exist_ok=True' prevents error if the directory exists
            except Exception as e:
                print(f"An error occurred when create torque report: {e}")


            try:
                os.makedirs(self.project_path+"/"+"force report", exist_ok=True)  
                    # 'exist_ok=True' prevents error if the directory exists
            except Exception as e:
                print(f"An error occurred when create force report: {e}")

            self.DesignName = "HBCPM"
            self.desktop = Desktop(version=AedtVersion,new_desktop=True, non_graphical=False, close_on_exit=True)
            # print(desktop.odesktop)

            self.HBCPM = Maxwell3d(
                            design=self.DesignName,
                            solution_type="",
                            version=AedtVersion,
                            new_desktop=True, 
                            non_graphical=False, 
                            close_on_exit=True)

            self.HBCPM.solution_type = self.HBCPM.SOLUTIONS.Maxwell3d.Transient

            self.oProject =self.desktop.odesktop.GetActiveProject()
            self.oProject.Rename(self.project_path+"/"+self.ProjectName, True)
            # "C:/he/HBCPM/HBCPMProject.aedt"

            self.oDesign = self.oProject.GetActiveDesign()

            oEditor = self.oDesign.SetActiveEditor("3D Modeler")

            print(self.oDesign)
            print(self.oProject)
            print(oEditor)

            # Define variables and expressions in a dictionary
            if (self.StatorPoleNumber / self.NumPolePairs == 3):
                variables = {
                    "RadialPMNumber":str(self.NumPolePairs),
                    "StatorPoleNumber":str(self.StatorPoleNumber),
                    "RadialPMAngle": str(self.RadialPMAngle)+"deg",
                    "RadialPMEmptyAngle": str(self.RadialPMEmptyAngle)+"deg",
                    
                    "RotorInnerRadius": str(self.RotorInnerRadius)+"mm",
                    "RotorCenterThickness": str(self.RotorCenterThickness)+"mm",
                    "RotorOuterRadius": str(self.RotorOuterRadius)+"mm",
                    "RadialPMThickness": str(self.RadialPMThickness)+"mm",
                    "RotorPMAxialThickness": str(self.RotorPMAxialThickness)+"mm",

                    "RotorIronOuterRadius": str(self.RotorIronOuterRadius)+"mm",
                    "RotorIronThickness": str(self.RotorIronThickness)+"mm",
                    
                    "RotorPMAxialOuterRadius": str(self.RotorPMAxialOuterRadius)+"mm",
                    "RotorPMInnerRadius": str(self.RotorPMInnerRadius)+"mm",

                    "StatorYokeWidth": str(self.StatorYokeWidth)+"mm",
                    "StatorInnerRadius": str(self.StatorInnerRadius)+"mm",
                    "StatorAxialThickness": str(self.StatorAxialThickness)+"mm",
                    "StatorOuterRadius": str(self.StatorOuterRadius)+"mm",

                    "StatorPoleWidth": str(self.StatorPoleWidth)+"mm",
                    "StatorPMOuterRadius": str(self.StatorPMOuterRadius)+"mm",
                    "StatorPMThickness": str(self.StatorPMThickness)+"mm",
                    "StatorIronThickness": str(self.StatorIronThickness)+"mm",
                    "StatorIronOuterRadius": str(self.StatorIronOuterRadius)+"mm",
                    "RotorIronInnerRadius": str(self.RotorIronInnerRadius)+"mm",

                    "StatorPoleTeethAdditionLength": str(self.StatorPoleWidth/4)+"mm",
                    "StatorPoleTeethAngle":  str(self.StatorPoleTeethAngle)+"deg",

                    "StatorPoleTeethStartX": str(self.StatorPoleTeethStartX)+"mm",


                    "SusWindThickness": str(self.SusWindThickness)+"mm",
                    "SusWindingLength": str(self.SusWindLength)+"mm",
                    "WindingThickness": str(self.WindingThickness)+"mm",
                    "WindingRadialLength": str(self.WindingRadialLength)+"mm",
                    "Velocity_rpm": str(self.Velocity_rpm),

                    "turnm": str(self.turnm),
                    "turns": str(self.turns),
                    "Im": str(self.Im)+"A",
                    "Is_a": str(self.Is_a)+"A",
                    "Is_b": str(self.Is_b)+"A",

                    "ImA": "Im*cos(Velocity_rpm/60*2*pi*time*RadialPMNumber+pi/2)",
                    "ImB": "Im*cos(Velocity_rpm/60*2*pi*time*RadialPMNumber+pi/2-2*pi/3)",
                    "ImC": "Im*cos(Velocity_rpm/60*2*pi*time*RadialPMNumber+pi/2+2*pi/3)",

                    "NumPolePairs":str(self.NumPolePairs),

                    "R_phase":str(self.R_phase)+"Ohm",
                }


            if (self.StatorPoleNumber / self.NumPolePairs == 1.5):
                variables = {
                    "RadialPMNumber":str(self.NumPolePairs),
                    "StatorPoleNumber":str(self.StatorPoleNumber),
                    "RadialPMAngle": str(self.RadialPMAngle)+"deg",

                    "RotorInnerRadius": str(self.RotorInnerRadius)+"mm",
                    "RotorCenterThickness": str(self.RotorCenterThickness)+"mm",
                    "RotorOuterRadius": str(self.RotorOuterRadius)+"mm",
                    "RadialPMThickness": str(self.RadialPMThickness)+"mm",
                    "RotorPMAxialThickness": str(self.RotorPMAxialThickness)+"mm",

                    "RotorIronOuterRadius": str(self.RotorIronOuterRadius)+"mm",
                    "RotorIronThickness": str(self.RotorIronThickness)+"mm",
                    
                    "RotorPMAxialOuterRadius": str(self.RotorPMAxialOuterRadius)+"mm",
                    "RotorPMInnerRadius": str(self.RotorPMInnerRadius)+"mm",

                    "StatorYokeWidth": str(self.StatorYokeWidth)+"mm",
                    "StatorInnerRadius": str(self.StatorInnerRadius)+"mm",
                    "StatorAxialThickness": str(self.StatorAxialThickness)+"mm",
                    "StatorOuterRadius": str(self.StatorOuterRadius)+"mm",

                    "StatorPoleWidth": str(self.StatorPoleWidth)+"mm",
                    "StatorPMOuterRadius": str(self.StatorPMOuterRadius)+"mm",
                    "StatorPMThickness": str(self.StatorPMThickness)+"mm",
                    "StatorIronThickness": str(self.StatorIronThickness)+"mm",
                    "StatorIronOuterRadius": str(self.StatorIronOuterRadius)+"mm",
                    "RotorIronInnerRadius": str(self.RotorIronInnerRadius)+"mm",

                    "StatorPoleTeethAdditionLength": str(self.StatorPoleWidth/4)+"mm",
                    "StatorPoleTeethAngle":  str(self.StatorPoleTeethAngle)+"deg",

                    "StatorPoleTeethStartX": str(self.StatorPoleTeethStartX)+"mm",


                    "SusWindThickness": str(self.SusWindThickness)+"mm",
                    "SusWindingLength": str(self.SusWindLength)+"mm",
                    "WindingThickness": str(self.WindingThickness)+"mm",
                    "WindingRadialLength": str(self.WindingRadialLength)+"mm",
                    "Velocity_rpm": str(self.Velocity_rpm),

                    "turnm": str(self.turnm),
                    "turns": str(self.turns),
                    "Im": str(self.Im)+"A",
                    "Is_a": str(self.Is_a)+"A",
                    "Is_b": str(self.Is_b)+"A",

                    "ImA": "Im*cos(Velocity_rpm/60*2*pi*time*RadialPMNumber+pi/2)",
                    "ImB": "Im*cos(Velocity_rpm/60*2*pi*time*RadialPMNumber+pi/2+2*pi/3)",
                    "ImC": "Im*cos(Velocity_rpm/60*2*pi*time*RadialPMNumber+pi/2-2*pi/3)",

                    "NumPolePairs":str(self.NumPolePairs),

                    "R_phase":str(self.R_phase)+"Ohm",

                }

            # # Save the dictionary as a JSON file
            # with open("Para.json", "w") as json_file:
            #     json.dump(variables, json_file, indent=4)

            # print("Parameters saved to Para.json successfully!")

            # This call returns the VariableManager class
            # Iterate through the dictionary and set each variable
            for var_name, expression in variables.items():
                self.HBCPM.variable_manager.set_variable(var_name, expression=expression)

            # Define new materials
            # Load from JSON file
            with open('JFE_Steel_35JNE300_lamination_data.json', 'r') as f:
                JFE_Steel_35JNE300_lamination_data = json.load(f)


            oDefinitionManager = self.oProject.GetDefinitionManager()

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
                        "DirComp1:="		, "-1",
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

    def build_motor(self):
        # Create 3D model
        # define the object in Create, Duplicate function
        # the object is actually the name or namelist of the each instance

        # Rotor main body
        ###################################################################################
        self.all_objectsList=[]

        if (self.BuildMotor):
            print("BuildMotor")

            oEditor = self.oDesign.SetActiveEditor("3D Modeler")

            self.Rotor = oEditor.CreateRectangle(
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
                    "Color:="		, "(128 128 128)",
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
                    "Selections:="		, self.Rotor,
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
            if (self.RadialPM == True):
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

            RotorRadialPMEmpty = oEditor.CreateRectangle(
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
                    "Selections:="		, RotorRadialPMEmpty,
                    "NewPartsModelFlag:="	, "Model"
                ], 
                [
                    "NAME:AxisSweepParameters",
                    "DraftAngle:="		, "0deg",
                    "DraftType:="		, "Round",
                    "CheckFaceFaceIntersection:=", False,
                    "ClearAllIDs:="		, False,
                    "SweepAxis:="		, "Y",
                    "SweepAngle:="		, "RadialPMEmptyAngle/2",
                    "NumOfSegments:="	, "0"
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


            RotorRadialPMEmptyhalf = oEditor.DuplicateMirror(
                [
                    "NAME:Selections",
                    "Selections:="		, RotorRadialPMEmpty,
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

            self.RotorRadialPMEmptyhalfList=[RotorRadialPMEmpty]
            self.RotorRadialPMEmptyhalfList.extend(RotorRadialPMEmptyhalf)

            self.RotorRadialPMhalfList=[RotorRadialPM]
            self.RotorRadialPMhalfList.extend(RotorRadialPMhalf)

            oEditor.Unite(
                [
                    "NAME:Selections",
                    "Selections:="		, ",".join(map(str, self.RotorRadialPMhalfList))
                ], 
                [
                    "NAME:UniteParameters",
                    "KeepOriginals:="	, False,
                    "TurnOnNBodyBoolean:="	, True
                ])

            oEditor.Unite(
                [
                    "NAME:Selections",
                    "Selections:="		, ",".join(map(str, self.RotorRadialPMEmptyhalfList))
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

            RotorRadialPMEMptyDupt = oEditor.DuplicateAroundAxis(
                [
                    "NAME:Selections",
                    "Selections:="		, RotorRadialPMEmpty,
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
            self.RotorRadialPMList=[RotorRadialPM]
            self.RotorRadialPMList.extend(RotorRadialPMDupt)
            # print(RotorRadialPMList)

            self.RotorRadialPMEmptyList=[RotorRadialPMEmpty]
            self.RotorRadialPMEmptyList.extend(RotorRadialPMEMptyDupt)

            # oEditor.Subtract(
            #     [
            #         "NAME:Selections",
            #         "Blank Parts:="		, "Rotor",
            #         "Tool Parts:="		, ",".join(map(str, self.RotorRadialPMList))
            #     ], 
            #     [
            #         "NAME:SubtractParameters",
            #         "KeepOriginals:="	, True,
            #         "TurnOnNBodyBoolean:="	, True
            #     ])

            oEditor.Subtract(
                [
                    "NAME:Selections",
                    "Blank Parts:="		, "Rotor",
                    "Tool Parts:="		, ",".join(map(str, self.RotorRadialPMEmptyList))
                ], 
                [
                    "NAME:SubtractParameters",
                    "KeepOriginals:="	, False,
                    "TurnOnNBodyBoolean:="	, True
                ])

            print("Create "+ self.Rotor + " successful")

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
                    "Color:="		, "(255 0 0)",
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

            self.RotorAxialPMList=[RotorAxialPM]

            self.RotorAxialPMList.extend(RotorAxialPMDupt)
            # print(RotorAxialPMList)

            oEditor.ChangeProperty(
                [
                    "NAME:AllTabs",
                    [
                        "NAME:Geometry3DAttributeTab",
                        [
                            "NAME:PropServers", 
                            self.RotorAxialPMList[1], 
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
 
            print("Create "+ str(self.RotorAxialPMList) + " successful")

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
                    "Color:="		, "(207 207 207)",
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

            self.RotorAxialIronList=[RotorAxialIron]
            self.RotorAxialIronList.extend(RotorAxialIronDupt)

            self.RotorList = [self.Rotor] + self.RotorRadialPMList + self.RotorAxialPMList + self.RotorAxialIronList

            print("Create " + str(self.RotorAxialIronList) + " successful")

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
                    "Color:="		, "(255 0 0)",
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

            self.StatorAxialPMList=[StatorAxialPM]

            self.StatorAxialPMList.extend(StatorAxialPMDupt)
            # print(RotorAxialPMList)

            oEditor.ChangeProperty(
                [
                    "NAME:AllTabs",
                    [
                        "NAME:Geometry3DAttributeTab",
                        [
                            "NAME:PropServers", 
                            self.StatorAxialPMList[1], 
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

            print("Create "+ str(self.StatorAxialPMList) + " successful")


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
                    "Color:="		, "(207 207 207)",
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

            self.StatorAxialIronList=[StatorAxialIron]
            self.StatorAxialIronList.extend(StatorAxialIronDupt)

            print("Create " + str(StatorAxialIron) + " successful")


            # Create stator Pole and Yoke

            # Stator Yoke
            self.Stator = oEditor.CreateRectangle(
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
                    "Color:="		, "(128 128 128)",
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
                    "Selections:="		, self.Stator,
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

            print("Create " + str(self.Stator) + " successful")

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

            self.StatorPoleList=[StatorPole]

            self.StatorPoleList.extend(StatorPolehalfDupt)

            oEditor.Unite(
                [
                    "NAME:Selections",
                    "Selections:="		, ",".join(map(str, self.StatorPoleList))
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
                    "Color:="		, "(128 128 128)",
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

            self.StatorPoleIntersectorList=[StatorPole,StatorPoleIntersector]
            # print(StatorPoleIntersectorList)

            oEditor.Intersect(
                [
                    "NAME:Selections",
                    "Selections:="		, ",".join(map(str, self.StatorPoleIntersectorList))
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
                    "Color:="		, "(128 128 128)",
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
                    "Color:="		, "(128 128 128)",
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
                    "Color:="		, "(128 128 128)",
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

            self.StatorToothList=[StatorTooth,StatorToothIntersector1,StatorToothIntersector2]

            oEditor.Intersect(
                [
                    "NAME:Selections",
                    "Selections:="		, ",".join(map(str, self.StatorToothList))
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

            self.StatorToothUnionList = [StatorPole,StatorTooth]
            self.StatorToothUnionList.extend(StatorToothDul)

            print(self.StatorToothUnionList)

            oEditor.Unite(
                [
                    "NAME:Selections",
                    "Selections:="		, ",".join(map(str, self.StatorToothUnionList))
                ], 
                [
                    "NAME:UniteParameters",
                    "KeepOriginals:="	, False,
                    "TurnOnNBodyBoolean:="	, True
                ])

            StatorToothUnion = oEditor.DuplicateAroundAxis(
                [
                    "NAME:Selections",
                    "Selections:="		, self.StatorToothUnionList[0],
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

            self.StatorList=[self.Stator,self.StatorToothUnionList[0]]
            self.StatorList.extend(StatorToothUnion)

            oEditor.Unite(
                [
                    "NAME:Selections",
                    "Selections:="		, ",".join(map(str, self.StatorList))
                ], 
                [
                    "NAME:UniteParameters",
                    "KeepOriginals:="	, False,
                    "TurnOnNBodyBoolean:="	, True
                ])

            self.StatorAllList = [self.Stator] + self.StatorAxialPMList + self.StatorAxialIronList
            print("Create " + str(self.StatorList) + " successful")


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
                    "Color:="		, "(255 128 0)",
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

            self.ArmatureWindingList=[ArmatureWinding]
            self.ArmatureWindingList.extend(ArmatureWindingDup)

            print("Create " + str(self.ArmatureWindingList) + " successful")

            self.ArmatureWindingSectionList= oEditor.Section(
                [
                    "NAME:Selections",
                    "Selections:="		, ",".join(map(str, self.ArmatureWindingList)),
                    "NewPartsModelFlag:="	, "Model"
                ], 
                [
                    "NAME:SectionToParameters",
                    "CreateNewObjects:="	, True,
                    "SectionPlane:="	, "ZX",
                    "SectionCrossObject:="	, False
                ])

            # print(ArmatureWindingSectionList)

            self.ArmatureWindingSectionSeparateList = oEditor.SeparateBody(
                [
                    "NAME:Selections",
                    "Selections:="		, ",".join(map(str, self.ArmatureWindingSectionList)),
                    "NewPartsModelFlag:="	, "Model"
                ], 
                [
                    "CreateGroupsForNewObjects:=", False
                ])

            # Create a new list with strings ending with "Separate1"
            self.ArmatureWindingSectionDeleteList = [s for s in self.ArmatureWindingSectionSeparateList if s.endswith("Separate1")]

            # print(ArmatureWindingSectionDeleteList)

            oEditor.Delete(
                [
                    "NAME:Selections",
                    "Selections:="		, ",".join(map(str, self.ArmatureWindingSectionDeleteList))
                ])

            ##################################################################
            #Create Suspension Windings
            self.SuspensionWindingsubtractor = oEditor.CreateRectangle(
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
                    "Color:="		, "(255 128 0)",
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
                    "Color:="		, "(255 128 0)",
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
                    "Tool Parts:="		, self.SuspensionWindingsubtractor
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

            if(self.SuspensionWindingFullSlot == False):
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

            self.SuspensionWindingList=[SuspensionWinding]
            self.SuspensionWindingList.extend(SuspensionWindingDup)

            print("Create " + str(self.SuspensionWindingList) + " successful")

            self.SuspensionWindingSectionList= oEditor.Section(
                [
                    "NAME:Selections",
                    "Selections:="		, ",".join(map(str, self.SuspensionWindingList)),
                    "NewPartsModelFlag:="	, "Model"
                ], 
                [
                    "NAME:SectionToParameters",
                    "CreateNewObjects:="	, True,
                    "SectionPlane:="	, "ZX",
                    "SectionCrossObject:="	, False
                ])
            
            # print(ArmatureWindingSectionList)

            self.SuspensionWindingSectionSeparateList = oEditor.SeparateBody(
                [
                    "NAME:Selections",
                    "Selections:="		, ",".join(map(str, self.SuspensionWindingSectionList)),
                    "NewPartsModelFlag:="	, "Model"
                ], 
                [
                    "CreateGroupsForNewObjects:=", False
                ])

            # Create a new list with strings ending with "Separate1"
            self.SuspensionWindingSectionDeleteList = [s for s in self.SuspensionWindingSectionSeparateList if s.endswith("Separate1")]

            # print(ArmatureWindingSectionDeleteList)

            oEditor.Delete(
                [
                    "NAME:Selections",
                    "Selections:="		, ",".join(map(str, self.SuspensionWindingSectionDeleteList))
                ])

            ################################################################
            # air boundry, band, air gap segment

            self.Air = oEditor.CreateCylinder(
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

            self.Band = oEditor.CreateCylinder(
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
                    "Radius:="		, "4*StatorInnerRadius/8+4*RotorOuterRadius/8+0.1mm",
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
                    "Radius:="		, "8*StatorInnerRadius/8+0*RotorOuterRadius/8 - 0.1 mm",
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

            self.AirgapSubtractorList=[Airgap1,Airgap2,Airgap3,Airgap4,Airgap5]

            oEditor.Subtract(
                [
                    "NAME:Selections",
                    "Blank Parts:="		, self.AirgapSubtractorList[4],
                    "Tool Parts:="		, self.AirgapSubtractorList[3]
                ], 
                [
                    "NAME:SubtractParameters",
                    "KeepOriginals:="	, True,
                    "TurnOnNBodyBoolean:="	, True
                ])

            oEditor.Subtract(
                [
                    "NAME:Selections",
                    "Blank Parts:="		, self.AirgapSubtractorList[3],
                    "Tool Parts:="		, self.AirgapSubtractorList[2]
                ], 
                [
                    "NAME:SubtractParameters",
                    "KeepOriginals:="	, True,
                    "TurnOnNBodyBoolean:="	, True
                ])

            oEditor.Subtract(
                [
                    "NAME:Selections",
                    "Blank Parts:="		, self.AirgapSubtractorList[1],
                    "Tool Parts:="		, self.AirgapSubtractorList[0]
                ], 
                [
                    "NAME:SubtractParameters",
                    "KeepOriginals:="	, True,
                    "TurnOnNBodyBoolean:="	, True
                ])

            self.AirgapList=[self.AirgapSubtractorList[4],self.AirgapSubtractorList[3],self.AirgapSubtractorList[1]]

            self.AirgapDeleteList=[self.AirgapSubtractorList[2],self.AirgapSubtractorList[0]]

            oEditor.Delete(
                [
                    "NAME:Selections",
                    "Selections:="		, ",".join(map(str, self.AirgapDeleteList))
                ])

            print("Create " + str(self.AirgapList) + " successful")


            # Create lines for field analysis
            oEditor = self.oDesign.SetActiveEditor("3D Modeler")
            self.AirgapCircleSweep=oEditor.CreatePolyline(
                [
                    "NAME:PolylineParameters",
                    "IsPolylineCovered:="	, True,
                    "IsPolylineClosed:="	, False,
                    [
                        "NAME:PolylinePoints",
                        [
                            "NAME:PLPoint",
                            "X:="			, "26mm",
                            "Y:="			, "0mm",
                            "Z:="			, "0mm"
                        ],
                        [
                            "NAME:PLPoint",
                            "X:="			, "1.59204083889156e-15mm",
                            "Y:="			, "26mm",
                            "Z:="			, "0mm"
                        ],
                        [
                            "NAME:PLPoint",
                            "X:="			, "-26mm",
                            "Y:="			, "3.18408167778312e-15mm",
                            "Z:="			, "0mm"
                        ]
                    ],
                    [
                        "NAME:PolylineSegments",
                        [
                            "NAME:PLSegment",
                            "SegmentType:="		, "AngularArc",
                            "StartIndex:="		, 0,
                            "NoOfPoints:="		, 3,
                            "NoOfSegments:="	, "0",
                            "ArcAngle:="		, "180deg",
                            "ArcCenterX:="		, "0mm",
                            "ArcCenterY:="		, "0mm",
                            "ArcCenterZ:="		, "0mm",
                            "ArcPlane:="		, "XY"
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
                    "Name:="		, "AirgapCircleSweep",
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
            
            oEditor.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:Geometry3DPolylineTab",
                    [
                        "NAME:PropServers", 
                        "AirgapCircleSweep:CreatePolyline:1:Segment0"
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:Start Point",
                            "X:="			, "StatorInnerRadius/2+RotorOuterRadius/2",
                            "Y:="			, "0mm",
                            "Z:="			, "0mm"
                        ],
                        [
                            "NAME:Plane",
                            "Value:="		, "ZX"
                        ],
                        [
                        "NAME:Angle",
                        "Value:="		, "-359.9deg"
                        ]
                    ]
                ]
            ])

            AirgapAxialSweep = oEditor.CreatePolyline(
                [
                    "NAME:PolylineParameters",
                    "IsPolylineCovered:="	, True,
                    "IsPolylineClosed:="	, False,
                    [
                        "NAME:PolylinePoints",
                        [
                            "NAME:PLPoint",
                            "X:="			, "StatorInnerRadius/2+RotorOuterRadius/2",
                            "Y:="			, "-12mm",
                            "Z:="			, "0mm"
                        ],
                        [
                            "NAME:PLPoint",
                            "X:="			, "StatorInnerRadius/2+RotorOuterRadius/2",
                            "Y:="			, "12mm",
                            "Z:="			, "0mm"
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
                    "Name:="		, "AirgapAxialSweep",
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

            AirgapAxialSweepDup = oEditor.DuplicateAroundAxis(
        [
            "NAME:Selections",
            "Selections:="		, AirgapAxialSweep,
            "NewPartsModelFlag:="	, "Model"
        ], 
        [
            "NAME:DuplicateAroundAxisParameters",
            "CreateNewObjects:="	, True,
            "WhichAxis:="		, "Y",
            "AngleStr:="		, "(180/NumPolePairs)deg",
            "NumClones:="		, "NumPolePairs*2"
        ], 
        [
            "NAME:Options",
            "DuplicateAssignments:=", True
        ], 
        [
            "CreateGroupsForNewObjects:=", False
        ])

            self.AirgapAxialSweepList=[AirgapAxialSweep]
            self.AirgapAxialSweepList.extend(AirgapAxialSweepDup)

            self.all_objectsList = self.RotorList + self.StatorAllList+ self.ArmatureWindingList+ self.SuspensionWindingList+ self.AirgapList + self.ArmatureWindingSectionList+ self.SuspensionWindingSectionList+ self.AirgapAxialSweepList +[self.Band, self.Air,self.AirgapCircleSweep]

            oEditor.Rotate(
                [
                    "NAME:Selections",
                    "Selections:="		, ",".join(map(str, self.all_objectsList)),
                    "NewPartsModelFlag:="	, "Model"
                ], 
                [
                    "NAME:RotateParameters",
                    "RotateAxis:="		, "X",
                    "RotateAngle:="		, "90deg"
                ])


            self.HBCPM.save_project()

    def mesh(self):
        ##################################################### 
        # Mesh Operation

        if (self.CreateMesh):
            print("CreateMesh")

            oModule = self.oDesign.GetModule("MeshSetup")

            oModule.InitialMeshSettings(
                [
                    "NAME:MeshSettings",
                    [
                        "NAME:GlobalSurfApproximation",
                        "CurvedSurfaceApproxChoice:=", "UseSlider",
                        "SliderMeshSettings:="	, 7
                    ],
                    [
                        "NAME:GlobalCurvilinear",
                        "Apply:="		, True
                    ],
                    [
                        "NAME:GlobalModelRes",
                        "UseAutoLength:="	, True
                    ],
                    "MeshMethod:="		, "AnsoftTAU",
                    "UseLegacyFaceterForTauVolumeMesh:=", False,
                    "DynamicSurfaceResolution:=", False,
                    "UseFlexMeshingForTAUvolumeMesh:=", False,
                    "UseAlternativeMeshMethodsAsFallBack:=", True,
                    "AllowPhiForLayeredGeometry:=", False
                ])

            self.TotalPMList = self.RotorRadialPMList+self.RotorAxialPMList+self.StatorAxialPMList
            self.TotalIronList = self.RotorAxialIronList+self.StatorAxialIronList

            self.SteelList=[self.Rotor]
            self.SteelList.append(self.Stator)

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
                    "RefineInside:="	, False,
                    "Enabled:="		, True,
                    "Objects:="		, self.AirgapList,
                    "RestrictElem:="	, False,
                    "NumMaxElem:="		, "1000",
                    "RestrictLength:="	, True,
                    "MaxLength:="		, "1mm"
                ])

            oModule.AssignLengthOp(
                [
                    "NAME:Winding",
                    "RefineInside:="	, True,
                    "Enabled:="		, True,
                    "Objects:="		, self.ArmatureWindingList,
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
                    "Objects:="		, self.TotalPMList,
                    "RestrictElem:="	, False,
                    "NumMaxElem:="		, "1000",
                    "RestrictLength:="	, True,
                    "MaxLength:="		, "1.2mm"
                ])

            oModule.AssignLengthOp(
                [
                    "NAME:Iron",
                    "RefineInside:="	, True,
                    "Enabled:="		, True,
                    "Objects:="		, self.TotalIronList,
                    "RestrictElem:="	, False,
                    "NumMaxElem:="		, "1000",
                    "RestrictLength:="	, True,
                    "MaxLength:="		, "1.5mm"
                ])

            oModule.AssignLengthOp(
                [
                    "NAME:Steel",
                    "RefineInside:="	, True,
                    "Enabled:="		, True,
                    "Objects:="		, self.SteelList,
                    "RestrictElem:="	, False,
                    "NumMaxElem:="		, "1000",
                    "RestrictLength:="	, True,
                    "MaxLength:="		, "3mm"
                ])

    def create_relative_coordinate_system(self):
        #############################################################
        # Create relative coordinate system

        oEditor = self.oDesign.SetActiveEditor("3D Modeler")
        oEditor.CreateRelativeCS(
            [
                "NAME:RelativeCSParameters",
                "Mode:="		, "Axis/Position",
                "OriginX:="		, "0mm",
                "OriginY:="		, "0mm",
                "OriginZ:="		, "0mm",
                "XAxisXvec:="		, "0mm",
                "XAxisYvec:="		, "0mm",
                "XAxisZvec:="		, "1mm",
                "YAxisXvec:="		, "1mm",
                "YAxisYvec:="		, "0mm",
                "YAxisZvec:="		, "0mm"
            ], 
            [
                "NAME:Attributes",
                "Name:="		, "RelativeCoordSyst"
            ])
        
        print("Create " + str("RelativeCoordSyst") + " successful")
        self.HBCPM.save_project()

    def assign_boudry_band(self):
        #############################################################
        # assign boudry and band

        if (self.AssignBoundryBand):  
            print("AssignBoundryBand")
                
            # Setup boundry and band
            self.AirSurfaceList = self.HBCPM.modeler.get_object_faces(assignment=self.Air)

            print(self.AirSurfaceList)

            oModule = self.oDesign.GetModule("BoundarySetup")

            oModule.AssignZeroTangentialHField(
                [
                    "NAME:ZeroTangentialHField",
                    "Faces:="		, self.AirSurfaceList
                ])

            self.HBCPM.assign_rotate_motion(
                assignment=self.Band,
                coordinate_system = "Global",
                axis="Z",
                positive_movement=True,
                start_position="0deg",
                angular_velocity=str(self.Velocity_rpm)+" rpm",
            )

            self.HBCPM.save_project()

    def assign_force_torque(self):
            ###################################################################
            # Set force and torque

            oModule = self.oDesign.GetModule("MaxwellParameterSetup")

            # self.RotorList=self.RotorAxialIronList+self.RotorRadialPMList+self.RotorAxialPMList
            # self.RotorList.append(self.Rotor)

            oModule.AssignForce(
                [
                    "NAME:Force",
                    "Reference CS:="	, "Global",
                    "Is Virtual:="		, True,
                    "Objects:="		, self.RotorList
                ])
            oModule.AssignTorque(
                [
                    "NAME:TorqueRotation",
                    "Is Virtual:="		, True,
                    "Coordinate System:="	, "Global",
                    "Axis:="		, "Z",
                    "Is Positive:="		, True,
                    "Objects:="		, self.RotorList
                ])
            oModule.AssignTorque(
                [
                    "NAME:TorqueTilt",
                    "Is Virtual:="		, True,
                    "Coordinate System:="	, "Global",
                    "Axis:="		, "X",
                    "Is Positive:="		, True,
                    "Objects:="		, self.RotorList
                ])

    def create_excitation(self):
        ###################################################################
        # Create excitation

        if (self.CreateExcitation):
            print("CreateExcitation")

            # Winding configuration
            oModule =self.oDesign.GetModule("BoundarySetup")

            # print(ArmatureWindingSectionList)

            # Define the phase configurations
            self.ArmaturePhases = generate_three_phases(self.Armature_coil_number)

            # ArmaturePhases = [
            # 	{"name": "Phase_A", "current": "ImA", "group": ["A_1", "A_2", "A_3", "A_4"]},
            # 	{"name": "Phase_B", "current": "ImB", "group": ["B_1", "B_2", "B_3", "B_4"]},
            # 	{"name": "Phase_C", "current": "ImC", "group": ["C_1", "C_2", "C_3", "C_4"]},
            # ]
            self.ArmaturePhasedivisor = len(self.ArmaturePhases) # 3

            # Process each phase
            for phase_index, phase in enumerate(self.ArmaturePhases):
                winding_group = phase["group"]

                # Assign coils for the current phase
                for index, element in enumerate(self.ArmatureWindingSectionList):
                    if index % self.ArmaturePhasedivisor == phase_index:
                        self.HBCPM.assign_coil(
                            assignment=self.ArmatureWindingSectionList[index],
                            conductors_number="turnm",
                            polarity="Nagative",
                            name=winding_group[int((index - phase_index) / self.ArmaturePhasedivisor)],
                        )

                # Assign the winding
                self.HBCPM.assign_winding(
                    assignment=None,
                    winding_type="Current",
                    is_solid=False,
                    current=phase["current"],
                    parallel_branches=1,
                    name=phase["name"],
                )

                # Add winding coils
                self.HBCPM.add_winding_coils(
                    assignment=phase["name"], coils=winding_group
                )

            if(self.SuspensionWindingFullSlot == False):
                self.SuspensionPhases = generate_two_phases(4)
            else:
                self.SuspensionPhases = generate_two_phases(self.Armature_coil_number)

            # SuspensionPhases [{'name': 'Phase_sa', 'current': 'Is_a', 'group': ['sa_1', 'sa_2']},
            #                   {'name': 'Phase_sb', 'current': 'Is_b', 'group': ['sb_1', 'sb_2']}]
            self.SuspensionPhasedivisor = len(self.SuspensionPhases) # 2

            for phase_index, phase in enumerate(self.SuspensionPhases):
                winding_group = phase["group"]
                winding_group_index=0

                # Assign coils for the current phase
                for index, element in enumerate(self.SuspensionWindingSectionList):
                    
                    if(self.SuspensionWindingFullSlot == False):

                        if (index+1) % self.SuspensionPhasedivisor == phase_index:
                            if index in (0, 1):
                                print(self.SuspensionWindingSectionList[index]+" Positive", winding_group[winding_group_index])
                                self.HBCPM.assign_coil(
                                    assignment=self.SuspensionWindingSectionList[index],
                                    conductors_number="turns",
                                    polarity="Nagative",
                                    name=winding_group[winding_group_index],
                                )
                            else:
                                print(self.SuspensionWindingSectionList[index]+" Nagative", winding_group[winding_group_index])
                                self.HBCPM.assign_coil(
                                    assignment=self.SuspensionWindingSectionList[index],
                                    conductors_number="turns",
                                    polarity="Positive",
                                    name=winding_group[winding_group_index],
                                )
                            winding_group_index+=1
                    else: 
            # SuspensionPhases [{'name': 'Phase_sa', 'current': 'Is_a', 'group': ['sa_1', 'sa_2',...'sa_6']},
            #                   {'name': 'Phase_sb', 'current': 'Is_b', 'group': ['sb_1', 'sb_2',...'sb_6']}]
                        if ((((index+3)-self.StatorPoleNumber/2/2*float(phase_index)) % float(self.StatorPoleNumber/2)) < float(self.StatorPoleNumber/2/2)):
                            print(index)
                            print("enter loop, winding_group_index+1 **************************")


                            if index in range(0, int(self.StatorPoleNumber/2)):
                                
                                self.HBCPM.assign_coil(
                                    assignment=self.SuspensionWindingSectionList[index],
                                    conductors_number="turns",
                                    polarity="Nagative",
                                    name=winding_group[winding_group_index],
                                )

                            else:
                                self.HBCPM.assign_coil(
                                    assignment=self.SuspensionWindingSectionList[index],
                                    conductors_number="turns",
                                    polarity="Positive",
                                    name=winding_group[winding_group_index],
                                )

                            winding_group_index+=1

                # Assign the winding
                self.HBCPM.assign_winding(
                    assignment=None,
                    winding_type="Current",
                    is_solid=False,
                    current=phase["current"],
                    parallel_branches=1,
                    name=phase["name"],
                )

                # Add winding coils
                self.HBCPM.add_winding_coils(
                    assignment=phase["name"], coils=winding_group
                )

            ################################################################
            # Turn core loss, inductance cal
            self.HBCPM.set_core_losses(self.SteelList)

            # HBCPM.eddy_effects_on(RotorRadialPMList+RotorAxialPMList+StatorAxialPMList)

            self.HBCPM.change_inductance_computation(
                compute_transient_inductance=True, incremental_matrix=False
            )

    def create_setup(self):
        #################################################################

        if(self.Createsetup):
            print("Createsetup")
            # Setup generation

            # setup_name = setup_name
            # setup = HBCPM.create_setup(name=setup_name)
            # setup.props["StopTime"] = str(60/self.Velocity_rpm/self.NumPolePairs/2)+"s"
            # setup.props["TimeStep"] = str(60/self.Velocity_rpm/self.NumPolePairs/2/10)+"s"
            # setup.props["SaveFieldsType"] = "None"
            # setup.props["OutputPerObjectCoreLoss"] = True
            # setup.props["OutputPerObjectSolidLoss"] = True
            # setup.props["OutputError"] = True
            # setup.update()

            self.setup_name="MySetupAuto"
            oModule = self.oDesign.GetModule("AnalysisSetup")
            oModule.InsertSetup("Transient", 
                [
                    "NAME:"+self.setup_name,
                    "Enabled:="		, True,
                    [
                        "NAME:MeshLink",
                        "ImportMesh:="		, False
                    ],
                    "NonlinearSolverResidual:=", "0.01",
                    "ScalarPotential:="	, "First Order",
                    "SmoothBHCurve:="	, False,
                    "StopTime:="		, str(60/self.Velocity_rpm/self.NumPolePairs/2)+"s",
                    "TimeStep:="		, str(60/self.Velocity_rpm/self.NumPolePairs/2/10)+"s",
                    "OutputError:="		, False,
                    "OutputPerObjectCoreLoss:=", True,
                    "OutputPerObjectSolidLoss:=", True,
                    "UseControlProgram:="	, False,
                    "ControlProgramName:="	, " ",
                    "ControlProgramArg:="	, " ",
                    "CallCtrlProgAfterLastStep:=", False,
                    "FastReachSteadyState:=", False,
                    "AutoDetectSteadyState:=", False,
                    "IsGeneralTransient:="	, True,
                    "IsHalfPeriodicTransient:=", False,
                    "SaveFieldsType:="	, "Every N Steps",
                    "N Steps:="		, "1",
                    "Steps From:="		, "0s",
                    "Steps To:="		, "0.0025s",
                    "UseNonLinearIterNum:="	, False,
                    "CacheSaveKind:="	, "Count",
                    "NumberSolveSteps:="	, 1,
                    "RangeStart:="		, "0s",
                    "RangeEnd:="		, "0.1s"
                ])
            self.HBCPM.save_project()

    def create_report(self):
        #################################################################
        # generate report

        if(self.Postprocessing):
            print("postprocessing")

            # postprocessing
            self.output_vars = {
                
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

            for k, v in self.output_vars.items():
                self.HBCPM.create_output_variable(k, v)

            # Single plot
            self.post_params = {"TorqueRotation.Torque": "TorqueRotation",
                        "TorqueTilt.Torque": "TorqueTilt",}

            # multiple plot
            self.post_params_multiplot = {  
            # reports

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
            for k, v in self.post_params.items():
                self.HBCPM.post.create_report(expressions=k, setup_sweep_name="",
                                    domain="Sweep", variations=None,
                                    primary_sweep_variable="Time", secondary_sweep_variable=None,
                                    report_category=None, plot_type="Rectangular Plot",
                                    context=None, subdesign_id=None,
                                    polyline_points=1001, plot_name=v)

            # generate multi plot report
            for k, v in self.post_params_multiplot.items():
                self.HBCPM.post.create_report(expressions=list(k), setup_sweep_name="",
                                    domain="Sweep", variations=None,
                                    primary_sweep_variable="Time", secondary_sweep_variable=None,
                                    report_category=None, plot_type="Rectangular Plot",
                                    context=None, subdesign_id=None,
                                    polyline_points=1001, plot_name=v)


            # Create field report
            oModule = self.oDesign.GetModule("FieldsReporter")
            oModule.LoadNamedExpressions(self.Proj_path+"/cal.clc", "Fields", ["B_air", "Br", "Bt"])

            oModule.CreateFieldPlot(
                [
                    "NAME:XZ_Plane",
                    "SolutionName:="	, self.setup_name+" : Transient",
                    "UserSpecifyName:="	, 0,
                    "UserSpecifyFolder:="	, 0,
                    "QuantityName:="	, "Mag_B",
                    "PlotFolder:="		, "B",
                    "StreamlinePlot:="	, False,
                    "AdjacentSidePlot:="	, False,
                    "FullModelPlot:="	, False,
                    "IntrinsicVar:="	, "Time=\'0\'",
                    "PlotGeomInfo:="	, [1,"Surface","CutPlane",1,"Global:XZ"],
                    "FilterBoxes:="		, [0],
                    [
                        "NAME:PlotOnSurfaceSettings",
                        "Filled:="		, False,
                        "IsoValType:="		, "Tone",
                        "AddGrid:="		, False,
                        "MapTransparency:="	, True,
                        "Refinement:="		, 0,
                        "Transparency:="	, 0,
                        "SmoothingLevel:="	, 0,
                        "ShadingType:="		, 0,
                        [
                            "NAME:Arrow3DSpacingSettings",
                            "ArrowUniform:="	, True,
                            "ArrowSpacing:="	, 0,
                            "MinArrowSpacing:="	, 0,
                            "MaxArrowSpacing:="	, 0
                        ],
                        "GridColor:="		, [255,255,255]
                    ],
                    "EnableGaussianSmoothing:=", False,
                    "SurfaceOnly:="		, False
                ], "Field")

            oModule.CreateFieldPlot(
                [
                    "NAME:XY_Plane",
                    "SolutionName:="	, self.setup_name+" : Transient",
                    "UserSpecifyName:="	, 0,
                    "UserSpecifyFolder:="	, 0,
                    "QuantityName:="	, "Mag_B",
                    "PlotFolder:="		, "B",
                    "StreamlinePlot:="	, False,
                    "AdjacentSidePlot:="	, False,
                    "FullModelPlot:="	, False,
                    "IntrinsicVar:="	, "Time=\'0\'",
                    "PlotGeomInfo:="	, [1,"Surface","CutPlane",1,"Global:XY"],
                    "FilterBoxes:="		, [0],
                    [
                        "NAME:PlotOnSurfaceSettings",
                        "Filled:="		, False,
                        "IsoValType:="		, "Tone",
                        "AddGrid:="		, False,
                        "MapTransparency:="	, True,
                        "Refinement:="		, 0,
                        "Transparency:="	, 0,
                        "SmoothingLevel:="	, 0,
                        "ShadingType:="		, 0,
                        [
                            "NAME:Arrow3DSpacingSettings",
                            "ArrowUniform:="	, True,
                            "ArrowSpacing:="	, 0,
                            "MinArrowSpacing:="	, 0,
                            "MaxArrowSpacing:="	, 0
                        ],
                        "GridColor:="		, [255,255,255]
                    ],
                    "EnableGaussianSmoothing:=", False,
                    "SurfaceOnly:="		, False
                ], "Field")

            oModule = self.oDesign.GetModule("ReportSetup")
            oModule.CreateReport(self.AirgapCircleSweep, "Fields", "Rectangular Plot", self.setup_name+" : Transient", 
            [
                "Context:="		, self.AirgapCircleSweep,
                "PointCount:="		, 361
            ], 
            [
                "Distance:="		, ["All"],
                "Time:="		, ["All"],
                "RadialPMNumber:="	, ["Nominal"],
                "StatorPoleNumber:="	, ["Nominal"],
                "RadialPMAngle:="	, ["Nominal"],
                "RotorInnerRadius:="	, ["Nominal"],
                "RotorCenterThickness:=", ["Nominal"],
                "RotorOuterRadius:="	, ["Nominal"],
                "RadialPMThickness:="	, ["Nominal"],
                "RotorPMAxialThickness:=", ["Nominal"],
                "RotorIronOuterRadius:=", ["Nominal"],
                "RotorIronThickness:="	, ["Nominal"],
                "RotorPMAxialOuterRadius:=", ["Nominal"],
                "RotorPMInnerRadius:="	, ["Nominal"],
                "StatorYokeWidth:="	, ["Nominal"],
                "StatorInnerRadius:="	, ["Nominal"],
                "StatorAxialThickness:=", ["Nominal"],
                "StatorOuterRadius:="	, ["Nominal"],
                "StatorPoleWidth:="	, ["Nominal"],
                "StatorPMOuterRadius:="	, ["Nominal"],
                "StatorPMThickness:="	, ["Nominal"],
                "StatorIronThickness:="	, ["Nominal"],
                "StatorIronOuterRadius:=", ["Nominal"],
                "RotorIronInnerRadius:=", ["Nominal"],
                "StatorPoleTeethAdditionLength:=", ["Nominal"],
                "StatorPoleTeethAngle:=", ["Nominal"],
                "StatorPoleTeethStartX:=", ["Nominal"],
                "SusWindThickness:="	, ["Nominal"],
                "SusWindingLength:="	, ["Nominal"],
                "WindingThickness:="	, ["Nominal"],
                "WindingRadialLength:="	, ["Nominal"],
                "Velocity_rpm:="	    , ["Nominal"],
                "turnm:="		, ["Nominal"],
                "turns:="		, ["Nominal"],
                "Im:="			, ["Nominal"],
                "Is_a:="		, ["Nominal"],
                "Is_b:="		, ["Nominal"],
                "NumPolePairs:="	, ["Nominal"],
                "R_phase:="		, ["Nominal"]
            ], 
            [
                "X Component:="		, "360*Distance/ ((StatorInnerRadius/2+ RotorOuterRadius/2)*2*pi)",
                "Y Component:="		, ["B_air"]
            ])

            oModule.CreateReport(self.AirgapAxialSweepList[0], "Fields", "Rectangular Plot", self.setup_name+" : Transient", 
            [
                "Context:="		, self.AirgapAxialSweepList[0],
                "PointCount:="		, 101
            ], 
            [
                "Distance:="		, ["All"],
                "Time:="		, ["All"],
                "RadialPMNumber:="	, ["Nominal"],
                "StatorPoleNumber:="	, ["Nominal"],
                "RadialPMAngle:="	, ["Nominal"],
                "RotorInnerRadius:="	, ["Nominal"],
                "RotorCenterThickness:=", ["Nominal"],
                "RotorOuterRadius:="	, ["Nominal"],
                "RadialPMThickness:="	, ["Nominal"],
                "RotorPMAxialThickness:=", ["Nominal"],
                "RotorIronOuterRadius:=", ["Nominal"],
                "RotorIronThickness:="	, ["Nominal"],
                "RotorPMAxialOuterRadius:=", ["Nominal"],
                "RotorPMInnerRadius:="	, ["Nominal"],
                "StatorYokeWidth:="	, ["Nominal"],
                "StatorInnerRadius:="	, ["Nominal"],
                "StatorAxialThickness:=", ["Nominal"],
                "StatorOuterRadius:="	, ["Nominal"],
                "StatorPoleWidth:="	, ["Nominal"],
                "StatorPMOuterRadius:="	, ["Nominal"],
                "StatorPMThickness:="	, ["Nominal"],
                "StatorIronThickness:="	, ["Nominal"],
                "StatorIronOuterRadius:=", ["Nominal"],
                "RotorIronInnerRadius:=", ["Nominal"],
                "StatorPoleTeethAdditionLength:=", ["Nominal"],
                "StatorPoleTeethAngle:=", ["Nominal"],
                "StatorPoleTeethStartX:=", ["Nominal"],
                "SusWindThickness:="	, ["Nominal"],
                "SusWindingLength:="	, ["Nominal"],
                "WindingThickness:="	, ["Nominal"],
                "WindingRadialLength:="	, ["Nominal"],
                "Velocity_rpm:="		, ["Nominal"],
                "turnm:="		, ["Nominal"],
                "turns:="		, ["Nominal"],
                "Im:="			, ["Nominal"],
                "Is_a:="		, ["Nominal"],
                "Is_b:="		, ["Nominal"],
                "NumPolePairs:="	, ["Nominal"],
                "R_phase:="		, ["Nominal"]
            ], 
            [
                "X Component:="		, "Distance",
                "Y Component:="		, ["B_air"]
            ])

            self.HBCPM.save_project()

    def resume_project(self, project_name=None):

        if project_name is not None:

            AedtVersion = "2024.1"  # Replace with your installed AEDT version
            print("Open project"+project_name)
            self.project_path = os.path.dirname(project_name) 
            # example: C:/he/HBCPM/4p12s_HBCPM_with_radial_PM_four_slotProject_TZ8
            self.ProjectName=os.path.basename(project_name)
            # example: Project_TZ8.aedt
            print(self.ProjectName+"**************************")

            try:
                os.makedirs(self.project_path+"/"+"torque report", exist_ok=True)  
                    # 'exist_ok=True' prevents error if the directory exists
            except Exception as e:
                print(f"An error occurred when create torque report: {e}")

            try:
                os.makedirs(self.project_path+"/"+"force report", exist_ok=True)  
                    # 'exist_ok=True' prevents error if the directory exists
            except Exception as e:
                print(f"An error occurred when create force report: {e}")

            self.desktop = Desktop(version=AedtVersion,new_desktop=True, non_graphical=False, close_on_exit=True)
            # print(desktop.odesktop)

            self.HBCPM = Maxwell3d(
                            project=project_name,
                            solution_type="",
                            version=AedtVersion,
                            new_desktop=True, 
                            non_graphical=False, 
                            close_on_exit=True)

            self.DesignName = self.HBCPM.design_name
            print(self.params)

            self.oProject =self.desktop.odesktop.GetActiveProject()
            self.oDesign = self.oProject.GetActiveDesign()

            oEditor = self.oDesign.SetActiveEditor("3D Modeler")

            print(self.oDesign)
            print(self.oProject)
            print(oEditor)

            # resume parameters
            self.setup_name="MySetupAuto"

            self.output_vars = {
                
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

            # Single plot
            self.post_params = {"TorqueRotation.Torque": "TorqueRotation",
                        "TorqueTilt.Torque": "TorqueTilt",}

            # multiple plot
            self.post_params_multiplot = {  
            # reports

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

    def generate_mesh_export(self):
        #################################################################
        # Generate mesh and export mesh to file

        self.oDesign.GenerateMesh(self.setup_name)
        self.oDesign.ExportMeshStats(self.setup_name,"All",self.project_path+"/"+"meshstats.ms")

    def analyze_torque(self, Im=1, Is_a=0, Is_b=0):
        #################################################################
        # Analyze setup and export report to file
        # 4 cpu cores
        self.HBCPM.cleanup_solution(variations="All", entire_solution=True, field=True, mesh=True, linked_data=True)
        
        self.Im=Im
        self.Is_a=Is_a
        self.Is_b=Is_b
        current_variable={
            "Im": str(self.Im)+"A",
            "Is_a": str(self.Is_a)+"A",
            "Is_b": str(self.Is_b)+"A",
        }
         # This call returns the VariableManager class
        # Iterate through the dictionary and set each variable
        for var_name, expression in current_variable.items():
            self.HBCPM.variable_manager.set_variable(var_name, expression=expression)

        print("Rotational torque Analysis start")
        self.HBCPM.analyze_setup(self.setup_name, use_auto_settings=False, cores=4)

        # # Single plot
        # post_params = {"TorqueRotation.Torque": "TorqueRotation",
        #             "TorqueTilt.Torque": "TorqueTilt",}

        oModule = self.oDesign.GetModule("ReportSetup")

        # update single plot report
        for k, v in self.post_params.items():
            k_list=[k]
            oModule.UpdateTracesContextAndSweeps(v, k_list, self.setup_name+" : Transient", 
                [
                    "Domain:="		, "Sweep"
                ], 
                [
                    "Time:="		, ["All"]
                ])

        # update multi plot report
        for k, v in self.post_params_multiplot.items():
            k_list=list(k)
            oModule.UpdateTracesContextAndSweeps(v, k_list, self.setup_name+" : Transient", 
                [
                    "Domain:="		, "Sweep"
                ], 
                [
                    "Time:="		, ["All"]
                ])


        try:
            os.makedirs(self.project_path+"/"+"torque report", exist_ok=True)  
                # 'exist_ok=True' prevents error if the directory exists
        except Exception as e:
            print(f"An error occurred when create torque report: {e}")



        # export single plot report
        for k, v in self.post_params.items():
            self.HBCPM.post.export_report_to_file(output_dir=self.project_path+"/"+"torque report", 
                                        plot_name=v, 
                                        extension=".csv")

        # export multi plot report
        for k, v in self.post_params_multiplot.items():
            self.HBCPM.post.export_report_to_file(output_dir=self.project_path+"/"+"torque report", 
                                        plot_name=v, 
                                        extension=".csv")

    def analyze_force(self, Im=0, Is_a=1, Is_b=1):
        #################################################################
        # Analyze setup and export report to file
        # 4 cpu cores

        self.HBCPM.cleanup_solution(variations="All", entire_solution=True, field=True, mesh=True, linked_data=True)
        
        self.Im=Im
        self.Is_a=Is_a
        self.Is_b=Is_b
        current_variable={
            "Im": str(self.Im)+"A",
            "Is_a": str(self.Is_a)+"A",
            "Is_b": str(self.Is_b)+"A",
        }
         # This call returns the VariableManager class
        # Iterate through the dictionary and set each variable
        for var_name, expression in current_variable.items():
            self.HBCPM.variable_manager.set_variable(var_name, expression=expression)

        print("Force Analysis start")
        self.HBCPM.analyze_setup(self.setup_name, use_auto_settings=False, cores=4)

        # # Single plot
        # post_params = {"TorqueRotation.Torque": "TorqueRotation",
        #             "TorqueTilt.Torque": "TorqueTilt",}

        oModule = self.oDesign.GetModule("ReportSetup")

        # update single plot report
        for k, v in self.post_params.items():
            k_list=[k]
            oModule.UpdateTracesContextAndSweeps(v, k_list, self.setup_name+" : Transient", 
                [
                    "Domain:="		, "Sweep"
                ], 
                [
                    "Time:="		, ["All"]
                ])

        # update multi plot report
        for k, v in self.post_params_multiplot.items():
            k_list=list(k)
            oModule.UpdateTracesContextAndSweeps(v, k_list, self.setup_name+" : Transient", 
                [
                    "Domain:="		, "Sweep"
                ], 
                [
                    "Time:="		, ["All"]
                ])


            try:
                os.makedirs(self.project_path+"/"+"force report", exist_ok=True)  
                    # 'exist_ok=True' prevents error if the directory exists
            except Exception as e:
                print(f"An error occurred when create force report: {e}")


        # export single plot report
        for k, v in self.post_params.items():
            self.HBCPM.post.export_report_to_file(output_dir=self.project_path+"/"+"force report", 
                                        plot_name=v, 
                                        extension=".csv")

        # export multi plot report
        for k, v in self.post_params_multiplot.items():
            self.HBCPM.post.export_report_to_file(output_dir=self.project_path+"/"+"force report", 
                                        plot_name=v, 
                                        extension=".csv")

        # 	solutions = HBCPM.post.get_solution_data(
        # 		expressions="Moving1.Torque", primary_sweep_variable="Time"
        # 	)
        # 	mag = solutions.data_magnitude()
        # 	avg = sum(mag) / len(mag)
        # 	# solutions.plot()

        #################################################################
        # Using builtin optimizer or selfdefine optimizer

        """	
        if(self.BuildInOptimization):
        # Set Optimization  

            oModule = self.oDesign.GetModule("Optimetrics")

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

    def release_project(self):
        self.HBCPM.save_project()
        self.HBCPM.release_desktop()
