import matplotlib.pyplot as plt
from models.schedule import Schedule
from utils.city_map import GRID_SIZE, create_city_grid
from utils.travel_time import calculate_travel_time
import numpy as np

def visualize_schedule(schedule: Schedule, ax_or_filename=None):
    """
    Visualize the schedule and city layout.
    
    :param schedule: The schedule to visualize
    :param ax_or_filename: Matplotlib axes to plot on or filename to save the visualization
    """
    city_grid = create_city_grid()
    
    if ax_or_filename is None or isinstance(ax_or_filename, str):
        fig, ax = plt.subplots(figsize=(12, 12))
    else:
        ax = ax_or_filename
    
    ax.imshow(city_grid, cmap='binary')
    
    # Plot customers
    customer_locations = [customer.location for customer in schedule.customers]
    ax.scatter([loc[0] for loc in customer_locations], [loc[1] for loc in customer_locations], 
               color='blue', label='Customers', s=50)
    
    # Plot contractors
    contractor_locations = [contractor.location for contractor in schedule.contractors]
    ax.scatter([loc[0] for loc in contractor_locations], [loc[1] for loc in contractor_locations], 
               color='red', label='Contractors', s=100, marker='s')
    
    # Plot routes using the exact path from calculate_travel_time
    colors = plt.cm.rainbow(np.linspace(0, 1, len(schedule.contractors)))
    for day, assignments in schedule.assignments.items():
        for i, (customer, contractor, _) in enumerate(assignments):
            start = contractor.location if i == 0 else schedule.customers[assignments[i-1][0].id].location
            end = customer.location
            
            _, route = calculate_travel_time(start, end)
            
            # Plot the route
            route_x, route_y = zip(*route)
            ax.plot(route_x, route_y, color=colors[contractor.id], alpha=0.5)
    
    ax.set_title("Synthetic Errands Schedule Visualization")
    ax.legend()
    ax.grid(True)
    
    if isinstance(ax_or_filename, str):
        plt.savefig(ax_or_filename)
        plt.close()

def print_schedule(schedule: Schedule):
    """
    Print a detailed view of the schedule.
    
    :param schedule: The schedule to print
    """
    print("Synthetic Errands Schedule:")
    print("===========================")
    
    for day, assignments in schedule.assignments.items():
        print(f"\nDay {day + 1}:")
        for customer, contractor, start_time in assignments:
            hours, minutes = divmod(start_time, 60)
            print(f"  Contractor {contractor.id + 1} - Customer {customer.id + 1}:")
            print(f"    Errand: {customer.desired_errand.type}")
            print(f"    Start Time: {hours:02d}:{minutes:02d}")
            print(f"    Location: ({customer.location[0]}, {customer.location[1]})")
    
    print(f"\nTotal Profit: ${schedule.calculate_total_profit():.2f}")