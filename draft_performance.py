import matplotlib.pyplot as plt
import timeit
from chan import chans_algorithm  # Assuming this is where Chan's algorithm is defined
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
                    points = hull + data_gen.generate_points_inside_polygon(hull, n - h)
                    chen_time = self.time_algorithms(points)  # Note: Variable name kept as chen_time for consistency
                    self.results.append((n, h, chen_time))

    def time_algorithms(self, points):
        chen_time = timeit.timeit(lambda: chans_algorithm(points,False), number=1)
        return chen_time

    def plot_results(self):
        n_values, h_values, chen_times = zip(*self.results)  # Renamed jarvis_times to chen_times for clarity

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Color by execution time: normalize and map the execution time to a colormap
        times_normalized = [t / max(chen_times) for t in chen_times]
        colors = plt.cm.jet(times_normalized)

        scatter = ax.scatter(n_values, h_values, chen_times, c=colors, marker='o')

        ax.set_xlabel('N (Number of Points)')
        ax.set_ylabel('H (Hull Size)')
        ax.set_zlabel('Execution Time (seconds)')

        plt.title("Chan's Algorithm Performance")

        plt.show()


# Assuming jarvis_march and DataGeneration are correctly defined and implemented
# Example initialization and method calls (with corrected ranges)
framework = ExperimentalFramework(range(1, 1000, 10), range(3, 100, 3), (0, 32767), (0, 32767))
framework.run_experiment()
framework.plot_results()
