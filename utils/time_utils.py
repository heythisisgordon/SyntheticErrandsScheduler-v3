import datetime
from typing import Union

def convert_minutes_to_time(minutes: int) -> datetime.time:
    """
    Convert minutes since midnight to a datetime.time object.

    Args:
        minutes (int): Number of minutes since midnight.

    Returns:
        datetime.time: Corresponding time object.

    Raises:
        ValueError: If minutes is negative or greater than 1439 (23:59).
    """
    if minutes < 0 or minutes > 1439:
        raise ValueError("Minutes must be between 0 and 1439")
    hours, mins = divmod(minutes, 60)
    return datetime.time(hour=hours, minute=mins)

def is_time_within_range(time: datetime.time, start: datetime.time, end: datetime.time) -> bool:
    """
    Check if a given time is within a specified range.

    Args:
        time (datetime.time): The time to check.
        start (datetime.time): The start of the time range.
        end (datetime.time): The end of the time range.

    Returns:
        bool: True if the time is within the range, False otherwise.
    """
    if start <= end:
        return start <= time <= end
    else:  # Range spans midnight
        return time >= start or time <= end

def get_next_working_day(current_date: datetime.date) -> datetime.date:
    """
    Get the next working day (Monday to Friday) from the given date.

    Args:
        current_date (datetime.date): The current date.

    Returns:
        datetime.date: The next working day.
    """
    next_day = current_date + datetime.timedelta(days=1)
    while next_day.weekday() >= 5:  # Saturday is 5, Sunday is 6
        next_day += datetime.timedelta(days=1)
    return next_day

def calculate_time_difference(start: Union[datetime.datetime, datetime.time], 
                              end: Union[datetime.datetime, datetime.time]) -> datetime.timedelta:
    """
    Calculate the time difference between two datetime or time objects.

    Args:
        start (Union[datetime.datetime, datetime.time]): The start time.
        end (Union[datetime.datetime, datetime.time]): The end time.

    Returns:
        datetime.timedelta: The time difference.

    Raises:
        TypeError: If start and end are not of the same type.
        ValueError: If end is earlier than start for time objects.
    """
    if isinstance(start, datetime.time) and isinstance(end, datetime.time):
        if end < start:
            raise ValueError("End time cannot be earlier than start time for time objects")
        start_datetime = datetime.datetime.combine(datetime.date.today(), start)
        end_datetime = datetime.datetime.combine(datetime.date.today(), end)
        return end_datetime - start_datetime
    elif isinstance(start, datetime.datetime) and isinstance(end, datetime.datetime):
        return end - start
    else:
        raise TypeError("Both start and end must be of the same type (either datetime or time)")