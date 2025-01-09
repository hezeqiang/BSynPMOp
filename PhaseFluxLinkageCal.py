import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

class FluxLinkageCalculator:
    def __init__(self, ArmatureTurn, coil_span, cycle_number,motor_thickness,arigap_raduis):
        """
        Initialize the FluxLinkageCalculator class.

        Parameters:
        ArmatureTurn (int): Number of turns of the coil.
        coil_span (float): Span of each coil in terms of the cycle angle (fraction of 360 degrees).
        cycle_number (int): Number of cycles of the magnetic field.
        """
        self.ArmatureTurn = ArmatureTurn
        self.coil_span = coil_span
        self.cycle_number = cycle_number
        self.motor_thickness=motor_thickness
        self.arigap_raduis=arigap_raduis

    def fluxlinkage_cal(self, fluxdensitylist):
        """
        Calculate the flux linkage for the coils.

        Parameters:
        fluxdensitylist (list): List of magnetic field flux density covering 0 to 360 degrees.

        Returns:
        dict: Flux linkage for each phase (A, B, C).
        """
        # Ensure the fluxdensitylist covers exactly one cycle of 360 degrees
        if not all(isinstance(x, (int, float)) for x in fluxdensitylist):
            raise ValueError("fluxdensitylist must contain only numerical values.")
        
        num_points = len(fluxdensitylist)
        angle_step = 360 / num_points

        # Initialize flux linkage for each phase
        flux_linkage = {'A': 0, 'B': 0, 'C': 0}


        for phase_index, phase in enumerate(['A', 'B', 'C']):
            for coil_index in range(self.cycle_number):
                # Determine start and end angles of the coil
                start_angle = (phase_index * 120 + coil_index * 360 - 120 / 2 )/ self.cycle_number 
                end_angle = (start_angle + self.coil_span * 360 / self.cycle_number)

                # print(phase_index,coil_index, start_angle,end_angle)

                # Convert angles to indices in the fluxdensitylist
                start_idx = int(start_angle / angle_step)
                end_idx = int(end_angle / angle_step)

                # Calculate flux linkage for the coil
                if start_idx >0:
                    coil_flux = sum(fluxdensitylist[start_idx:end_idx]) * angle_step
                else:  # Wraps around the list
                    coil_flux = sum(fluxdensitylist[start_idx:]) * angle_step + sum(fluxdensitylist[:end_idx]) * angle_step

                # Multiply by the number of turns and add to the phase
                flux_linkage[phase] += coil_flux * self.ArmatureTurn * 2 * np.pi/360 * self.arigap_raduis * self.motor_thickness 

        return flux_linkage

    def plot_coils_polar(self,ax=None):
        """
        Plot the coils around a circle to visualize their arrangement.
    
        """
        if (ax==None):
            fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

            # Number of coils per phase
            total_coils = self.cycle_number * 3

        for phase_index, phase in enumerate(['A', 'B', 'C']):
            for coil_index in range(self.cycle_number):
                # Calculate the start and end angles of the coil
                start_angle = np.radians((phase_index * 120 + coil_index * 360 - 120 / 2 )/ self.cycle_number )
                end_angle = np.radians(np.degrees(start_angle) + self.coil_span * 360 / self.cycle_number)

                # print(phase_index,coil_index, start_angle,end_angle)

                # Plot the coil as an arc
                theta = np.linspace(start_angle, end_angle, 100)
                r = np.ones_like(theta) * (1 + phase_index * 0.1)  # Separate phases visually
                ax.plot(theta, r, label=f'Phase {phase} Coil {coil_index + 1}' if coil_index == 0 else "")


                # Add winding direction symbol (dot for in, cross for out)
                symbol_r = 1 + phase_index * 0.1

                ax.plot([end_angle], [symbol_r], marker='o', markersize=4, color='black')

                ax.plot([start_angle], [symbol_r], marker='x', markersize=8, color='red')

        ax.set_title("Coil Arrangement Around Circle")
        ax.legend()
                # # Plot the coil as an arc
                # theta = np.linspace(start_angle, end_angle, 100)
                # r = np.ones_like(theta) * (1 + phase_index * 0.1)  # Separate phases visually
                # # ax.plot(theta, r, label=f'Phase {phase} Coil {coil_index + 1}' if coil_index == 0 else "")
                # ax.plot(theta, r, label=f'Phase {phase} Coil {coil_index + 1}')



    def plot_coils_Cartesian(self,ax=None):
        """
        Plot the coils to visualize their arrangement.
        """
        if (ax==None):
            fig, ax = plt.subplots()
        
        colors = ['red', 'blue', 'green']

        for phase_index, phase in enumerate(['A', 'B', 'C']):
            for coil_index in range(self.cycle_number):
                # Calculate the start and end angles of the coil
                start_angle = (phase_index * 120 + coil_index * 360 - 120 / 2 )/ self.cycle_number
                end_angle = (start_angle) + self.coil_span * 360 / self.cycle_number

                print(phase_index,coil_index, start_angle,end_angle)

                if (start_angle>0):
                    # Plot the coil as an arc                 
                    theta = np.linspace(start_angle, end_angle, 100)
                    r = np.ones_like(theta) * (-0.1 + phase_index * 0.1)  # Separate phases visually

                    ax.plot(theta, r, linewidth=2, label=f'Phase {phase} ' if coil_index == 0 else "",color=colors[phase_index])

                    # Add winding direction symbol (dot for in, cross for out)
                    symbol_r = -0.1+ phase_index * 0.1

                    ax.plot(end_angle, symbol_r , marker='o', markersize=4, color='darkorange')

                    ax.plot(start_angle, symbol_r , marker='x', markersize=8, color='darkorange')

                else:
                    print(start_angle,end_angle)
                    theta1 = np.linspace(0, end_angle, 100)
                    theta2= np.linspace(start_angle+360, 360, 100)
                    r = np.ones_like(theta1) * ( -0.1 + phase_index * 0.1)  # Separate phases visually
                    ax.plot(theta1, r, linewidth=2, label=f'Phase {phase} ' if coil_index == 0 else "",color=colors[phase_index])

                    r = np.ones_like(theta2) * (-0.1 + phase_index * 0.1)  # Separate phases visually
                    ax.plot(theta2, r, linewidth=2,color=colors[phase_index])

                    # Add winding direction symbol (dot for in, cross for out)
                    symbol_r = -0.1+ phase_index * 0.1

                    ax.plot(end_angle, symbol_r , marker='o', markersize=4, color='darkorange')

                    ax.plot(start_angle+360, symbol_r , marker='x', markersize=8, color='darkorange')
                    

        ax.set_title("Coil Arrangement Around Circle with Flux Direction")
        ax.legend(loc='upper right')

