from typing import List, Tuple, Optional, Set, Dict, Any
from datetime import datetime, timedelta
from models.schedule import Schedule
from models.customer import Customer
from models.contractor import Contractor
from models.contractor_calendar import ContractorCalendar
from constants import SCHEDULING_DAYS, WORK_START_TIME_OBJ
from utils.scheduling_utils import calculate_total_time, is_valid_assignment, calculate_profit

class GreedyStepper:
    def __init__(self, customers: List[Customer], contractors: List[Contractor], contractor_calendars: Dict[str, ContractorCalendar]):
        self.customers = customers
        self.contractors = contractors
        self.contractor_calendars = contractor_calendars
        self.schedule = Schedule(contractors, customers)
        self.unscheduled_customers: Set[Customer] = set()
        self.current_date = datetime.now().replace(hour=WORK_START_TIME_OBJ.hour, minute=WORK_START_TIME_OBJ.minute, second=0, microsecond=0)
        self.current_day = 0
        self.current_customer_index = 0
        self.scheduled_customer_ids = set()
        self.step_count = 0
        self.current_method = "initialize"

    def step(self) -> Optional[Dict[str, Any]]:
        self.step_count += 1
        
        if self.current_method == "initialize":
            self.current_method = "check_scheduling_days"
            return self.method_info()

        if self.current_method == "check_scheduling_days":
            if self.current_day >= SCHEDULING_DAYS:
                self.current_method = "log_results"
            else:
                self.current_method = "reset_contractor_locations"
            return self.method_info()

        if self.current_method == "reset_contractor_locations":
            result = self.reset_contractor_locations()
            self.current_method = "check_customer_index"
            return result

        if self.current_method == "check_customer_index":
            if self.current_customer_index >= len(self.customers):
                self.current_day += 1
                self.current_customer_index = 0
                self.current_date += timedelta(days=1)
                self.current_method = "check_scheduling_days"
            else:
                self.current_method = "get_current_customer"
            return self.method_info()

        if self.current_method == "get_current_customer":
            customer = self.customers[self.current_customer_index]
            self.current_customer_index += 1
            self.current_method = "check_customer_scheduled"
            return self.method_info(customer=customer)

        if self.current_method == "check_customer_scheduled":
            customer = self.customers[self.current_customer_index - 1]
            if customer.id not in self.scheduled_customer_ids:
                self.current_method = "find_earliest_valid_slot"
            else:
                self.current_method = "check_customer_index"
            return self.method_info(customer=customer)

        if self.current_method == "find_earliest_valid_slot":
            customer = self.customers[self.current_customer_index - 1]
            result = self.find_earliest_valid_slot(customer)
            self.current_method = "attempt_scheduling"
            return result

        if self.current_method == "attempt_scheduling":
            customer = self.customers[self.current_customer_index - 1]
            result = self.schedule_customer(customer)
            self.current_method = "check_customer_index"
            return result

        if self.current_method == "log_results":
            return self.log_results()

        return None

    def method_info(self, **kwargs) -> Dict[str, Any]:
        return {
            'step_name': self.current_method,
            'variables': {
                'current_day': self.current_day,
                'current_date': self.current_date,
                'current_customer_index': self.current_customer_index,
                'scheduled_customer_ids': self.scheduled_customer_ids,
                **kwargs
            }
        }

    def reset_contractor_locations(self) -> Dict[str, Any]:
        for contractor in self.contractors:
            contractor.reset_location()
        return {
            'step_name': 'reset_contractor_locations',
            'variables': {
                'current_day': self.current_day,
                'current_date': self.current_date,
                'contractor_locations': {c.id: c.location for c in self.contractors}
            }
        }

    def find_earliest_valid_slot(self, customer: Customer) -> Dict[str, Any]:
        earliest_valid_slot = None
        selected_contractor = None
        for contractor in self.contractors:
            total_time = calculate_total_time(contractor, customer, customer.desired_errand)
            potential_slot = self.contractor_calendars[contractor.id].get_next_available_slot(self.current_date, total_time)
            if potential_slot:
                start_time = potential_slot['start']
                end_time = start_time + total_time
                if is_valid_assignment(contractor, customer, start_time, end_time):
                    if earliest_valid_slot is None or start_time < earliest_valid_slot['start']:
                        earliest_valid_slot = potential_slot
                        selected_contractor = contractor
        
        return {
            'step_name': 'find_earliest_valid_slot',
            'variables': {
                'customer_id': customer.id,
                'selected_contractor_id': selected_contractor.id if selected_contractor else None,
                'earliest_valid_slot': earliest_valid_slot
            }
        }

    def schedule_customer(self, customer: Customer) -> Dict[str, Any]:
        valid_slot_info = self.find_earliest_valid_slot(customer)
        selected_contractor_id = valid_slot_info['variables']['selected_contractor_id']
        earliest_valid_slot = valid_slot_info['variables']['earliest_valid_slot']

        if selected_contractor_id and earliest_valid_slot:
            selected_contractor = next(c for c in self.contractors if c.id == selected_contractor_id)
            start_time = earliest_valid_slot['start']
            end_time = start_time + calculate_total_time(selected_contractor, customer, customer.desired_errand)
            
            if self.attempt_scheduling(customer, selected_contractor, start_time, end_time):
                return {
                    'step_name': 'schedule_customer',
                    'variables': {
                        'customer_id': customer.id,
                        'scheduled': True,
                        'contractor_id': selected_contractor.id,
                        'start_time': start_time,
                        'end_time': end_time,
                        'profit': calculate_profit(customer, selected_contractor, start_time, end_time - start_time)
                    }
                }

        self.unscheduled_customers.add(customer)
        return {
            'step_name': 'schedule_customer',
            'variables': {
                'customer_id': customer.id,
                'scheduled': False
            }
        }

    def attempt_scheduling(self, customer: Customer, contractor: Contractor, start_time: datetime, end_time: datetime) -> bool:
        total_time = calculate_total_time(contractor, customer, customer.desired_errand)
        actual_end_time = start_time + total_time
        
        if is_valid_assignment(contractor, customer, start_time, actual_end_time):
            errand_id = f"errand_{customer.id}_{contractor.id}_{start_time.strftime('%Y%m%d%H%M')}"
            if self.contractor_calendars[contractor.id].reserve_time_slot(errand_id, start_time, actual_end_time):
                self.schedule.add_assignment(start_time, customer, contractor)
                contractor.update_location(customer.location)
                self.scheduled_customer_ids.add(customer.id)
                return True
        return False

    def log_results(self) -> Dict[str, Any]:
        total_profit = self.schedule.calculate_total_profit()
        scheduled_count = len(self.customers) - len(self.unscheduled_customers)
        return {
            'step_name': 'log_results',
            'variables': {
                'total_profit': total_profit,
                'scheduled_customers': scheduled_count,
                'unscheduled_customers': len(self.unscheduled_customers),
                'unscheduled_customer_ids': [c.id for c in self.unscheduled_customers]
            }
        }

def greedy_step_through(customers: List[Customer], contractors: List[Contractor], contractor_calendars: Dict[str, ContractorCalendar]) -> GreedyStepper:
    return GreedyStepper(customers, contractors, contractor_calendars)
