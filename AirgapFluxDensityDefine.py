import numpy as np
import matplotlib.pyplot as plt

class AirgapFluxDensity:
    def __init__(self, top_amplitude=0.4, bottom_amplitude=-0.5, flat_top_ratio=0.32, flat_bottom_ratio=0.5, resolution=3600, cycles_number=4):
        """
        Initialize the waveform parameters.

        Parameters:
        - top_amplitude: The peak value of the top part of the waveform.
        - bottom_amplitude: The peak value of the bottom part of the waveform.
        - flat_top_ratio: The ratio of the flat top regions (0 to 1) relative to one period.
        - flat_bottom_ratio: The ratio of the flat bottom regions (0 to 1) relative to one period.
        - slope_ratio: The ratio of the slope regions (0 to 1) relative to one period.
        - resolution: Number of points in one period of the waveform.
        - cycles: Number of cycles to include in the waveform.
        """
        self.top_amplitude = top_amplitude
        self.bottom_amplitude = bottom_amplitude
        self.flat_top_ratio = flat_top_ratio
        self.flat_bottom_ratio = flat_bottom_ratio
        self.slope_ratio = (1-flat_top_ratio-flat_bottom_ratio)/2
        self.resolution = resolution
        self.cycles =  cycles_number

        # Generate the waveform on initialization
        self.update_waveform()



    def update_waveform(self):
        """Generate the airgap flux density waveform based on the parameters."""
        total_ratio = self.flat_top_ratio + self.flat_bottom_ratio + 2 * self.slope_ratio
        if not np.isclose(total_ratio, 1.0):
            raise ValueError("The total ratio of the waveform (flat and slope regions) must sum to 1.0.")

        period_points = self.resolution
        flat_top_points = int(self.flat_top_ratio * period_points)
        flat_bottom_points = int(self.flat_bottom_ratio * period_points)
        slope_points = int(self.slope_ratio * period_points)

        angles = np.linspace(0, 360 * self.cycles, self.resolution * self.cycles, endpoint=False)
        waveform = []

        for i in range(len(angles)):
            mod_index = i % period_points

            if mod_index < flat_top_points/2:
                # Flat top
                value = self.top_amplitude
            elif mod_index < slope_points + flat_top_points/2:
                # Falling slope
                value = self.top_amplitude - ((self.top_amplitude - self.bottom_amplitude) * ((mod_index -  flat_top_points/2 ) / slope_points))
            elif mod_index <  flat_top_points/2 + slope_points+flat_bottom_points:
                # Flat bottom
                value = self.bottom_amplitude
            elif mod_index <  flat_top_points/2 + slope_points*2 +flat_bottom_points:
                # Rising slope for flat bottom
                value = self.bottom_amplitude + ((self.top_amplitude - self.bottom_amplitude) * ((mod_index - flat_top_points/2 - slope_points  - flat_bottom_points) / slope_points))
            else:
                value = self.top_amplitude

            waveform.append(value)

        self.waveform = np.array(waveform)
        self.waveform_superimposed = np.copy(self.waveform)
        self.waveform_shifted =np.copy(self.waveform)
        self.waveform_shift_superimposed=np.copy(self.waveform)


    def plot_waveform(self, ax=None):
        """Plot the current waveform."""
        angles = np.linspace(0, 360, self.resolution * self.cycles, endpoint=False)
        if (ax==None):
            plt.plot(angles, self.waveform, 'r')
            plt.xlabel("Angle (degrees)")
            plt.ylabel("B_air")
            plt.grid(True)
            plt.show()
        else:
            ax.plot(angles, self.waveform)

    def edit_parameters(self, top_amplitude=None, bottom_amplitude=None, flat_top_ratio=None, flat_bottom_ratio=None, resolution=None,  cycles_number=None):
        """
        Update the parameters of the waveform and regenerate it.

        Parameters:
        - top_amplitude: The new peak value of the top part of the waveform.
        - bottom_amplitude: The new peak value of the bottom part of the waveform.
        - flat_top_ratio: The new ratio of the flat top regions (0 to 1).
        - flat_bottom_ratio: The new ratio of the flat bottom regions (0 to 1).
        - slope_ratio: The new ratio of the slope regions (0 to 1).
        - resolution: The new number of points in one period of the waveform.
        - cycles: The new number of cycles to include in the waveform.
        """
        if top_amplitude is not None:
            self.top_amplitude = top_amplitude
        if bottom_amplitude is not None:
            self.bottom_amplitude = bottom_amplitude
        if flat_top_ratio is not None:
            self.flat_top_ratio = flat_top_ratio
        if flat_bottom_ratio is not None:
            self.flat_bottom_ratio = flat_bottom_ratio
        if (1-flat_top_ratio-flat_bottom_ratio)/2 is not None:
            self.slope_ratio = (1-flat_top_ratio-flat_bottom_ratio)/2
        if resolution is not None:
            self.resolution = resolution
        if  cycles_number is not None:
            self.cycles =  cycles_number

        self.update_waveform()


    def plot_shift_waveform(self, ax=None):
        """Plot the current waveform."""
        angles = np.linspace(0, 360, self.resolution * self.cycles, endpoint=False)
        if (ax==None):
            plt.plot(angles, self.waveform_shifted, 'r')
            plt.xlabel("Angle (degrees)")
            plt.ylabel("B_air")
            plt.grid(True)
            plt.show()
        else:
            ax.plot(angles, self.waveform_shifted)


    def flux_density_by_suspension(self, suspension_flux_influ=0):
        """
        Update the waveform considering the suspension flux
        The suspension flux field is a 2-pole field from +y to -y direction
        """
        length_flux_list = len(self.waveform)
        self.waveform_superimposed[:length_flux_list//8] = self.waveform[:length_flux_list//8]
        self.waveform_superimposed[length_flux_list//8+1:3*(length_flux_list//8)] = self.waveform[length_flux_list //8+1:3*(length_flux_list//8)]+suspension_flux_influ
        self.waveform_superimposed[3*(length_flux_list//8)+1:5*(length_flux_list//8)] = self.waveform[3*(length_flux_list//8)+1:5*(length_flux_list//8)]
        self.waveform_superimposed[5*(length_flux_list//8):7*(length_flux_list//8)] = self.waveform[5*(length_flux_list//8):7*(length_flux_list//8)]-suspension_flux_influ
        self.waveform_superimposed[7*(length_flux_list //8):] = self.waveform[7*(length_flux_list //8):]
        

    def waveform_shift_by_rotor_angle(self, rotor_angle):
        """
        Shift the waveform by a given rotor angle.

        Parameters:
        - rotor_angle: The angle by which to shift the waveform (in degrees).
        """
        total_points = len(self.waveform)
        shift_points = int((rotor_angle / 360) * total_points) % total_points
        self.waveform_shifted = np.roll(self.waveform, shift_points)


    def flux_density_by_suspension_shift(self, suspension_flux_influ=0, rotor_angle=0):


        total_points = len(self.waveform)
        shift_points = int((rotor_angle / 360) * total_points) % total_points

        self.waveform_shifted = np.roll(self.waveform, shift_points)

        length_flux_list = len(self.waveform)

        self.waveform_shift_superimposed[:length_flux_list//8] = self.waveform_shifted[:length_flux_list//8]
        self.waveform_shift_superimposed[length_flux_list//8+1:3*(length_flux_list//8)] = self.waveform_shifted[length_flux_list //8+1:3*(length_flux_list//8)]+suspension_flux_influ
        self.waveform_shift_superimposed[3*(length_flux_list//8)+1:5*(length_flux_list//8)] = self.waveform_shifted[3*(length_flux_list//8)+1:5*(length_flux_list//8)]
        self.waveform_shift_superimposed[5*(length_flux_list//8):7*(length_flux_list//8)] = self.waveform_shifted[5*(length_flux_list//8):7*(length_flux_list//8)]-suspension_flux_influ
        self.waveform_shift_superimposed[7*(length_flux_list //8):] = self.waveform_shifted[7*(length_flux_list //8):]


        # Generate the list
        angle_list = np.linspace(0, 360, total_points)
        if (rotor_angle %90 ==0):
            fig,ax=plt.subplots()
            ax.plot( angle_list, self.waveform, 'b')
            ax.plot( angle_list, self.waveform_shifted, 'r')
            ax.plot( angle_list, self.waveform_shift_superimposed, 'grey')
            ax.set_xlabel("Angle (degrees)")
            ax.set_ylabel("B_air")
            ax.grid(True)
            plt.show()




if __name__ == '__main__':
    # Example usage
    airgap_flux = AirgapFluxDensity()

    # Edit parameters and re-plot
    # airgap_flux.edit_parameters(top_amplitude=0.4, bottom_amplitude=-0.5, flat_top_ratio=0.41, flat_bottom_ratio=0.41,  cycles_number=4)
    airgap_flux.plot_waveform()
    airgap_flux.waveform_shift_by_rotor_angle(30)
    airgap_flux.plot_waveform()

# # Example usage:
# # Create an instance of the waveform
# waveform = AirgapFluxDensity()
# waveform.plot_waveform()

