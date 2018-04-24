"""
Copyright 2018 Bogdan Kulynych

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import time
import statistics as stats

from collections import defaultdict
from functools import wraps

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

    @wraps(func)
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
