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
    
    ax.imshow(city_grid, cmap='binary', alpha=0.2)  # Reduce the opacity of the city grid
    
    # Plot customers with errand numbers
    for i, customer in enumerate(schedule.customers):
        ax.scatter(customer.location[0], customer.location[1], color='blue', s=100, zorder=3)
        ax.annotate(f'{i+1}', (customer.location[0], customer.location[1]), xytext=(3, 3), 
                    textcoords='offset points', color='black', fontsize=8, fontweight='bold')
    
    # Plot contractors
    contractor_locations = [contractor.location for contractor in schedule.contractors]
    ax.scatter([loc[0] for loc in contractor_locations], [loc[1] for loc in contractor_locations], 
               color='red', label='Contractors', s=150, marker='s', zorder=3)
    
    # Plot routes using the exact path from calculate_travel_time
    contractor_colors = plt.cm.Set1(np.linspace(0, 1, len(schedule.contractors)))
    
    for day, assignments in schedule.assignments.items():
        for contractor in schedule.contractors:
            contractor_assignments = [a for a in assignments if a[1].id == contractor.id]
            if not contractor_assignments:
                continue
            
            route = [contractor.location]
            for customer, _, _ in contractor_assignments:
                route.append(customer.location)
            
            for i in range(len(route) - 1):
                start, end = route[i], route[i+1]
                _, path = calculate_travel_time(start, end)
                
                path_x, path_y = zip(*path)
                offset = 0.15  # Add a slight offset to make routes more visible
                ax.plot([x + offset for x in path_x], [y + offset for y in path_y],
                        color=contractor_colors[contractor.id], 
                        alpha=1, linewidth=3, zorder=2,
                        label=f'Contractor {contractor.id+1}, Day {day+1}' if i == 0 else "")
    
    ax.set_title("Optimized Schedule Visualization")
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.grid(True, alpha=0.3)  # Reduce the opacity of the grid
    
    if isinstance(ax_or_filename, str):
        plt.savefig(ax_or_filename, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        ax.figure.tight_layout()

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