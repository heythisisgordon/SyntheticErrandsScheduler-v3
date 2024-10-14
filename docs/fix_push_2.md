To switch your `ContractorCalendar` from the current dictionary-based approach to an **event-based** system (where tasks and availability are represented as intervals), you can focus on restructuring your `calendar`
 attributes to store **intervals** (start time, end time) instead of time slots indexed by specific `datetime` keys. 

Here are some recommendations and a suggested structure for making the transition:

### 1. **Switch from Dict to List of Intervals**
Instead of storing availability slots and errands by specific `datetime` keys, you will store them as **lists of intervals** (each with a start time, end time, and associated task or availability). This will allow for more flexibility when you need to move tasks or check for overlaps.

### 2. **Define an Interval Object**
Create a class to represent an interval. This class will store the start time, end time, and the task or availability it represents.

#### Example of an Interval Class:
```python
class TimeInterval:
    def __init__(self, start_time: datetime, end_time: datetime, task_or_availability):
        self.start_time = start_time
        self.end_time = end_time
        self.task_or_availability = task_or_availability

    def __repr__(self):
        return f"{self.start_time} - {self.end_time}: {self.task_or_availability}"
```

### 3. **Modify `ContractorCalendar` to Use Intervals**
Now, instead of using dictionaries keyed by `datetime`, you'll use **lists of intervals**. This allows for easy sorting, checking for conflicts, and moving tasks around. You’ll track both the contractor’s availability and their errands as lists of `TimeInterval` objects.

#### Updated `ContractorCalendar` Class:
```python
class ContractorCalendar:
    def __init__(self):
        # List of availability intervals
        self.availability: List[TimeInterval] = []
        # List of errand assignments as intervals
        self.errands: List[TimeInterval] = []
        self.start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self._initialize_calendar()

    def _initialize_calendar(self):
        """Initialize contractor availability, for example, starting from the start date."""
        # Example: Define a contractor as available from 9 AM to 5 PM
        day_start = self.start_date.replace(hour=9)
        day_end = self.start_date.replace(hour=17)
        self.availability.append(TimeInterval(day_start, day_end, "Available"))

    def add_errand(self, errand, start_time: datetime, duration: timedelta):
        """Add an errand to the calendar as an interval."""
        end_time = start_time + duration
        errand_interval = TimeInterval(start_time, end_time, errand)
        self.errands.append(errand_interval)
        self._sort_intervals()

    def move_errand(self, errand, new_start_time: datetime, duration: timedelta):
        """Move an existing errand to a new time interval."""
        # Find and remove the old errand
        self.remove_errand(errand)
        # Add the errand at the new time
        self.add_errand(errand, new_start_time, duration)

    def remove_errand(self, errand):
        """Remove an errand from the calendar."""
        self.errands = [interval for interval in self.errands if interval.task_or_availability != errand]

    def _sort_intervals(self):
        """Sort errands and availability by start time for easier management."""
        self.errands.sort(key=lambda x: x.start_time)
        self.availability.sort(key=lambda x: x.start_time)

    def __repr__(self):
        return f"Availability: {self.availability}\nErrands: {self.errands}"
```

### 4. **Handle Time Conflicts**
You can now check for conflicts or overlapping errands more easily by sorting the intervals and checking if any of them overlap.

```python
def has_conflict(self, new_interval: TimeInterval):
    """Check if a new task conflicts with existing errands."""
    for interval in self.errands:
        if not (new_interval.end_time <= interval.start_time or new_interval.start_time >= interval.end_time):
            return True  # Conflict found
    return False
```

### 5. **Advantages of the Event-Based System**
- **Flexibility**: You can now move tasks by adjusting the start and end times of intervals, rather than dealing with specific `datetime` keys.
- **Conflict Handling**: You can easily check for time conflicts by comparing intervals.
- **Sorting and Optimization**: Since the intervals are stored in lists, they can be sorted and manipulated easily to optimize the schedule.
- **Dynamic**: The event-based structure allows you to manage tasks with variable durations and reallocate them to different contractors without modifying dictionary keys.

### Transitioning Your Code
Here are the steps to switch from your current structure:
1. **Replace the `calendar` and `errands` dictionaries** with lists of `TimeInterval` objects.
2. **Convert your `ContractorAvailabilitySlot` and `ErrandAssignment` objects** into something that can fit into the `task_or_availability` attribute of `TimeInterval`. This could involve some refactoring, depending on how detailed those objects are.
3. **Remove the reliance on `datetime` keys**, and instead use the `start_time` and `end_time` attributes of `TimeInterval` to manage task assignment.

### Example Usage:
```python
calendar = ContractorCalendar()
calendar.add_errand("Errand 1", datetime.now().replace(hour=10), timedelta(hours=1))
calendar.add_errand("Errand 2", datetime.now().replace(hour=12), timedelta(hours=2))

# Move Errand 1 to a different time slot
calendar.move_errand("Errand 1", datetime.now().replace(hour=15), timedelta(hours=1))

print(calendar)
```

This event-based approach will give you more flexibility for manipulating and optimizing the schedule, and it’s easier to adapt for advanced scheduling algorithms in the future.