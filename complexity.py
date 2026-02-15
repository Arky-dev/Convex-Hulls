import time
import numpy as np
import matplotlib.pyplot as plt
import copy
from datasets import DataSet
from hull import SweepingHull, OSHull, GiftWrappingHull

def benchmark_hulls(methods=['Sweeping', 'GiftWrap', 'OS'], distribution='B', max_pow=14, trials=5):
    """
    Benchmarks the execution time of convex hull algorithms averaged over multiple trials.
    
    Args:
        methods: List of algorithms to test.
        distribution: The dataset distribution ('A', 'B', 'C', or 'D').
        max_pow: The max power of 2 for the number of points (2^max_pow).
        trials: Number of times to run each test to average the results.
    """
    sizes = [2**i+1 for i in range(5, max_pow + 1)]
    results = {m: [] for m in methods}

    for n in sizes:
        trial_times = {m: [] for m in methods}

        for t in range(trials):
            ds = DataSet(size=n, method=distribution, seed=-1)
            
            if 'Sweeping' in methods:
                ds_copy = copy.deepcopy(ds) 
                start = time.perf_counter()
                SweepingHull(ds_copy)
                trial_times['Sweeping'].append(time.perf_counter() - start)
                
            if 'OS' in methods:
                ds_copy = copy.deepcopy(ds)
                start = time.perf_counter()
                OSHull(ds_copy)
                trial_times['OS'].append(time.perf_counter() - start)

            if 'GiftWrap' in methods:
                ds_copy = copy.deepcopy(ds)
                start = time.perf_counter()
                GiftWrappingHull(ds_copy)
                trial_times['GiftWrap'].append(time.perf_counter() - start)

        for m in methods:
            results[m].append(np.mean(trial_times[m]))

    plot_results(sizes, results, distribution, trials)

def plot_results(sizes, results, dist_name, trials):
    plt.figure(figsize=(10, 6))
    
    for method, times in results.items():
        plt.plot(sizes, times, 'o-', label=f'Mean Actual: {method}')

    sizes_arr = np.array(sizes)
    
    first_method = list(results.keys())[0]
    n_log_n = sizes_arr * np.log2(sizes_arr)
    scaling_factor = results[first_method][0] / n_log_n[0]
    plt.plot(sizes, n_log_n * scaling_factor, '--', color='gray', alpha=0.5, label='Theoretical Slope O(n log n)')

    plt.xscale('log', base=2)
    plt.yscale('log', base=10)
    plt.xlabel('Number of points (n)')
    plt.ylabel('Time (seconds)')
    plt.title(f'Empirical Complexity (Dist: {dist_name}, Trials: {trials})')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.show()

if __name__ == '__main__':
    benchmark_hulls(methods=['Sweeping', 'OS'], distribution='A', max_pow=18, trials=10)