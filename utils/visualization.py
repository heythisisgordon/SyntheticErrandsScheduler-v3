import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from typing import Union, List, Tuple
import numpy as np
from models.schedule import Schedule
from models.customer import Customer
from models.contractor import Contractor
from models.contractor_calendar import ErrandAssignment
from utils.city_map import GRID_SIZE, create_city_grid
from utils.travel_time import calculate_travel_time
from datetime import date, datetime
import logging

logger = logging.getLogger(__name__)

def visualize_schedule(schedule: Schedule, ax_or_filename: Union[Axes, str, None] = None) -> None:
    """
    Visualize the schedule and city layout.
    
    Args:
        schedule (Schedule): The schedule to visualize
        ax_or_filename (Union[Axes, str, None]): Matplotlib axes to plot on or filename to save the visualization
    """
    city_grid: np.ndarray = create_city_grid()
    
    if ax_or_filename is None or isinstance(ax_or_filename, str):
        fig: Figure
        ax: Axes
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
    contractor_locations: List[Tuple[int, int]] = [contractor.location for contractor in schedule.contractors]
    ax.scatter([loc[0] for loc in contractor_locations], [loc[1] for loc in contractor_locations], 
               color='red', label='Contractors', s=150, marker='s', zorder=3)
    
    # Plot routes using the exact path from calculate_travel_time
    contractor_colors: np.ndarray = plt.cm.Set1(np.linspace(0, 1, len(schedule.contractors)))
    
    # Group assignments by day
    assignments = schedule.get_assignments()
    assignments_by_day = {}
    for errand, customer, contractor in assignments:
        day = errand.travel_start_time.date()
        if day not in assignments_by_day:
            assignments_by_day[day] = []
        assignments_by_day[day].append((errand, customer, contractor))
    
    for day, day_assignments in sorted(assignments_by_day.items()):
        day_str = day.strftime("%Y-%m-%d")
        
        # Sort day_assignments by travel_start_time
        sorted_day_assignments = sorted(day_assignments, key=lambda x: x[0].travel_start_time)
        
        for contractor in schedule.contractors:
            contractor_assignments = [a for a in sorted_day_assignments if a[2].id == contractor.id]
            if not contractor_assignments:
                continue
            
            route: List[Tuple[int, int]] = [contractor.location]
            for _, customer, _ in contractor_assignments:
                route.append(customer.location)
            
            for i in range(len(route) - 1):
                start, end = route[i], route[i+1]
                _, path = calculate_travel_time(start, end)
                
                path_x, path_y = zip(*path)
                offset: float = 0.15  # Add a slight offset to make routes more visible
                ax.plot([x + offset for x in path_x], [y + offset for y in path_y],
                        color=contractor_colors[contractor.id], 
                        alpha=1, linewidth=3, zorder=2,
                        label=f'Contractor {contractor.id+1}, {day_str}' if i == 0 else "")
    
    ax.set_title("Optimized Schedule Visualization")
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.grid(True, alpha=0.3)  # Reduce the opacity of the grid
    
    if isinstance(ax_or_filename, str):
        plt.savefig(ax_or_filename, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        ax.figure.tight_layout()

def print_schedule(schedule: Schedule) -> None:
    """
    Print a detailed view of the schedule.
    
    Args:
        schedule (Schedule): The schedule to print
    """
    print("Synthetic Errands Schedule:")
    print("===========================")
    
    assignments = schedule.get_assignments()
    # Group assignments by day
    assignments_by_day = {}
    for errand, customer, contractor in assignments:
        day = errand.travel_start_time.date()
        if day not in assignments_by_day:
            assignments_by_day[day] = []
        assignments_by_day[day].append((errand, customer, contractor))
    
    for day, day_assignments in sorted(assignments_by_day.items()):
        day_str = day.strftime("%Y-%m-%d")
        
        print(f"\n{day_str}:")
        # Sort day_assignments by travel_start_time
        for errand, customer, contractor in sorted(day_assignments, key=lambda x: x[0].travel_start_time):
            travel_start_str = errand.travel_start_time.strftime("%H:%M")
            travel_end_str = errand.travel_end_time.strftime("%H:%M")
            task_start_str = errand.task_start_time.strftime("%H:%M")
            task_end_str = errand.task_end_time.strftime("%H:%M")
            
            print(f"  Contractor {contractor.id + 1} - Customer {customer.id + 1}:")
            print(f"    Errand: {errand.errand_type}")
            print(f"    Travel Time: {travel_start_str} - {travel_end_str}")
            print(f"    Task Time: {task_start_str} - {task_end_str}")
            print(f"    Location: ({customer.location[0]}, {customer.location[1]})")
            print(f"    Travel Duration: {errand.travel_duration}")
            print(f"    Total Duration: {errand.total_duration}")
    
    print(f"\nTotal Profit: ${schedule.calculate_total_profit():.2f}")
