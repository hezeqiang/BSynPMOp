import pygmo as pg
import numpy as np
import matplotlib as mpl
from collections import OrderedDict
import matplotlib.pyplot as plt
from AirgapFluxDensityDefine import AirgapFluxDensity
from PhaseFluxLinkageCal import FluxLinkageCalculator
from EMF_calculator import EMF_Calculator
from FFT_analyzer import FFTAnalyser
from FFT_analyzer import generate_cos_list_and_plot
from Power_torque_calculator import ThreePhaseMotorPower
from RotorRadialForceCal import RotorRadialForceCalculator


##################################################################
# Abbreviations:
# GP = GeometricParameters
# EX = OtherProperties
# SI = SpecificationDictionary


# # Update rcParams to use LaTeX
# mpl.rcParams.update({
#     "text.usetex": True,              # Use LaTeX to render text
#     "font.family": "serif",           # Use serif fonts
#     "font.serif": ["Computer Modern"],# Use the Computer Modern font
#     "axes.labelsize": 10,             # Font size for axis labels
#     "font.size": 10,                  # Font size for general text
#     "legend.fontsize": 8,             # Font size for legend
#     "xtick.labelsize": 8,             # Font size for x tick labels
#     "ytick.labelsize": 8,             # Font size for y tick labels
#     "figure.figsize": [4.5, 3.0],     # Figure size (in inches)
#     "figure.dpi": 300,                # Figure dots-per-inch
# })

###########################################################################
# Geometric Parameters
npp=4
Mechanical_speed_rpm=3000
current_amplitudes=1
suspension_flux_density = 0.05 # 0.05 T biased flux

Angle_list = np.arange(0, 361, 3).tolist()
Rotor_PM_angle=45 # degree
Rotor_salient_ratio = 1 # 1 for round rotor
Rotor_PM_thickness = 1 # mm
Rotor_Axial_PM_influence_salient = 0.1 # 0.1 T bias in salient pole
Rotor_Axial_PM_influence_Nonsalient = 0.1 * Rotor_salient_ratio
ArmatureTurn=90
Armaturecoil_span=1/3   # 360/3
motor_thickness=0.008
airgap_radius=0.026
Rotor_Axial_PM_thickness=0.002
Rotor_Axial_PM_inner_radius=0.020
Rotor_Axial_PM_outer_radius=0.023

Stator_Axial_PM_thickness=0.002
Stator_Axial_PM_inner_radius=0.026
Stator_Axial_PM_outer_radius=0.029

airgap_flux_density_top_amplitude=0.4
airgap_flux_density_bottom_amplitude=-0.4
airgap_flux_density_flat_top_ratio=0.32
airgap_flux_density_flat_bottom_ratio=0.5


# plot figures or not
plot_use_Cartesian=True

##############################################################################


Mechanical_speed_rad=Mechanical_speed_rpm/60*2*np.pi
Mechanical_cycle_time=1/(Mechanical_speed_rpm/60)
Mechanical_fund_freq=(Mechanical_speed_rpm/60)
Electrical_fund_freq=(Mechanical_speed_rpm/60)*npp
Mechanical_speed_deg_per_second = Mechanical_speed_rpm / 60 * 360
Angle_per_step=360/len(Angle_list) # degree
Time_step = Angle_per_step / Mechanical_speed_deg_per_second

###############################################################################



if(1):
    fig, ax = plt.subplots(nrows=2, ncols=2)

    ax[0,0].set_xlabel("Angle (Deg)")
    ax[0,0].set_xlabel("")
    ax[0,0].set_xlim(0, 360)  # Adjust these values as needed
    ax[0,0].grid(True)

    ax[0,1].set_xlabel("Angle (Deg)")
    ax[0,1].set_ylabel("Flux density (T)")
    ax[0,1].set_xlim(0, 360)  # Adjust these values as needed
    ax[0,1].grid(True)

    ax[1,0].set_xlabel("Angle (Deg)")
    ax[1,0].set_ylabel("Flux linkage (Wb)")
    ax[1,0].set_xlim(0, 360)  # Adjust these values as needed
    ax[1,0].grid(True)

    ax[1,1].set_xlabel("Angle (Deg)")
    ax[1,1].set_ylabel("EMF (V)")
    ax[1,1].set_xlim(0, 360)  # Adjust these values as needed
    ax[1,1].grid(True)

    ax[1,0].legend()
    ax[1,1].legend()


Flux_calculator = FluxLinkageCalculator(ArmatureTurn=ArmatureTurn, 
                                        coil_span=Armaturecoil_span, 
                                        cycle_number=npp, 
                                        motor_thickness=motor_thickness,
                                        arigap_raduis=airgap_radius)
Flux_calculator.plot_coils_Cartesian(ax[0,0])


