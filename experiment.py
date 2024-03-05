import timeit
import matplotlib.pyplot as plt
from chan import chans_algorithm
from graham_display import graham_scan
from jarvis_march import jarvis_march
from data_generation_convex_polygon import DataGeneration

class ExperimentalFramework:
    def __init__(self, n_range, h_range, x_range, y_range, chan = True, graham = True, jarvis = True):
        self.n_range = n_range
        self.h_range = h_range
        self.x_range = x_range
        self.y_range = y_range
        self.results = []
        self.include_chans = chan
        self.include_graham = graham
        self.include_jarvis = jarvis

    def time_algorithms(self, points):
        chans_time, graham_time, jarvis_time = None, None, None
        if self.include_chans:
            chans_time = timeit.timeit(lambda: chans_algorithm(points, plot=False), number=1)
        if self.include_graham:
            graham_time = timeit.timeit(lambda: graham_scan(points, plot=False), number=1)
        if self.include_jarvis:
            jarvis_time = timeit.timeit(lambda: jarvis_march(points, plot=False), number=1)
        return chans_time, graham_time, jarvis_time

    def run_experiment(self, count=1):
        for n in self.n_range:
            print(n)
            for h in self.h_range:
                data_gen = DataGeneration(self.x_range, self.y_range)
                if h:
                    hull = data_gen.generate_random_convex_polygon(h)
                    points = hull + data_gen.generate_points_inside_polygon(hull, n-h)
                else:
                    points = data_gen.generate_random_points(n)
                chans_times, graham_times, jarvis_times = [], [], []
                for _ in range(count):
                    chans_time, graham_time, jarvis_time = self.time_algorithms(points)
                    if self.include_chans:
                        chans_times.append(chans_time)
                    if self.include_graham:
                        graham_times.append(graham_time)
                    if self.include_jarvis:
                        jarvis_times.append(jarvis_time)
                chans_mean = sum(chans_times) / count if self.include_chans else None
                graham_mean = sum(graham_times) / count if self.include_graham else None
                jarvis_mean = sum(jarvis_times) / count if self.include_jarvis else None
                self.results.append((n, h, chans_mean, graham_mean, jarvis_mean))
                if n == h:
                    break

    def plot_results(self):
        h_values_set = set(h for _, h, _, _, _ in self.results)
        for h in h_values_set:
            plt.figure(figsize=(10, 6))
            n_values, chans_times, graham_times, jarvis_times = zip(*[(n, ct, gt, jt) for n, h_val, ct, gt, jt in self.results if h_val == h])
            if self.include_chans:
                plt.plot(n_values, chans_times, label='Chan\'s Algorithm')
                plt.scatter(n_values, chans_times, 5, color='black')
            if self.include_graham:
                plt.plot(n_values, graham_times, label='Graham Scan')
                plt.scatter(n_values, graham_times, 5, color='black')
            if self.include_jarvis:
                plt.plot(n_values, jarvis_times, label='Jarvis March')
                plt.scatter(n_values, jarvis_times, 5, color='black')
            plt.xlabel('Number of Points (n)')
            plt.ylabel('Time (seconds)')
            plt.title(f'h = {h}')
            plt.legend()
            if n_values[0] == h:
                break
        plt.show()

    def plot_results_one_algorithm(self):
        h_values_set = sorted(set(h for _, h, _, _, _ in self.results))
        plt.figure(figsize=(10, 6))
        for h in h_values_set:
            n_values, chans_times, graham_times, jarvis_times = zip(*[(n, ct, gt, jt) for n, h_val, ct, gt, jt in self.results if h_val == h])
            if self.include_graham:
                plt.plot(n_values, graham_times, label=str(h))
                plt.scatter(n_values, graham_times, 5, color='black')
                title = 'Graham Scan'
            if self.include_chans:
                plt.plot(n_values, chans_times, label=str(h))
                plt.scatter(n_values, chans_times, 5, color='black')
                title = 'Chan\'s Algorithm'
            if self.include_jarvis:
                plt.plot(n_values, jarvis_times, label=str(h))
                plt.scatter(n_values, jarvis_times, 5, color='black')
                title = 'Jarvis March'
            plt.xlabel('Number of Points (n)')
            plt.ylabel('Time (seconds)')
            plt.title(title)
            plt.legend()
        plt.show()  

    def print_results(self):
        headers = ["n", "h", "Chan's Algorithm Time", "Graham Scan Time", "Jarvis March Time"]
        data = self.results
        lengths = [max(len(str(val)) for val in col) for col in zip(headers, *data)]
        lengths = [max(len(headers[i]), lengths[i]) for i in range(len(lengths))]
        row_format = "|".join(["{:<" + str(length) + "}" for length in lengths])
        print(row_format.format(*headers))
        for row in data:
            print(row_format.format(*row))
    
# framework = ExperimentalFramework(range(1000,10000,1000), [5], (0, 30000), (0, 30000)) # 3
n = range(1000,5000,1000)
framework = ExperimentalFramework(n,n, (0, 32767), (0, 32767)) # 3
# framework = ExperimentalFramework(range (10000, 26001,5000), [50], (0, 32767), (0, 32767)) # 3
# framework = ExperimentalFramework([50], range(1000,10000,1000), (0, 30000), (0, 30000))
# framework = ExperimentalFramework([1000], range(5, 51, 5), (0,30000), (0,30000))
# framework = ExperimentalFramework([10000], range(3,35,1), (0,30000), (0,30000))
# gonna change into range() eventually
# n_range, h_range, x_range, y_range
framework.run_experiment(count = 1)
framework.plot_results()
# framework.run_experiment(count = 1)
# framework.plot_results()
# framework.print_results()