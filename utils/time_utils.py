import pandas as pd
from typing import Union

def convert_minutes_to_time(minutes: int) -> pd.Timestamp:
    # Convert minutes since midnight to a Pandas Timestamp object.
    if minutes < 0 or minutes > 1439:
        raise ValueError("Minutes must be between 0 and 1439")
    return pd.Timestamp(year=1970, month=1, day=1, hour=minutes // 60, minute=minutes % 60)

def is_time_within_range(time: pd.Timestamp, start: pd.Timestamp, end: pd.Timestamp) -> bool:
    # Check if a given time is within a specified range.
    time = time.time()
    start = start.time()
    end = end.time()
    if start <= end:
        return start <= time <= end
    else:  # Range spans midnight
        return time >= start or time <= end