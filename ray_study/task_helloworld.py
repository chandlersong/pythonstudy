import random

import ray
import time


# A regular Python function.
def normal_function():
    return 1


# By adding the `@ray.remote` decorator, a regular Python function
# becomes a Ray remote function.
@ray.remote
def my_function():
    return 1


# To invoke this remote function, use the `remote` method.
# This will immediately return an object ref (a future) and then create
# a task that will be executed on a worker process.
obj_ref = my_function.remote()

# The result can be retrieved with ``ray.get``.
assert ray.get(obj_ref) == 1


@ray.remote
def slow_function(n):
    time.sleep(random.randint(0, 9))
    print(f"{n} sleep finish")
    return n


object_refs = [slow_function.remote(n) for n in range(10)]
ready_refs, remaining_refs = ray.wait(object_refs, num_returns=2, timeout=None)
for ref in ready_refs:
    print(ray.get(ref))