Airgap_flux = AirgapFluxDensity(top_amplitude=airgap_flux_density_top_amplitude, 
                                bottom_amplitude=airgap_flux_density_bottom_amplitude, 
                                flat_top_ratio=airgap_flux_density_flat_top_ratio, 
                                flat_bottom_ratio=airgap_flux_density_flat_bottom_ratio, 
                                resolution=1000,  
                                cycles_number=npp)
# Use plot_waveform on one of the subplots
Airgap_flux.plot_waveform(ax[0, 1])

EMF_calculator = EMF_Calculator()


"""
Phase flux calculation 
"""

# Crate a list to store the flux linkage of each phase from  0 to 360 degrees
fluxlinkage_list={}

fluxlinkage_list['A phase']=[]
fluxlinkage_list['B phase']=[]
fluxlinkage_list['C phase']=[]
###########################################################################

for index, Angle in enumerate(Angle_list):
    # if Angle==0:
    #     airgap_flux.plot_waveform(ax)
    #     # airgap_flux.waveform_shift_by_rotor_angle(30)
    #     calculator.fluxlinkage_cal(airgap_flux.waveform)
    #     calculator.plot_coils_Cartesian(ax)
    #     plt.show()
    Flux_result = Flux_calculator.fluxlinkage_cal(Airgap_flux.waveform_shifted)  #{'A': 25.881904510252298, 'B': 9.094947017729282e-13, 'C': -4.547473508864641e-13}

    fluxlinkage_list['A phase'].append(Flux_result['A'])
    fluxlinkage_list['B phase'].append(Flux_result['B'])
    fluxlinkage_list['C phase'].append(Flux_result['C'])

    Airgap_flux.waveform_shift_by_rotor_angle(Angle)
    # if (Angle==45):
    #     Airgap_flux.plot_shift_waveform(ax[0, 1])


# print(fluxlinkage_list)
colors = ['red', 'blue', 'green']

colorsindex=0
for key, value in fluxlinkage_list.items():
    ax[1,0].plot(Angle_list,value,label=key,color=colors[colorsindex])
    colorsindex+=1

"""
EMF calculation and FFT analysis
"""
# Crate a list to store the EMF of each phase from  0 to 360 degrees
EMF_list={}

colorsindex=0
for key, value in fluxlinkage_list.items():
    EMF_list[key] = EMF_calculator.EMF_cal_fluxlinkage(value, Time_step)
    ax[1,1].plot(Angle_list[:-1],EMF_list[key],label=key,color=colors[colorsindex])
    colorsindex+=1

ax[1,0].legend()
ax[1,1].legend()

fig_FFT, ax_FFT = plt.subplots()

Phase_current_list={}

for key, value in EMF_list.items():
    analyser = FFTAnalyser(value, cycle=Mechanical_cycle_time)
    analyser.compute_fft()
    if (key=='A phase'):
        analyser.plot_frequency_components(ax=ax_FFT)

    index_of_Elect_fund_freq = np.where(analyser.positive_freqs == Electrical_fund_freq)[0][0]
    # print(index_of_Elect_fund_freq)
    Elect_fund_freq_phase = analyser.positive_phase[index_of_Elect_fund_freq]
    Elect_fund_freq_amplitudes= analyser.positive_amplitudes[index_of_Elect_fund_freq]

    Phase_current_list[key]=generate_cos_list_and_plot(Elect_fund_freq_phase,current_amplitudes,len(value),npp,Mechanical_cycle_time,ax=ax_FFT)

"""
Power and torque calculation
"""
fig_powertorque, ax_powertorque = plt.subplots(nrows=2)
    
# Crate a list to store the power and torque of each phase from  0 to 360 degrees

PhasePowerTorque = ThreePhaseMotorPower(EMF_list, Phase_current_list, Mechanical_speed_rad, 1/len(Angle_list))
power, torque = PhasePowerTorque.calculate_power_and_torque()

PhasePowerTorque.plot_power_and_torque(ax=ax_powertorque)

print("Torque Avg:", torque.mean(),"Torque Var:", torque.var())


"""
Suspension force estimation
"""

Force={"X-axis force":[],
       "Y-axis force":[]}

Force_calculator = RotorRadialForceCalculator(airgap_radius, motor_thickness)

for index, Angle in enumerate(Angle_list):
    
    Airgap_flux.flux_density_by_suspension_shift(suspension_flux_influ=suspension_flux_density,rotor_angle=Angle)

    Fx, Fy = Force_calculator.calculate_radial_force(Airgap_flux.waveform_shift_superimposed)
    # print("X-axis force:", Fx,"Y-axis force:", Fy)

    Force["X-axis force"].append(Fx)
    Force["Y-axis force"].append(Fy)



fig_force, ax_force = plt.subplots()

colorsindex=0
for key, value in Force.items():
    ax_force.plot(Angle_list,value,label=key,color=colors[colorsindex])
    colorsindex+=1


#######################################################################################
    
if (plot_use_Cartesian==True):
    plt.show()


