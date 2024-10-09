Following are some areas of duplicated functionality in the code across the utilities, which you could refactor into reusable utility functions. Once each one is implemented, be sure to examine code related to any changes you make to be sure you're not affecting related files and that your new code is consistent with the program architecture. Implementations should be modular and maintainable.

    Errand Time Calculation:
        File: utils/errand_utils.py and utils/scheduling_utils.py
        Function calculate_total_time in scheduling_utils.py and calculate_total_errand_time in errand_utils.py are essentially duplicating the logic of calculating total errand time by including travel time.
        Recommendation: Merge the time calculation into one utility function that can be used across both modules.

    Time Difference Calculations:
        File: utils/scheduling_utils.py and utils/time_utils.py
        Functions calculate_time_difference in time_utils.py and repeated logic in calculate_profit in scheduling_utils.py perform similar operations.
        Recommendation: Consolidate all time-related calculations, such as calculating the difference between times, into time_utils.py.

    Working Hours Check:
        File: utils/scheduling_utils.py and utils/time_utils.py
        The function is_within_working_hours in scheduling_utils.py uses logic very similar to is_time_within_range in time_utils.py.
        Recommendation: Use a single function from time_utils.py for checking time ranges, ensuring consistency across the codebase.

    Profit Calculation:
        File: utils/scheduling_utils.py
        Function calculate_profit appears in multiple scheduling-related functions and could be centralized into a utility function for profit and cost calculation, improving readability and reusability.

    Errand and Assignment Details:
        File: utils/scheduling_utils.py and other scheduling-related files.
        Functions like get_assignment_details, is_valid_assignment, and others show repeated calculations of travel time, end times, and profit margins.
        Recommendation: Refactor these into a general-purpose utility function for processing errand assignments and computing related values (start time, end time, profit).