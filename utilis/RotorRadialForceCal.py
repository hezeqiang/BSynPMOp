import numpy as np
import matplotlib.pyplot as plt


class RotorRadialForceCalculator:
    def __init__(self, airgap_radius, axial_length):
        """
        Initialize the rotor radial force calculator.

        Parameters:
        - airgap_radius (float): Radius of the airgap (in meters).
        - axial_length (float): Axial length of the rotor (in meters).
        """
        self.airgap_radius = airgap_radius
        self.axial_length = axial_length

    def calculate_radial_force(self, flux_density_list):
        """
        Calculate the radial forces in the x and y directions.

        Parameters:
        - flux_density_list (list or numpy array): List of airgap flux densities (in Tesla).
          The list does not need to have 360 values; it will be interpolated as needed.

        Returns:
        - (float, float): Tuple containing the radial force components (Fx, Fy) in Newtons.
        """
        # Interpolate flux density to 360 values if necessary
        num_points = len(flux_density_list)
        angles = np.linspace(0, 360, num_points, endpoint=False)  # Original angles
        interpolated_angles = np.linspace(0, 360, 360, endpoint=False)  # Target angles

        flux_density = np.interp(interpolated_angles, angles, flux_density_list)

        # Angles in radians
        angles_rad = np.deg2rad(interpolated_angles)

        mu0 = 4 * np.pi * 1e-7

        # Calculate pressure on the surface of the rotor
        magnetic_tensor= (flux_density ** 2) / (2 * mu0)  # Pressure = B^2 / (2 * mu0)

        # Radial forces in x and y directions
        Fx = np.sum(magnetic_tensor * np.cos(angles_rad)) * self.axial_length * self.airgap_radius *2 * np.pi /len(angles_rad)
        Fy = np.sum(magnetic_tensor * np.sin(angles_rad)) * self.axial_length * self.airgap_radius *2 * np.pi /len(angles_rad)

        return Fx, Fy

# Example usage
if __name__ == "__main__":
    # Define airgap radius and axial length
    airgap_radius = 0.1  # meters
    axial_length = 0.2   # meters

    # Example airgap flux density (a sinusoidal distribution as an example)
    flux_density_list = [ -0.2 + 0.4 * np.sin(np.deg2rad(angle)) for angle in  range(0, 4 * 360, 4)]

    fig,ax = plt.subplots()
    ax.plot(range(360),flux_density_list)
    plt.show()


    # Create an instance of the calculator
    calculator = RotorRadialForceCalculator(airgap_radius, axial_length)

    # Calculate the radial forces
    Fx, Fy = calculator.calculate_radial_force(flux_density_list)

    print(f"Radial Force in X-direction: {Fx:.3f} N")
    print(f"Radial Force in Y-direction: {Fy:.3f} N")
