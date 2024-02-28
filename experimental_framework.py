import timeit
import matplotlib.pyplot as plt
from chan import chans_algorithm
from graham_display import graham_scan
from jarvis_march import jarvis_march
from data_generation import DataGeneration

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
                data_gen = DataGeneration(self.x_range, self.y_range)
                points = data_gen.generate_points(n, h)
                chans_time, graham_time, jarvis_time = self.time_algorithms(points)
                self.results.append((n, h, chans_time, graham_time, jarvis_time))

    def time_algorithms(self, points):
        jarvis_time = timeit.timeit(lambda: jarvis_march(points, plot=False), number=1)
        graham_time = timeit.timeit(lambda: graham_scan(points, plot=False), number=1)
        chans_time = timeit.timeit(lambda: chans_algorithm(points, plot=False), number=1)

        return chans_time, graham_time, jarvis_time

    def plot_results(self):
        h_values_set = set(h for _, h, _, _, _ in self.results)
        for h in h_values_set:
            plt.figure(figsize=(10, 6))
            n_values, chans_times, graham_times, jarvis_times = zip(*[(n, ct, gt, jt) for n, h_val, ct, gt, jt in self.results if h_val == h])
            plt.plot(n_values, chans_times, label='Chan\'s Algorithm')
            plt.plot(n_values, graham_times, label='Graham\'s Scan')
            plt.plot(n_values, jarvis_times, label='Jarvis\' March')
            plt.xlabel('Number of Points (n)')
            plt.ylabel('Time (seconds)')
            plt.title(f'h = {h}')
            plt.legend()
        plt.show()

    # def plot_results(self):
    #     n_values, h_values, chans_times, graham_times, jarvis_times = zip(*self.results)
    #     x_values = [f'{n}({h})' for n, h in zip(n_values, h_values)]
    #     # print(x_values, chans_times, graham_times, jarvis_times)
    #     plt.figure(figsize=(10, 6))
    #     plt.plot(x_values, chans_times, label='Chan\'s Algorithm')
    #     plt.plot(x_values, graham_times, label='Graham\'s Scan')
    #     plt.plot(x_values, jarvis_times, label='Jarvis\' March')
    #     plt.xlabel('Number of Points (n) and Hull Points (h) in the form n(h)')
    #     plt.ylabel('Time (seconds)')
    #     plt.legend()
    #     plt.xticks(rotation=90)
    #     plt.tight_layout()
    #     plt.show()

framework = ExperimentalFramework([30000,50000,100000,110000,120000,130000,150000], [10,30,1000], (1, 32767), (1, 32767))
# gonna change into range() eventually
# n_range, h_range, x_range, y_range
framework.run_experiment()
framework.plot_results()