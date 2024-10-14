Here are step-by-step instructions for refactoring the code to use lists instead of dictionaries for storing schedule information. This refactoring will mainly affect the `Schedule` class and related components. Here are the instructions:

1. Refactor the Schedule class (models/schedule.py):

   a. Change the `assignments` attribute from a dictionary to a list of tuples:
   ```python
   self.assignments: List[Tuple[datetime, Customer, Contractor]] = []
   ```

   b. Update the `add_assignment` method:
   ```python
   def add_assignment(self, start_time: datetime, customer: Customer, contractor: Contractor) -> None:
       self.assignments.append((start_time, customer, contractor))
   ```

   c. Update the `calculate_total_profit` method:
   ```python
   def calculate_total_profit(self) -> float:
       return sum(
           self.calculate_errand_profit(customer, contractor, start_time, i)
           for i, (start_time, customer, contractor) in enumerate(self.assignments)
           if SchedulingUtilities.is_valid_assignment(contractor, customer, start_time, self.get_errand_end_time(customer, contractor, start_time))
       )
   ```

   d. Update the `calculate_errand_profit` method:
   ```python
   def calculate_errand_profit(self, customer: Customer, contractor: Contractor, start_time: datetime, index: int) -> float:
       errand: Errand = customer.desired_errand
       
       prev_location = self.assignments[index-1][1].location if index > 0 else contractor.location
       total_time = SchedulingUtilities.calculate_total_time(contractor, customer, errand)
       
       contractor_cost: float = total_time.total_seconds() / 60 * contractor.rate
       final_charge: float = errand.calculate_final_charge(start_time, datetime.now())

       return final_charge - contractor_cost
   ```

2. Update the GreedyScheduler class (algorithms/initial_greedy_scheduler.py):

   a. Modify the `generate_schedule` method:
   ```python
   def generate_schedule(self) -> Schedule:
       for day in range(SCHEDULING_DAYS):
           self.reset_contractor_locations()
           self.schedule_day(day)
           self.current_date += timedelta(days=1)
       
       self.schedule.assignments.sort(key=lambda x: x[0])  # Sort assignments by start time
       self.log_results()
       return self.schedule
   ```

3. Update the ScheduleFormatter class (utils/schedule_formatter.py):

   a. Modify the `format_schedule` method:
   ```python
   @staticmethod
   def format_schedule(customers: List[Customer], contractors: List[Contractor], schedule: Schedule) -> List[str]:
       formatted_schedule = []
       
       # Group assignments by day
       assignments_by_day = defaultdict(list)
       for start_time, customer, contractor in schedule.assignments:
           day = start_time.date()
           assignments_by_day[day].append((start_time, customer, contractor))
       
       for day, assignments in sorted(assignments_by_day.items()):
           day_str = day.strftime("%Y-%m-%d")
           formatted_schedule.append(f"\n{day_str}:")
           
           for contractor in contractors:
               prev_location = contractor.initial_location
               contractor_assignments = [a for a in assignments if a[2].id == contractor.id]
               
               for start_time, customer, _ in contractor_assignments:
                   # ... (rest of the formatting logic remains the same)
       
       return formatted_schedule
   ```

4. Update the ContractorScheduleFormatter class (utils/contractor_schedule_formatter.py):

   a. Modify the `format_grid` method:
   ```python
   @staticmethod
   def format_grid(schedule: Schedule) -> Tuple[List[str], List[str], List[List[str]], List[List[str]]]:
       contractors = schedule.contractors
       
       # Group assignments by day
       assignments_by_day = defaultdict(list)
       for start_time, customer, contractor in schedule.assignments:
           day = start_time.date()
           assignments_by_day[day].append((start_time, customer, contractor))
       
       days = sorted(assignments_by_day.keys())
       
       # ... (rest of the method remains the same)
       
       # Fill in the grid with errand information
       for day_index, day in enumerate(days):
           assignments = assignments_by_day[day]
           for start_time, customer, contractor in assignments:
               col = contractors.index(contractor)
               start_hour = (start_time - datetime.combine(day, work_start)).total_seconds() / 3600
               start_row = day_index * int(hours_per_day) + int(start_hour)
               
               end_time = schedule.get_errand_end_time(customer, contractor, start_time)
               duration_hours = (end_time - start_time).total_seconds() / 3600
               end_row = start_row + int(duration_hours)
               
               # ... (rest of the grid filling logic remains the same)
       
       return col_labels, row_labels, grid_data, grid_colors
   ```

5. Update the visualization function (utils/visualization.py):

   a. Modify the `visualize_schedule` function:
   ```python
   def visualize_schedule(schedule: Schedule, ax_or_filename: Union[Axes, str, None] = None) -> None:
       # ... (beginning of the function remains the same)
       
       # Group assignments by day
       assignments_by_day = defaultdict(list)
       for start_time, customer, contractor in schedule.assignments:
           day = start_time.date()
           assignments_by_day[day].append((start_time, customer, contractor))
       
       for day, assignments in sorted(assignments_by_day.items()):
           day_str = day.strftime("%Y-%m-%d")
           
           for contractor in schedule.contractors:
               contractor_assignments = [a for a in assignments if a[2].id == contractor.id]
               if not contractor_assignments:
                   continue
               
               route: List[Tuple[int, int]] = [contractor.location]
               for _, customer, _ in contractor_assignments:
                   route.append(customer.location)
               
               # ... (rest of the visualization logic remains the same)
       
       # ... (end of the function remains the same)
   ```

6. Update any other parts of the code that directly access the `schedule.assignments` dictionary. Search for `schedule.assignments` and update the access pattern accordingly.

Review the code logically. Pay special attention to the following areas:
   - Scheduling logic in the GreedyScheduler
   - Profit calculations
   - Schedule formatting and visualization
   - Contractor schedule grid generation

These instructions should guide you through the process of refactoring the code to use lists instead of dictionaries for storing schedule information. Remember to thoroughly investigate the changes to ensure the program continues to function as intended without any errors.