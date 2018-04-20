# profiled

A simple profiling decorator:

```python
In [1]: from profiled import profiled, Profiler

In [2]: @profiled
   ...: def get_answer():
   ...:     return 42
   ...: 

In [3]: profiler = Profiler()

In [4]: with profiler.as_default():
   ...:     for i in range(100000): get_answer()
   ...:     

In [5]: profiler.compute_stats()
Out[5]: 
{'get_answer': {'avg': 2.2763967514038087e-07,
  'max': 0.00016736984252929688,
  'min': 0.0,
  'num': 100000,
  'std': 6.953436521202228e-07,
  'tot': 0.022763967514038086}}
```

That's it.
