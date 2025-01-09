import matplotlib.pyplot as plt
import numpy as np

class AirgapFlux:
    def __init__(self, resolution=100, cycles=1):
        self.resolution = resolution
        self.cycles = cycles
        self.waveform = np.sin(np.linspace(0, 2 * np.pi * cycles, resolution * cycles))

    def plot_waveform(self, ax=None):
        """Plot the current waveform."""
        angles = np.linspace(0, 360, self.resolution * self.cycles, endpoint=False)
        if ax is None:
            plt.plot(angles, self.waveform, 'r')
            plt.xlabel("Angle (degrees)")
            plt.ylabel("B_air")
            plt.grid(True)
            plt.show()
        else:
            ax.plot(angles, self.waveform, 'r')
            ax.set_xlabel("Angle (degrees)")
            ax.set_ylabel("B_air")
            ax.grid(True)
            print("Plot waveform")

# Create the figure and subplots
fig, ax = plt.subplots(nrows=2, ncols=2)

# Create an instance of AirgapFlux
Airgap_flux = AirgapFlux()

# Use plot_waveform on one of the subplots
Airgap_flux.plot_waveform(ax[0, 1])

# Add titles to ensure visualization works
ax[0, 0].set_title("Empty Subplot 1")
ax[0, 1].set_title("Waveform Plot")
ax[1, 0].set_title("Empty Subplot 2")
ax[1, 1].set_title("Empty Subplot 3")

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the figure
plt.show()