import glob
import pandas as pd
import matplotlib.pyplot as plt

def plot_csv_files():
    # Find all CSV files in the current directory
    csv_files = glob.glob("*.csv")
    
    if not csv_files:
        print("No CSV files found in the current directory.")
        return

    # List to keep track of created figures (optional)
    figures = []

    for file in csv_files:
        print(f"Processing {file}...")
        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file)
        except Exception as e:
            print(f"Error reading {file}: {e}")
            continue

        # Check if the required "Time [ms]" column exists
        if "Time [ms]" not in df.columns:
            print(f"File {file} does not contain a 'Time [ms]' column. Skipping...")
            continue

        # Get x-data from the "Time [ms]" column
        x = df["Time [ms]"]

        # Identify all columns after "Time [ms]" to use as y-data
        time_index = df.columns.get_loc("Time [ms]")
        y_columns = df.columns[time_index+1:]
        
        if len(y_columns) == 0:
            print(f"File {file} does not contain any columns after 'Time [ms]'. Skipping...")
            continue

        # Create a new figure for the current CSV file
        fig, ax = plt.subplots(figsize=(10, 6))
        for col in y_columns:
            y = df[col]
            ax.plot(x, y, marker='o', label=str(col))
        
        # Set plot labels, title, legend, and grid
        ax.set_xlabel("Time [ms]")
        ax.set_ylabel("Values")
        ax.set_title(f"Plot for {file}")
        ax.legend()
        ax.grid(True)
        fig.tight_layout()

        # Append the figure to the list (optional)
        figures.append(fig)
    
    # Show all figures concurrently in separate windows
    plt.show()

if __name__ == "__main__":
    plot_csv_files()
