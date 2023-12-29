import time
import statistics as stats

from collections import defaultdict
from functools import wraps


class Profiler:
    """Profiling context.

    Example ::

        profiler = Profiler()
        with profiler:
            do_stuff()   # (1)

        do_stuff()       # (2)
        profiler.compute_stats()

    This will show profiling stats for line (1), but not (2),
    because line 2 is not executed in the context.
    """

    _default_instance = None

    @staticmethod
    def get_default():
        return Profiler._default_instance

    def __init__(self):
        self.reset()

    def reset(self):
        self.data = defaultdict(list)

    def compute_stats(self):
        result = {}
        for func_name, data_points in self.data.items():
            result[func_name] = {
                "avg": stats.mean(data_points),
                "min": min(data_points),
                "max": max(data_points),
                "num": len(data_points),
                "tot": sum(data_points),
            }
            if len(data_points) >= 2:
                result[func_name]["std"] = stats.stdev(data_points)
        return result

    def __enter__(self):
        Profiler._default_instance = self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Profiler._default_instance = None


def get_func_id(func):
    """Get a quasi-identifier of a given function."""
    return func.__qualname__


def profiled(func):
    """Profiling decorator."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        profiler = Profiler.get_default()
        if profiler is None:
            return func(*args, **kwargs)

        t0 = time.time()
        result = func(*args, **kwargs)
        t1 = time.time()
        profiler.data[get_func_id(func)].append(t1 - t0)
        return result

    return wrapped
