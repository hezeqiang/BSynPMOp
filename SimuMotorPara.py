import numpy as np

class HBCPMConcentratedWindingParameters:
    def __init__(
        self,
        NumPolePairs=4,       
        RadialPMPoleArcRatio= 0.8,

        RadialPMThickness=2,

        RotorInnerRadius=16.6,
        RotorCenterThickness=8,
        RotorOuterRadius=25, 

        RotorPMAxialThickness=2,
        RotorPMAxialRadialWidth=3,

        RotorIronOuterRadius=25,
        RotorIronThickness=1.5,

        StatorInnerRadius=27,
        StatorAxialThickness=8,
        StatorOuterRadius=56,
        StatorPoleWidthArcRatio= 0.57 ,
        StatorPoleNumber= 12 ,   
        StatorYokeWidth=8,

        StatorPMRadialWidth=3,
        StatorPMThickness=2,
        StatorIronThickness=1.5,

        StatorPoleToothWidthArcRatio = 1/4 ,
        StatorPoleTeethAngle=45,

        WindingThickness=2.6,
        WindingRadialLength=13.3,

        rpm=3000,
        turnm=90,
        turns=100,
        Im=2,
        R_phase=0.6
    ):
        
        self.RadialPMNumber = NumPolePairs
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

        self.StatorPoleWidth = 2*np.sin(StatorPoleWidthArcRatio*np.pi/12) * StatorInnerRadius
        self.StatorPMOuterRadius = StatorInnerRadius + StatorPMRadialWidth
    
        self.StatorPMThickness = StatorPMThickness
        self.StatorIronThickness = StatorIronThickness
        self.StatorIronOuterRadius = StatorInnerRadius + StatorPMRadialWidth - 1

        self.StatorPoleTeethAdditionLength = self.StatorPoleWidth*StatorPoleToothWidthArcRatio
        self.StatorPoleTeethAngle = StatorPoleTeethAngle

        self.WindingThickness = WindingThickness
        self.WindingRadialLength = WindingRadialLength
        self.rpm = rpm

        self.turnm = turnm
        self.turns = turns
        self.Im = Im

        self.NumPolePairs = NumPolePairs
        self.R_phase = R_phase