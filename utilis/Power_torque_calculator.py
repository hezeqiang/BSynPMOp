import numpy as np
import matplotlib.pyplot as plt

class ThreePhaseMotorPower:
    def __init__(self, emf_dict, current_dict, mechanical_speed, time_step):
        """
        Initialize the ThreePhaseMotor object.

        Parameters:
        emf_dict (dict): A dictionary where keys are 'A', 'B', 'C', and values are lists of EMF values in time sequence.
        current_dict (dict): A dictionary where keys are 'A', 'B', 'C', and values are lists of current values in time sequence.
        mechanical_speed (float): Mechanical speed of the motor in rad/s.
        time_step (float): Time step of the sequence in seconds.
        """
        self.emf_dict = emf_dict
        self.current_dict = current_dict
        self.mechanical_speed = mechanical_speed
        self.time_step = time_step


    def calculate_instantaneous_power(self):
        """
        Calculate the instantaneous power of the motor.

        Returns:
        np.ndarray: Array of instantaneous power values.
        """
        emf_A = np.array(self.emf_dict['A phase'])
        emf_B = np.array(self.emf_dict['B phase'])
        emf_C = np.array(self.emf_dict['C phase'])

        current_A = np.array(self.current_dict['A phase'])
        current_B = np.array(self.current_dict['B phase'])
        current_C = np.array(self.current_dict['C phase'])

        power_A = emf_A * current_A
        power_B = emf_B * current_B
        power_C = emf_C * current_C

        instantaneous_power = power_A + power_B + power_C
        return instantaneous_power

    def calculate_torque(self):
        """
        Calculate the instantaneous torque of the motor.

        Returns:
        np.ndarray: Array of instantaneous torque values.
        """
        instantaneous_power = self.calculate_instantaneous_power()
        torque = instantaneous_power / self.mechanical_speed
        return torque

    def calculate_power_and_torque(self):
        """
        Calculate both instantaneous power and torque of the motor.

        Returns:
        tuple: Two numpy arrays (power, torque).
        """
        self.instantaneous_power = self.calculate_instantaneous_power()
        self.instantaneous_torque = self.calculate_torque()

        return self.instantaneous_power, self.instantaneous_torque

    def plot_power_and_torque(self, ax=None):
        """
        Plot the instantaneous power and torque.

        Parameters:
        ax (matplotlib.axes.Axes, optional): Axis to plot on. If None, a new figure is created.
        """
        # print(self.instantaneous_power)
        power, torque = self.instantaneous_power, self.instantaneous_torque
        time = np.arange(0, len(power) * self.time_step, self.time_step)

        if ax is None:
            fig, ax = plt.subplots(2, 1, figsize=(10, 6))

            ax[0].plot(time, power, label='Instantaneous Power', color='blue')
            ax[0].set_title('Instantaneous Power')
            ax[0].set_xlabel('Time (s)')
            ax[0].set_ylabel('Power (W)')
            ax[0].grid(True)
            ax[0].legend()

            ax[1].plot(time, torque, label='Instantaneous Torque', color='green')
            ax[1].set_title('Instantaneous Torque')
            ax[1].set_xlabel('Time (s)')
            ax[1].set_ylabel('Torque (Nm)')
            ax[1].grid(True)
            ax[1].legend()
            plt.tight_layout()
            plt.show()
        else:
            ax[0].plot(time, power, label='Instantaneous Power', color='blue')
            ax[0].set_title('Instantaneous Power')
            ax[0].set_xlabel('Time (s)')
            ax[0].set_ylabel('Power (W)')
            ax[0].grid(True)
            ax[0].legend()

            ax[1].plot(time, torque, label='Instantaneous Torque', color='green')
            ax[1].set_title('Instantaneous Torque')
            ax[1].set_xlabel('Time (s)')
            ax[1].set_ylabel('Torque (Nm)')
            ax[1].grid(True)
            ax[1].legend()
            plt.tight_layout()


# Example Usage:


if __name__ == '__main__':
     
    emf = {
    'A': [1.0, 2.0, 3.0, 4.0],
    'B': [0.5, 1.5, 2.5, 3.5],
    'C': [0.3, 1.3, 2.3, 3.3]
    }

    current = {
    'A': [0.1, 0.2, 0.3, 0.4],
    'B': [0.05, 0.15, 0.25, 0.35],
    'C': [0.03, 0.13, 0.23, 0.33]
    } 

    mechanical_speed = 10.0  # rad/s
    time_step = 0.01  # seconds

    motor = ThreePhaseMotorPower(emf, current, mechanical_speed, time_step)
    power, torque = motor.calculate_power_and_torque()

    print("Instantaneous Power:", power)
    print("Instantaneous Torque:", torque)
