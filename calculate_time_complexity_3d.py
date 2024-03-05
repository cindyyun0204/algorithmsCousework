import matplotlib.pyplot as plt
import math

# Generate ranges for x and y axes
x_range = range(1, 10000, 100)
y_range = range(3, 10000, 100)

# Generating x, y, and z values
x_values = [x for x in x_range for _ in y_range]
y_values = [y for _ in x_range for y in y_range]
# z_values = [x*y for x in x_range for y in y_range]
z_values = [x * math.log(y) for x in x_range for y in y_range]

# # Manually calculating normalized z values for color mapping
# max_z = max(z_values)
# min_z = min(z_values)
# # Normalize z_values to [0, 1] for color mapping
# colors = [(z - min_z) / (max_z - min_z) for z in z_values]

# Color by execution time: normalize and map the execution time to a colormap
times_normalized = [t / max(z_values) for t in z_values]  # Normalize times
colors = plt.cm.jet(times_normalized)  # Map normalized times to colors

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create a scatter plot with colors mapped from z_values
scatter = ax.scatter(x_values, y_values, z_values, c=colors, marker='o')

ax.set_xlabel('N (Number of Points)')
ax.set_ylabel('H (Hull Size)')
ax.set_zlabel('Time Complexity')

# plt.title('Jarvis March Algorithm Time Complexity (O(nh))')
plt.title('Chan\'s Algorithm Time Complexity (O(n log h))')

# # Adding a color bar to indicate the scale of the z_values
# cbar = fig.colorbar(scatter, shrink=0.5, aspect=5)
# cbar.set_label('Performance Metric (normalized)')

plt.show()


