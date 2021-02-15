"""
dott

Use dott in your code to schedule invoking a function at a given time(s) or
periodically.

dott has just two functions; `hourly` and `daily`.

Here's some examples:

```python
import dott


def say_hello():
    print("hello world")

# Invoke `say_hello` every 2 hours.
dott.hourly(say_hello, 2)

# Invoke 'say_hello` daily at 14:00 and 21:00.
dott.daily(say_hello, ["14:00", "21:00"])
```
"""

from .api import hourly, daily