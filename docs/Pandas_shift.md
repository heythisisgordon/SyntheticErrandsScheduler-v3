To implement the Pandas-based scheduling logic from the 20241016-MegaScheduler program into the 20241014 Greedy Scheduler, we'll need to make several changes. Here's a detailed outline of the modifications required:

1. Update the Contractor model:
   a. Add a new attribute for the Pandas DataFrame schedule:
      ```python
      import pandas as pd
      from constants import WORK_START_TIME, WORK_END_TIME, TIME_BLOCKS, SIMTIME

      class Contractor:
          def __init__(self, id: int, location: Tuple[int, int], rate: float):
              # ... existing attributes ...
              self.schedule = self.generate_empty_schedule()

          def generate_empty_schedule(self):
              hours, minutes = self.generate_times()
              days = self.generate_days(len(hours))

              schedule = pd.DataFrame({
                  'Day': days,
                  'Hour': hours * SIMTIME,
                  'Minute': minutes * SIMTIME,
                  'Client_ID': [None for _ in range(len(hours) * SIMTIME)]
              })

              schedule.set_index(['Day', 'Hour', 'Minute'], inplace=True)
              return schedule

          def generate_times(self):
              # Implementation from 20241016-MegaScheduler

          def generate_days(self, time):
              # Implementation from 20241016-MegaScheduler
      ```

   b. Modify the ContractorCalendar class to work with the new Pandas DataFrame:
      ```python
      class ContractorCalendar:
          def __init__(self, schedule: pd.DataFrame):
              self.schedule = schedule

          def is_available(self, start_time: datetime, end_time: datetime) -> bool:
              mask = (self.schedule.index.get_level_values('Day') == start_time.date()) & \
                     (self.schedule.index.get_level_values('Hour') >= start_time.hour) & \
                     (self.schedule.index.get_level_values('Hour') < end_time.hour)
              return self.schedule.loc[mask, 'Client_ID'].isnull().all()

          def reserve_time_slot(self, errand_id: str, start_time: datetime, end_time: datetime) -> bool:
              if self.is_available(start_time, end_time):
                  mask = (self.schedule.index.get_level_values('Day') == start_time.date()) & \
                         (self.schedule.index.get_level_values('Hour') >= start_time.hour) & \
                         (self.schedule.index.get_level_values('Hour') < end_time.hour)
                  self.schedule.loc[mask, 'Client_ID'] = errand_id
                  return True
              return False

          def get_next_available_slot(self, start_datetime: datetime, min_duration: timedelta) -> Optional[Dict[str, datetime]]:
              # Implement this method using Pandas operations
      ```

2. Update the SchedulingUtilities class:
   a. Modify the `find_earliest_valid_slot` method to use Pandas operations:
      ```python
      @staticmethod
      def find_earliest_valid_slot(customer: Customer, contractor: Contractor) -> Optional[Tuple[Contractor, datetime, datetime]]:
          total_time = SchedulingUtilities.calculate_total_time(contractor, customer, customer.desired_errand)
          consecutive_blocks = math.ceil(total_time.total_seconds() / (TIME_BLOCKS * 60))

          for day in range(SCHEDULING_DAYS):
              day_schedule = contractor.schedule.loc[day + 1]
              empty_slots = day_schedule[day_schedule['Client_ID'].isnull()]
              
              if len(empty_slots) >= consecutive_blocks:
                  start_slot = empty_slots.iloc[0]
                  start_time = datetime.combine(date.today() + timedelta(days=day), 
                                                time(hour=start_slot.name[0], minute=start_slot.name[1]))
                  end_time = start_time + total_time
                  
                  if SchedulingUtilities.is_valid_assignment(contractor, customer, start_time, end_time):
                      return contractor, start_time, end_time

          return None
      ```

3. Update the Schedule class:
   a. Modify the `add_assignment` method to work with the new Pandas-based contractor schedule:
      ```python
      def add_assignment(self, start_time: datetime, customer: Customer, contractor: Contractor) -> None:
          self.assignments.append((start_time, customer, contractor))
          total_time = SchedulingUtilities.calculate_total_time(contractor, customer, customer.desired_errand)
          end_time = start_time + total_time
          
          mask = (contractor.schedule.index.get_level_values('Day') == start_time.date()) & \
                 (contractor.schedule.index.get_level_values('Hour') >= start_time.hour) & \
                 (contractor.schedule.index.get_level_values('Hour') < end_time.hour)
          contractor.schedule.loc[mask, 'Client_ID'] = customer.id
      ```

