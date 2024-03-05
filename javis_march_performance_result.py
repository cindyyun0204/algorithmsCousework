import matplotlib.pyplot as plt
import timeit
from jarvis_march import jarvis_march
from data_generation_convex_polygon import DataGeneration


class ExperimentalFramework:
    def __init__(self, n_range, h_range, x_range, y_range):
        self.n_range = n_range
        self.h_range = h_range
        self.x_range = x_range
        self.y_range = y_range
        self.results = []

    def run_experiment(self):
        for n in self.n_range:
            for h in self.h_range:
                if n > h:
                    data_gen = DataGeneration(self.x_range, self.y_range)
                    hull = data_gen.generate_random_convex_polygon(h)
                    points = hull + data_gen.generate_points_inside_polygon(hull, n-h)
                    jarvis_time = self.time_algorithms(points)
                    self.results.append((n, h,jarvis_time))

    def time_algorithms(self, points):
        jarvis_time = timeit.timeit(lambda: jarvis_march(points, plot=False), number=1)
        return jarvis_time

    def plot_results(self):
        n_values, h_values, jarvis_times = zip(*self.results)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')  # This enables 3D plotting

        # Color by execution time: normalize and map the execution time to a colormap
        times_normalized = [t / max(jarvis_times) for t in jarvis_times]  # Normalize times
        colors = plt.cm.jet(times_normalized)  # Map normalized times to colors

        # Plotting with color variation
        scatter = ax.scatter(n_values, h_values, jarvis_times, c=colors, marker='o')

        ax.set_xlabel('N (Number of Points)')
        ax.set_ylabel('H (Hull Size)')
        ax.set_zlabel('Execution Time (seconds)')

        plt.title('Jarvis March Algorithm Performance')

        # # Optional: Add a color bar to indicate the scale of execution times
        # cbar = fig.colorbar(scatter, shrink=0.5, aspect=5)
        # cbar.set_label('Execution Time (normalized)')

        plt.show()


# Assuming jarvis_march and DataGeneration are correctly defined and implemented
# Example initialization and method calls (with corrected ranges)
framework = ExperimentalFramework(range(1, 10000, 100), range(3, 2500, 50), (0, 32767), (0, 32767))
framework.run_experiment()
framework.plot_results()

