import numpy as np
import math

class HBCPMConcentratedWindingParameters:
    def __init__(self,params=None):
        
        defaults_para = {
            "NumPolePairs": 4,
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
            "SuspensionWindingFullSlot": True,

            "rpm": 3000,
            "turnm": 90,
            "turns": 100,
            "Im": 2,
            "R_phase": 0.6,

            "Is_a":0,
            "Is_b":0,

        }

        # Update defaults with provided params
        if params is not None:
            defaults_para.update(params)

        # # Dynamically set attributes
        # for key, value in defaults.items():
        #     setattr(self, key, value)
            
        self.RadialPM = defaults_para["RadialPM"]
        self.RadialPMNumber = defaults_para["NumPolePairs"]
        self.StatorPoleNumber = defaults_para["StatorPoleNumber"]
        self.RadialPMAngle = 360 / 2 / defaults_para["NumPolePairs"] * defaults_para["RadialPMPoleArcRatio"]  # Percentage

        self.RotorInnerRadius = defaults_para["RotorInnerRadius"]
        self.RotorCenterThickness = defaults_para["RotorCenterThickness"]
        self.RotorOuterRadius = defaults_para["RotorOuterRadius"]
        self.RadialPMThickness = defaults_para["RadialPMThickness"]
        self.RotorPMAxialThickness = defaults_para["RotorPMAxialThickness"]

        self.RotorIronOuterRadius = defaults_para["RotorIronOuterRadius"]
        self.RotorIronThickness = defaults_para["RotorIronThickness"]
        self.RotorIronInnerRadius = (
            defaults_para["RotorIronOuterRadius"] - defaults_para["RotorPMAxialRadialWidth"] - defaults_para["RotorPMAxialRadialWidth"] + 1
        )

        self.RotorPMAxialOuterRadius = defaults_para["RotorOuterRadius"] - defaults_para["RadialPMThickness"]
        self.RotorPMInnerRadius = self.RotorPMAxialOuterRadius - defaults_para["RotorPMAxialRadialWidth"]

        self.StatorYokeWidth = defaults_para["StatorYokeWidth"]
        self.StatorInnerRadius = defaults_para["StatorInnerRadius"]
        self.StatorAxialThickness = defaults_para["StatorAxialThickness"]
        self.StatorOuterRadius = defaults_para["StatorOuterRadius"]

        self.StatorPoleWidth = (
            2 * np.sin(defaults_para["StatorPoleWidthArcRatio"] * np.pi / defaults_para["StatorPoleNumber"]) * defaults_para["StatorInnerRadius"]
        )
        self.StatorPMOuterRadius = defaults_para["StatorInnerRadius"] + defaults_para["StatorPMRadialWidth"]

        self.StatorPMThickness = defaults_para["StatorPMThickness"]
        self.StatorIronThickness = defaults_para["StatorIronThickness"]
        self.StatorIronOuterRadius = defaults_para["StatorInnerRadius"] + defaults_para["StatorPMRadialWidth"] - 1

        self.StatorPoleTeethAdditionLength = self.StatorPoleWidth * defaults_para["StatorPoleToothWidthArcRatio"]
        self.StatorPoleTeethAngle = defaults_para["StatorPoleTeethAngle"]
        self.StatorPoleTeethStartX = np.sqrt(
            self.StatorPMOuterRadius**2 - (self.StatorPoleWidth / 2)**2
        )

        self.WindingThickness = self.StatorPoleWidth / 3
        self.SusWindThickness = self.StatorYokeWidth / 4
        self.WindingRadialLength = defaults_para["WindingRadialLength"]
        self.SusWindLength = (2* np.pi * (self.StatorOuterRadius-self.StatorYokeWidth/2)/self.StatorPoleNumber-self.StatorPoleWidth)*0.72
        self.SuspensionWindingFullSlot = defaults_para["SuspensionWindingFullSlot"]

        self.rpm = defaults_para["rpm"]

        self.turnm = defaults_para["turnm"]
        self.turns = defaults_para["turns"]
        self.Im = defaults_para["Im"]

        self.NumPolePairs = defaults_para["NumPolePairs"]
        self.R_phase = defaults_para["R_phase"]

        self.Armature_coil_number=self.StatorPoleNumber

        self.Is_a=defaults_para["Is_a"]
        self.Is_b=defaults_para["Is_b"]


        # self.RadialPMNumber = NumPolePairs
        # self.StatorPoleNumber = StatorPoleNumber
        # self.RadialPMAngle = 360/2/NumPolePairs*RadialPMPoleArcRatio # Percentage

        # self.RotorInnerRadius = RotorInnerRadius
        # self.RotorCenterThickness = RotorCenterThickness
        # self.RotorOuterRadius = RotorOuterRadius
        # self.RadialPMThickness = RadialPMThickness
        # self.RotorPMAxialThickness = RotorPMAxialThickness

        # self.RotorIronOuterRadius = RotorIronOuterRadius
        # self.RotorIronThickness = RotorIronThickness
        # self.RotorIronInnerRadius = RotorIronOuterRadius - RotorPMAxialRadialWidth - RotorPMAxialRadialWidth+1

        # self.RotorPMAxialOuterRadius = RotorOuterRadius - RadialPMThickness
        # self.RotorPMInnerRadius = self.RotorPMAxialOuterRadius - RotorPMAxialRadialWidth

        # self.StatorYokeWidth = StatorYokeWidth
        # self.StatorInnerRadius = StatorInnerRadius
        # self.StatorAxialThickness = StatorAxialThickness
        # self.StatorOuterRadius = StatorOuterRadius

        # self.StatorPoleWidth = 2*np.sin(StatorPoleWidthArcRatio*np.pi/StatorPoleNumber) * StatorInnerRadius
        # self.StatorPMOuterRadius = StatorInnerRadius + StatorPMRadialWidth
    
        # self.StatorPMThickness = StatorPMThickness
        # self.StatorIronThickness = StatorIronThickness
        # self.StatorIronOuterRadius = StatorInnerRadius + StatorPMRadialWidth - 1

        # self.StatorPoleTeethAdditionLength = self.StatorPoleWidth*StatorPoleToothWidthArcRatio
        # self.StatorPoleTeethAngle = StatorPoleTeethAngle
        # self.StatorPoleTeethStartX = np.sqrt(self.StatorPMOuterRadius**2-(self.StatorPoleWidth/2)**2)

        # self.WindingThickness = self.StatorPoleWidth/3
        # self.WindingRadialLength = WindingRadialLength
        # self.rpm = rpm

        # self.turnm = turnm
        # self.turns = turns
        # self.Im = Im

        # self.NumPolePairs = NumPolePairs
        # self.R_phase = R_phase