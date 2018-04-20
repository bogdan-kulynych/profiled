# profiled

A small profiling decorator:

```python
from profiled import profiled, Profiler


@profiled
def do_stuff():
    return 2 + 2


with Profiler() as prof:
    for i in range(1000): do_stuff()        


print(prof.compute_stats())
```