4. Update the initial_greedy_scheduler.py:
   a. Modify the `GreedyScheduler` class to use the new Pandas-based logic:
      ```python
      class GreedyScheduler:
          def __init__(self, customers: List[Customer], contractors: List[Contractor]):
              self.customers = customers
              self.contractors = contractors
              self.schedule = Schedule(contractors, customers)
              self.unscheduled_customers: List[Customer] = list(customers)
              self.current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

          def generate_schedule(self) -> Schedule:
              for day in range(SCHEDULING_DAYS):
                  self.reset_contractor_locations()
                  self.schedule_day(day)
                  self.current_date += timedelta(days=1)
              
              self.log_results()
              return self.schedule

          def schedule_day(self, day: int) -> None:
              for customer in self.unscheduled_customers[:]:
                  slot_info = self.find_earliest_valid_slot(customer)
                  if slot_info:
                      contractor, start_time, end_time = slot_info
                      if self.attempt_scheduling(customer, contractor, start_time, end_time):
                          self.unscheduled_customers.remove(customer)

          def find_earliest_valid_slot(self, customer: Customer) -> Optional[Tuple[Contractor, datetime, datetime]]:
              valid_slots = []
              for contractor in self.contractors:
                  slot = SchedulingUtilities.find_earliest_valid_slot(customer, contractor)
                  if slot:
                      valid_slots.append(slot)
              
              return min(valid_slots, key=lambda x: x[1]) if valid_slots else None

          def attempt_scheduling(self, customer: Customer, contractor: Contractor, start_time: datetime, end_time: datetime) -> bool:
              if SchedulingUtilities.is_valid_assignment(contractor, customer, start_time, end_time):
                  self.schedule.add_assignment(start_time, customer, contractor)
                  contractor.update_location(customer.location)
                  return True
              return False
      ```

5. Update the constants.py file:
   a. Add the new constants used in the Pandas-based scheduling:
      ```python
      TIME_BLOCKS = 30  # minutes
      SIMTIME = SCHEDULING_DAYS  # Use the existing SCHEDULING_DAYS constant
      ```

6. Update the problem_generator.py:
   a. Modify the customer generation to include the new availability format:
      ```python
      def _generate_customer(customer_id: int, start_date: datetime) -> Customer:
          return Customer(
              customer_id,
              _generate_valid_location(),
              _generate_random_errand(customer_id),
              _generate_full_day_availability(start_date),
              start_date  # Add this as the request_date
          )

      def _generate_full_day_availability(start_date: datetime) -> List[Tuple[datetime, datetime]]:
          availability = []
          for day in range(SCHEDULING_DAYS):
              current_date = start_date + timedelta(days=day)
              availability.append((
                  datetime.combine(current_date, WORK_START_TIME_OBJ),
                  datetime.combine(current_date, WORK_END_TIME_OBJ)
              ))
          return availability
      ```

7. Update the visualization.py file:
   a. Modify the `visualize_schedule` function to work with the new Pandas-based schedule:
      ```python
      def visualize_schedule(schedule: Schedule, ax_or_filename: Union[Axes, str, None] = None) -> None:
          # ... existing code ...

          for contractor in schedule.contractors:
              assignments = contractor.schedule[contractor.schedule['Client_ID'].notnull()]
              for _, row in assignments.iterrows():
                  customer = next(c for c in schedule.customers if c.id == row['Client_ID'])
                  start_time = datetime.combine(row.name[0], time(hour=row.name[1], minute=row.name[2]))
                  
                  # ... rest of the visualization code ...
      ```

8. Update the main.py file:
   a. Modify the main simulation loop to use the new Pandas-based scheduling:
      ```python
      def main():
          customers, contractors = generate_problem(DEFAULT_NUM_CUSTOMERS, DEFAULT_NUM_CONTRACTORS)
          
          scheduler = GreedyScheduler(customers, contractors)
          schedule = scheduler.generate_schedule()
          
          visualize_schedule(schedule)
          print_schedule(schedule)
      ```

