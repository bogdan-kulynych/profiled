import time
import statistics as stats

from collections import defaultdict

from defaultcontext import with_default_context


@with_default_context
class Profiler(object):
    """Profiling context.

    Example ::

        profiler = Profiler()
        with profiler.as_default():
            do_stuff()   # (1)

        do_stuff()       # (2)
        profiler.compute_stats()

    This will show profiling stats for line (1), but not (2),
    because line 2 is not executed in the context.
    """
    def __init__(self):
        self.data = defaultdict(list)

    def compute_stats(self):
        result = {}
        for func_name, data_points in self.data.items():
            result[func_name] = {
                'avg': stats.mean(data_points),
                'min': min(data_points),
                'max': max(data_points),
                'num': len(data_points),
                'tot': sum(data_points),
            }
            if len(data_points) >= 2:
                result[func_name]['std'] = stats.stdev(data_points)
        return result


def profiled(func):
    """Profiling decorator."""

    def wrapped(*args, **kwargs):
        profiler = Profiler.get_default()
        if profiler is None:
            return func(*args, **kwargs)

        t0 = time.time()
        result = func(*args, **kwargs)
        t1 = time.time()
        profiler.data[func.__name__].append(t1 - t0)
        return result

    return wrapped