# Example usage
# flux_density_list = [ ... ] # A list of flux density values from 0 to 360 degrees
# calculator = FluxLinkageCalculator(ArmatureTurn=100, coil_span=1/3, cycle_number=2)
# calculator.plot_coils_xy()
# result = calculator.fluxlinkage_cal(flux_density_list)
# print(result)



# generating ideal sinusoid wavefrom
def generate_flux_density_list(amplitude, num_points):
    """
    Generate a sinusoidal flux density list.

    Parameters:
    amplitude (float): The peak value of the sinusoidal flux density.
    num_points (int): The number of points in one cycle (360 degrees).

    Returns:
    list: A sinusoidal flux density list covering 0 to 360 degrees.
    """
    # Generate angles from 0 to 360 degrees
    angles = np.linspace(0, 360, num_points, endpoint=False)
    # Calculate the sinusoidal flux density
    flux_density = amplitude * np.sin(np.radians(angles))
    
    return flux_density.tolist()

if __name__ == '__main__':

    # Example usage
    amplitude = 1.0  # Peak value of the sinusoidal flux density
    num_points = 360  # Number of points in one cycle
    flux_density_list = generate_flux_density_list(amplitude, num_points)
    # print(flux_density_list)
    

    calculator = FluxLinkageCalculator(ArmatureTurn=100, coil_span=1/3, cycle_number=4,motor_thickness=0.008,arigap_raduis=0.026)
    result = calculator.fluxlinkage_cal(flux_density_list)
    # calculator.plot_coils_polar()
    calculator.plot_coils_Cartesian()
    print(result)