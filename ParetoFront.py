import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Sample Data for Pareto Front (replace with your data)
f1 = np.random.rand(100) * 6
f2 = np.random.rand(100) * 6
f3 = np.random.rand(100) * 6

# Create the 3D figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plotting the Pareto front
ax.scatter(f1, f2, f3, c='blue', label='Pareto front', alpha=0.8)

# Plotting reference points (example points, replace with yours)
ax.scatter(f1 * 0.9, f2 * 0.9, f3 * 0.9, c='orange', label='Reference points', alpha=0.8)

# Labels and legend
ax.set_xlabel('f1')
ax.set_ylabel('f2')
ax.set_zlabel('f3')
ax.set_title('Pareto Front')
ax.legend()

# Show the plot
plt.show()
