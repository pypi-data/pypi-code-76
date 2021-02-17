"""Sample code to test schedule.py."""
from datetime import datetime as dt

from stuy_utils import schedule

DAY = dt.now()

CURRENT_CLASS = schedule.get_current_class(DAY)
NEXT_CLASS = schedule.get_next_class(DAY)


print(f"Inputted Datetime: {DAY}")

if CURRENT_CLASS:
    print("School is in session!")
    print(f"Current Period: {CURRENT_CLASS[0]}")
    print(f"Over In: {CURRENT_CLASS[1].end - DAY}")
else:
    print("School is not in session!")

if NEXT_CLASS:
    print(f"{NEXT_CLASS[0]} will start in: {NEXT_CLASS[1].start - DAY}")
