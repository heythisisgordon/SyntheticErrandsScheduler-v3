import random
import sys
from models.customer import Customer
from models.contractor import Contractor
from models.errand import Errand
from utils.city_map import is_valid_road_location, GRID_SIZE
from algorithms.initial_scheduler import initial_schedule
from algorithms.optimizer import optimize_schedule, compare_schedules
from utils.visualization import visualize_schedule, print_schedule
from constants import ERRAND_TYPES, DEFAULT_NUM_CUSTOMERS, DEFAULT_NUM_CONTRACTORS, SCHEDULING_DAYS, WORK_START_TIME, WORK_END_TIME

def generate_problem(num_customers=DEFAULT_NUM_CUSTOMERS, num_contractors=DEFAULT_NUM_CONTRACTORS):
    customers = []
    contractors = []

    # Generate customers
    for i in range(num_customers):
        # Generate random valid road location
        while True:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            if is_valid_road_location(x, y):
                break

        # Randomly assign desired errand
        errand_type, base_time, incentive, disincentive = random.choice(ERRAND_TYPES)
        errand = Errand(i, errand_type, base_time, incentive, disincentive)

        # Generate random availability
        availability = {day: list(range(WORK_START_TIME, WORK_END_TIME, 30)) for day in range(SCHEDULING_DAYS)}  # 30-minute slots

        customer = Customer(i, (x, y), errand, availability)
        customers.append(customer)

    # Generate contractors
    for i in range(num_contractors):
        # Generate random valid road location
        while True:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            if is_valid_road_location(x, y):
                break

        contractor = Contractor(i, (x, y))
        contractors.append(contractor)

    return customers, contractors

def cli_main():
    customers, contractors = generate_problem()
    print(f"Generated {len(customers)} customers and {len(contractors)} contractors")

    print("\nCustomer Details:")
    for customer in customers:
        print(f"Customer {customer.id}: Location {customer.location}, Errand: {customer.desired_errand}")

    print("\nContractor Details:")
    for contractor in contractors:
        print(f"Contractor {contractor.id}: Location {contractor.location}")

    initial_sched = initial_schedule(customers, contractors)
    print("\nInitial schedule created")
    print_schedule(initial_sched)
    visualize_schedule(initial_sched, "initial_schedule.png")

    # Print some basic information about the initial schedule
    initial_profit = initial_sched.calculate_total_profit()
    print(f"\nInitial schedule - Profit: ${initial_profit:.2f}")

    # Optimize the schedule
    optimized_sched = optimize_schedule(initial_sched)
    print("\nSchedule optimized")
    print_schedule(optimized_sched)
    visualize_schedule(optimized_sched, "optimized_schedule.png")

    # Print information about the optimized schedule
    optimized_profit = optimized_sched.calculate_total_profit()
    print(f"\nOptimized schedule - Profit: ${optimized_profit:.2f}")

    profit_improvement = optimized_profit - initial_profit
    print(f"Profit improvement: ${profit_improvement:.2f}")

    # Compare the schedules
    compare_schedules(initial_sched, optimized_sched)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        cli_main()
    else:
        try:
            from gui.main_frame import main as gui_main
            gui_main()
        except ImportError:
            print("wxPython is not installed. Running in CLI mode instead.")
            print("To run in GUI mode, please install wxPython: pip install -U wxPython")
            cli_main()