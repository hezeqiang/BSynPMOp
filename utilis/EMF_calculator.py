import numpy as np

class EMF_Calculator:
    def __init__(self):
        """
        Initializes the EMF_Calculator class.
        """
        pass

    @staticmethod
    def EMF_cal_fluxlinkage(time_list_of_fluxlinkage, timestep):
        """
        Calculates the EMF for one phase based on the derivative of flux linkage.

        Args:
            time_list_of_fluxlinkage (list): List of flux linkage values over time.
            timestep (float): Time step between consecutive flux linkage values.

        Returns:
            list: List of EMF values corresponding to the flux linkage derivative.
        """
        # Ensure the input is valid
        if len(time_list_of_fluxlinkage) < 2:
            raise ValueError("The flux linkage list must contain at least two values.")
        if timestep <= 0:
            raise ValueError("Timestep must be a positive value.")

        # Low-pass filter parameters
        cutoff_frequency = 100000 # Hz
        alpha = timestep / (timestep + 1/ (2*np.pi*cutoff_frequency))

        # Calculate the EMF using the central difference method for interior points
        emf_values = []
        filtered_emf = 0  # Initialize the filter state
        for i in range(len(time_list_of_fluxlinkage) - 1):
            emf = -(time_list_of_fluxlinkage[i + 1] - time_list_of_fluxlinkage[i]) / timestep
            # Apply the low-pass filter
            filtered_emf = alpha * emf + (1 - alpha) * filtered_emf
            emf_values.append(filtered_emf)

        return emf_values



if __name__ == '__main__':
    # Example usage:
    time_list_of_fluxlinkage = [0.1, 0.15, 0.2, 0.25, 0.3]  # Example flux linkage values in Weber-turns
    timestep = 0.01  # Time step in seconds

    calculator = EMF_Calculator()
    emf_values = calculator.EMF_cal_fluxlinkage(time_list_of_fluxlinkage, timestep)
    print("Calculated EMF values:", emf_values)
