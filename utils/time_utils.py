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

def get_next_working_day(current_date: pd.Timestamp) -> pd.Timestamp:
    # Get the next working day (Monday to Friday) from the given date.
    next_day = current_date + pd.Timedelta(days=1)
    while next_day.dayofweek >= 5:  # Saturday is 5, Sunday is 6
        next_day += pd.Timedelta(days=1)
    return next_day

def calculate_time_difference(start: pd.Timestamp, end: pd.Timestamp) -> pd.Timedelta:
    # Calculate the time difference between two Pandas Timestamp objects.
    if end < start:
        raise ValueError("End time cannot be earlier than start time")
    return end - start
