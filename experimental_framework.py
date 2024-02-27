import timeit
import matplotlib.pyplot as plt
import random
from chan import chans_algorithm
from graham_display import graham_scan
from jarvis_march import jarvis_march
from data_generation import DataGeneration

class ExperimentalFramework():
    def __init__(self, num_points):
        self.num_points = num_points
        self.x_range = (0,32767) # should we still keep the x_range and y_range parameters in DataGeneration?
        self.y_range = (0,32767)
        self.points = []
        self.graham_scan_times = []
        self.jarvis_march_times = []
        self.chans_algorithm_times = []

    def run_jarvis(self, points):
        return jarvis_march(points, False)
    
    def run_graham(self, points):
        return graham_scan(points, False)
    
    def run_chans(self, points):
        return chans_algorithm(points, False)
    
    def time_algorithms(self, num_points):
        data_gen = DataGeneration(num_points, self.x_range, self.y_range)
        points = data_gen.random_points() # basic case, might need a parameter to choose which type of points to generate

        start = timeit.default_timer()
        self.run_chans(points)
        chans_time = timeit.default_timer() - start

        start = timeit.default_timer()
        self.run_graham(points)
        graham_time = timeit.default_timer() - start

        start = timeit.default_timer()
        self.run_jarvis(points)
        jarvis_time = timeit.default_timer() - start

        return chans_time, graham_time, jarvis_time
    
    def plot_results(self):
        # show the coordinates, but looks messy
        # plt.figure(figsize=(10, 6))
        # for x, y in zip(self.num_points, self.chans_algorithm_times):
        #     plt.annotate(f'({x}, {y:.2f})', (x, y))
        # for x, y in zip(self.num_points, self.graham_scan_times):
        #     plt.annotate(f'({x}, {y:.2f})', (x, y))
        # for x, y in zip(self.num_points, self.jarvis_march_times):
        #     plt.annotate(f'({x}, {y:.2f})', (x, y))
        plt.plot(self.num_points, self.chans_algorithm_times, label='Chan\'s Algorithm')
        plt.plot(self.num_points, self.graham_scan_times, label='Graham\'s Scan')
        plt.plot(self.num_points, self.jarvis_march_times, label='Jarvis\' March')
        plt.xlabel('Number of Points')
        plt.ylabel('Time (seconds)')
        plt.legend()
        plt.show()

    def run_experiments(self):
        for num_points in self.num_points:
            chans_time, graham_time, jarvis_time = self.time_algorithms(num_points)
            self.chans_algorithm_times.append(chans_time)
            self.graham_scan_times.append(graham_time)
            self.jarvis_march_times.append(jarvis_time)
        self.plot_results()

num_points = range(100, 100000, 10000)
framework = ExperimentalFramework(num_points)
framework.run_experiments()