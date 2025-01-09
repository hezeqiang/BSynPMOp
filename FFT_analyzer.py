import numpy as np
import matplotlib.pyplot as plt

class FFTAnalyser:
    def __init__(self, data_list, cycle):
        """
        Initialize the FFTAnalyser with the data list and its cycle.

        Parameters:
            data_list (list): List of input data.
            cycle (float): The cycle (duration) of the data in seconds.
        """
        self.data_list = np.array(data_list)
        self.cycle = cycle
        self.sampling_rate = len(data_list) / cycle

    def compute_fft(self):
        """
        Compute the FFT of the data list.

        Returns:
            frequencies (ndarray): The frequencies corresponding to the FFT components.
            amplitude (ndarray): The amplitude of each frequency component.
            phase (ndarray): The phase of each frequency component in radians.
        """
        fft_result = np.fft.fft(self.data_list)
        self.frequencies = np.fft.fftfreq(len(self.data_list), d=1/self.sampling_rate)
        self.amplitude = np.abs(fft_result) / len(self.data_list)
        self.phase = np.angle(fft_result)

        self.positive_freqs = self.frequencies[self.frequencies >= 0]
        self.positive_phase = self.phase[self.frequencies >= 0]
        self.positive_amplitudes = 2 * self.amplitude[self.frequencies >= 0]

        # print(self.positive_freqs)
        # print(self.positive_amplitudes)
        # print(self.positive_phase)

        return self.positive_freqs, self.positive_amplitudes, self.positive_phase

    def plot_frequency_components(self, save_path=None, ax=None):
        """
        Plot each frequency component reconstructed in the time domain, with the same length as the original data list.

        Parameters:
            save_path (str, optional): Path to save the plot as an image file. Defaults to None.
            ax (matplotlib.axes.Axes, optional): Axis to plot on. If None, a new figure is created.
        """
        frequencies, amplitude, phase = self.positive_freqs,self.positive_amplitudes,self.positive_phase
        time = np.linspace(0, self.cycle, len(self.data_list), endpoint=False)

        if ax is None:
            fig, ax = plt.subplots()
        
            ax.plot(time, self.data_list, label="FFT result")

            for i, freq in enumerate(frequencies):
                if freq >= 0:  # Ignore negative frequencies
                    component =  amplitude[i] * np.cos(2 * np.pi * freq * time + phase[i])
                    ax.plot(time, component, label=f"Freq: {freq:.2f} Hz")

            ax.set_title("Frequency Components")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Amplitude")
            ax.legend(loc="upper right", fontsize="small")
            ax.grid()
            plt.show()
            if save_path:
                plt.savefig(save_path)
       

        else:
            ax.plot(time, self.data_list, label="FFT result")

            for i, freq in enumerate(frequencies):
                if freq >= 0:  # Ignore negative frequencies
                    component = amplitude[i] * np.cos(2 * np.pi * freq * time + phase[i])
                    ax.plot(time, component, label=f"Freq: {freq:.2f} Hz")




    def plot_frequency_spectrum(self, save_path=None, ax=None):
        """
        Plot the frequency spectrum (amplitude vs frequency).

        Parameters:
            save_path (str, optional): Path to save the plot as an image file. Defaults to None.
            ax (matplotlib.axes.Axes, optional): Axis to plot on. If None, a new figure is created.
        """

        # Only consider positive frequencies
        positive_freqs = self.positive_freqs
        positive_amplitudes = self.positive_amplitudes

        if ax is None:
            fig, ax = plt.subplots()

            ax.stem(positive_freqs, positive_amplitudes)
            ax.set_title("Frequency Spectrum")
            ax.set_xlabel("Frequency (Hz)")
            ax.set_ylabel("Amplitude")
            ax.grid()

            plt.show()

        else:
            ax.stem(positive_freqs, positive_amplitudes)
            ax.set_title("Frequency Spectrum")
            ax.set_xlabel("Frequency (Hz)")
            ax.set_ylabel("Amplitude")
            ax.grid()

        if save_path:
            plt.savefig(save_path)



    def save_plots(self, components_path, spectrum_path):
        """
        Save both the frequency components plot and the frequency spectrum plot as image files.

        Parameters:
            components_path (str): Path to save the frequency components plot.
            spectrum_path (str): Path to save the frequency spectrum plot.
        """
        self.plot_frequency_components(save_path=components_path)
        self.plot_frequency_spectrum(save_path=spectrum_path)


def generate_cos_list_and_plot(phase, amplitude, n, cycle_nums, Total_time, ax=None):
    """
    Generates a list of n float values for a cosine function and plots the waveform.

    :param phase: Phase of the cosine function (in radians).
    :param amplitude: Amplitude of the cosine function.
    :param n: Number of points in the list.
    :param ax: Optional Matplotlib Axes object for plotting. If None, creates a new subplot.
    :return: List of n float values.
    """
    # Generate equally spaced points between 0 and 2π
    x = np.linspace(0, 2 * np.pi *cycle_nums, n, endpoint=False)
    # Calculate the cosine values with the given phase and amplitude
    cos_values = amplitude * np.cos(x + phase)

    time = np.linspace(0, Total_time, n, endpoint=False)
    
    # # Plot the waveform
    # if ax is None:
    #     fig, ax = plt.subplots()
    #     ax.plot(time, cos_values, label="Cosine Waveform")
    #     ax.set_title("Cosine Waveform")
    #     ax.set_xlabel("x (radians)")
    #     ax.set_ylabel("Amplitude")
    #     ax.grid(True)
    #     ax.legend()
    #     plt.show()
    # else:
    #     ax.plot(time, cos_values, label="Current Waveform")
    #     ax.grid(True)

    return cos_values.tolist()

def generate_cos_list(phase, amplitude, n, cycle_nums, Total_time):
    """
    Generates a list of n float values for a cosine function and plots the waveform.

    :param phase: Phase of the cosine function (in radians).
    :param amplitude: Amplitude of the cosine function.
    :param n: Number of points in the list.
    :param ax: Optional Matplotlib Axes object for plotting. If None, creates a new subplot.
    :return: List of n float values.
    """
    # Generate equally spaced points between 0 and 2π
    x = np.linspace(0, 2 * np.pi *cycle_nums, n, endpoint=False)
    # Calculate the cosine values with the given phase and amplitude
    cos_values = amplitude * np.cos(x + phase)
    
    return cos_values.tolist()




# # Example Usage
if __name__ == '__main__':

    data = [np.sin(2 * np.pi * 4 * t) + 0.5 * np.sin(2 * np.pi * 10 * t) for t in np.linspace(0, 1, 1000)]
    analyser = FFTAnalyser(data, cycle=1)
    analyser.compute_fft()
    analyser.plot_frequency_components()
    analyser.plot_frequency_spectrum()
    # analyser.save_plots("components.png", "spectrum.png")

