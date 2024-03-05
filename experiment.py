import timeit
import matplotlib.pyplot as plt
from chan import chans_algorithm
from graham_display import graham_scan
from jarvis_march import jarvis_march
from data_generation_convex_polygon import DataGeneration

class ExperimentalFramework:
    def __init__(self, n_range, h_range, x_range, y_range, c = True, g = True, j = True):
        self.n_range = n_range
        self.h_range = h_range
        self.x_range = x_range
        self.y_range = y_range
        self.results = []
        self.include_chans = c
        self.include_graham = g
        self.include_jarvis = j

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
        plt.show()
                
    def run_experiment_no_j(self, count=1):
        for n in self.n_range:
            print(n)
            for h in self.h_range:
                data_gen = DataGeneration(self.x_range, self.y_range)
                if h:
                    hull = data_gen.generate_random_convex_polygon(h)
                    points = hull + data_gen.generate_points_inside_polygon(hull, n-h)
                    # points = data_gen.generate_points(n, h)
                else:
                    points = data_gen.generate_random_points(n)
                chans_times, graham_times, jarvis_times = [], [], []
                for _ in range(count):
                    chans_time, graham_time = self.time_algorithms_no_j(points)
                    chans_times.append(chans_time)
                    graham_times.append(graham_time)
                chans_mean = sum(chans_times) / count
                graham_mean = sum(graham_times) / count
                self.results.append((n, h, chans_mean, graham_mean))

    def run_experiment_op_no_j(self, count=1):
        for h in self.h_range:
            print(h)
            for n in self.n_range:
                chans_times, graham_times = [], []
                for _ in range(count):
                    data_gen = DataGeneration(self.x_range, self.y_range)
                    if h:
                        hull = data_gen.generate_random_convex_polygon(h)
                        points = hull + data_gen.generate_points_inside_polygon(hull, n-h)
                        # points = data_gen.generate_points(n, h)
                    else:
                        points = data_gen.generate_random_points(n)
                    chans_time, graham_time = self.time_algorithms_no_j(points)
                    chans_times.append(chans_time)
                    graham_times.append(graham_time)
                    print(chans_time/graham_time)
                chans_mean = sum(chans_times) / count
                graham_mean = sum(graham_times) / count
                self.results.append((n, h, chans_mean, graham_mean))

    # def time_algorithms(self, points):
    #     jarvis_time = timeit.timeit(lambda: jarvis_march(points, plot=False), number=1)
    #     graham_time = timeit.timeit(lambda: graham_scan(points, plot=False), number=1)
    #     chans_time = timeit.timeit(lambda: chans_algorithm(points, plot=False), number=1)
    #     return chans_time, graham_time, jarvis_time
    
    def time_algorithms_no_j(self, points):
        graham_time = timeit.timeit(lambda: graham_scan(points, plot=False), number=1)
        chans_time = timeit.timeit(lambda: chans_algorithm(points, plot=False), number=1)
        return chans_time, graham_time

    def plot_resultss(self):
        h_values_set = set(h for _, h, _, _, _ in self.results)
        for h in h_values_set:
            plt.figure(figsize=(10, 6))
            n_values, chans_times, graham_times, jarvis_times = zip(*[(n, ct, gt, jt) for n, h_val, ct, gt, jt in self.results if h_val == h])
            plt.plot(n_values, chans_times, label='Chan\'s Algorithm')
            plt.scatter(n_values, chans_times, 5, color='black')
            plt.plot(n_values, graham_times, label='Graham Scan')
            plt.scatter(n_values, graham_times, 5, color='black')
            plt.plot(n_values, jarvis_times, label='Jarvis March')
            plt.scatter(n_values, jarvis_times, 5, color='black')
            plt.xlabel('Number of Points (n)')
            plt.ylabel('Time (seconds)')
            plt.title(f'h = {h}')
            plt.legend()
        plt.show()

    def plot_results_no_j(self):
        h_values_set = set(h for _, h, _, _ in self.results)
        for h in h_values_set:
            plt.figure(figsize=(10, 6))
            n_values, chans_times, graham_times = zip(*[(n, ct, gt) for n, h_val, ct, gt in self.results if h_val == h])
            plt.plot(n_values, chans_times, label='Chan\'s Algorithm')
            plt.scatter(n_values, chans_times, 5, color='black')
            plt.plot(n_values, graham_times, label='Graham Scan')
            plt.scatter(n_values, graham_times, 5, color='black')
            plt.xlabel('Number of Points (n)')
            plt.ylabel('Time (seconds)')
            plt.title(f'h = {h}')
            plt.legend()
        plt.show()

    def plot_results_op(self):
        n_values_set = set(n for n, _, _, _, _ in self.results)
        for n in n_values_set:
            plt.figure(figsize=(10, 6))
            h_values, chans_times, graham_times, jarvis_times = zip(*[(h, ct, gt, jt) for n_val, h, ct, gt, jt in self.results if n_val == n])
            plt.plot(h_values, chans_times, label='Chan\'s Algorithm')
            plt.scatter(h_values, chans_times, 5, color='black')
            plt.plot(h_values, graham_times, label='Graham Scan')
            plt.scatter(h_values, graham_times, 5, color='black')
            plt.plot(h_values, jarvis_times, label='Jarvis March')
            plt.scatter(h_values, jarvis_times, 5, color='black')
            plt.xlabel('Number of Hull Points (h)')
            plt.ylabel('Time (seconds)')
            plt.title(f'n = {n}')
            plt.legend()
        plt.show()

    def plot_results_op_no_j(self):
        n_values_set = set(n for n, _, _, _ in self.results)
        for n in n_values_set:
            plt.figure(figsize=(10, 6))
            h_values, chans_times, graham_times = zip(*[(h, ct, gt) for n_val, h, ct, gt in self.results if n_val == n])
            plt.plot(h_values, chans_times, label='Chan\'s Algorithm')
            plt.scatter(h_values, chans_times, 5, color='black')
            plt.plot(h_values, graham_times, label='Graham Scan')
            plt.scatter(h_values, graham_times, 5, color='black')
            plt.xlabel('Number of Hull Points (h)')
            plt.ylabel('Time (seconds)')
            plt.title(f'n = {n}')
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

framework = ExperimentalFramework(range(1000,10000,1000), [50], (0, 30000), (0, 30000)) # 3
# framework = ExperimentalFramework([1000], range(5, 51, 5), (0,30000), (0,30000))
# framework = ExperimentalFramework([10000], range(3,35,1), (0,30000), (0,30000))
# gonna change into range() eventually
# n_range, h_range, x_range, y_range
framework.run_experiment(count = 1)
framework.plot_results()
# framework.run_experiment(count = 1)
# framework.plot_results()
# framework.print_results()