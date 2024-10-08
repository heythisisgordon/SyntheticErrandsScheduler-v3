"""
Vehicle Routing Optimizer module for the Synthetic Errands Scheduler

This module contains functions for optimizing the schedule using Google OR-Tools
Vehicle Routing Problem (VRP) solver.
"""

import logging
from typing import Dict, List, Tuple, Optional
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from datetime import datetime, timedelta
from models.schedule import Schedule
from models.customer import Customer
from models.contractor import Contractor
from models.errand import Errand, ErrandType
from utils.travel_time import calculate_travel_time
from utils.errand_utils import get_errand_time, calculate_errand_end_time
from constants import SCHEDULING_DAYS, WORK_START_TIME_OBJ, WORK_END_TIME_OBJ

logger: logging.Logger = logging.getLogger(__name__)

def create_data_model(schedule: Schedule) -> Dict:
    """Creates the data model for the VRP solver."""
    data = {}
    data['num_vehicles'] = len(schedule.contractors)
    data['num_customers'] = len(schedule.customers)
    data['depot'] = 0  # All contractors start from the depot (index 0)
    
    # Combine contractors and customers into a single list of locations
    locations = [contractor.location for contractor in schedule.contractors]
    locations.extend([customer.location for customer in schedule.customers])
    
    # Create distance matrix
    data['distance_matrix'] = []
    for from_loc in locations:
        row = []
        for to_loc in locations:
            travel_time, _ = calculate_travel_time(from_loc, to_loc)
            row.append(int(travel_time.total_seconds() / 60))  # Convert to minutes
        data['distance_matrix'].append(row)
    
    # Time windows (in minutes from start of day)
    start_minutes = WORK_START_TIME_OBJ.hour * 60 + WORK_START_TIME_OBJ.minute
    end_minutes = WORK_END_TIME_OBJ.hour * 60 + WORK_END_TIME_OBJ.minute
    data['time_windows'] = [(start_minutes, end_minutes)] * len(locations)
    
    # Service times (in minutes)
    data['service_times'] = [0] * len(schedule.contractors)  # No service time for contractors
    data['service_times'].extend([int(customer.desired_errand.base_time.total_seconds() / 60) for customer in schedule.customers])
    
    # Contractor calendars
    data['contractor_calendars'] = [contractor.calendar for contractor in schedule.contractors]
    
    logger.debug(f"Data model created: {data}")
    return data

def optimize_schedule_vrp(schedule: Schedule) -> Tuple[Schedule, Schedule]:
    """
    Optimize the given schedule using Google OR-Tools Vehicle Routing solver.
    
    Args:
        schedule (Schedule): The initial schedule to optimize
    
    Returns:
        Tuple[Schedule, Schedule]: The initial schedule and the optimized schedule
    """
    logger.info("Starting VRP optimization")
    try:
        data = create_data_model(schedule)
        logger.info(f"Problem size: {data['num_vehicles']} vehicles, {data['num_customers']} customers")
        
        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                               data['num_vehicles'], data['depot'])
        routing = pywrapcp.RoutingModel(manager)

        def time_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            travel_time = data['distance_matrix'][from_node][to_node]
            service_time = data['service_times'][from_node]
            
            # Check contractor availability
            if from_node < data['num_vehicles']:  # It's a contractor
                contractor_calendar = data['contractor_calendars'][from_node]
                current_time = datetime.now().replace(hour=WORK_START_TIME_OBJ.hour, minute=WORK_START_TIME_OBJ.minute)
                end_time = current_time + timedelta(minutes=travel_time + service_time)
                if not contractor_calendar.is_available(current_time, end_time):
                    return 10000  # Large penalty for unavailable time slots
            
            return travel_time + service_time

        transit_callback_index = routing.RegisterTransitCallback(time_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        time = 'Time'
        routing.AddDimension(
            transit_callback_index,
            60,  # allow waiting time
            data['time_windows'][0][1] - data['time_windows'][0][0],  # maximum time per vehicle
            False,  # Don't force start cumul to zero
            time)
        time_dimension = routing.GetDimensionOrDie(time)

        # Add time window constraints for each location except depot.
        for location_idx, time_window in enumerate(data['time_windows']):
            if location_idx == data['depot']:
                continue
            index = manager.NodeToIndex(location_idx)
            time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])

        # Add time window constraints for each vehicle start node.
        for vehicle_id in range(data['num_vehicles']):
            index = routing.Start(vehicle_id)
            time_dimension.CumulVar(index).SetRange(data['time_windows'][0][0],
                                                    data['time_windows'][0][1])

        # Instantiate route start and end times to produce feasible times.
        for i in range(data['num_vehicles']):
            routing.AddVariableMinimizedByFinalizer(
                time_dimension.CumulVar(routing.Start(i)))
            routing.AddVariableMinimizedByFinalizer(
                time_dimension.CumulVar(routing.End(i)))

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        search_parameters.time_limit.seconds = 60  # 60 seconds time limit

        logger.info("Solving VRP problem")
        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            logger.info("Solution found, building new schedule")
            optimized_schedule = build_schedule_from_solution(schedule, manager, routing, solution, time_dimension)
            return schedule, optimized_schedule
        else:
            logger.warning('No solution found. Returning original schedule.')
            return schedule, schedule
    except Exception as e:
        logger.error(f"Error occurred during VRP optimization: {str(e)}", exc_info=True)
        return schedule, schedule

def build_schedule_from_solution(schedule: Schedule, manager: pywrapcp.RoutingIndexManager, 
                                 routing: pywrapcp.RoutingModel, solution: pywrapcp.Assignment, 
                                 time_dimension: pywrapcp.RoutingDimension) -> Schedule:
    """Builds a new schedule from the VRP solution."""
    new_schedule = Schedule(schedule.contractors.copy(), schedule.customers.copy())

    logger.info("Building optimized schedule:")
    today = datetime.now().replace(hour=WORK_START_TIME_OBJ.hour, minute=WORK_START_TIME_OBJ.minute, second=0, microsecond=0)

    for vehicle_id in range(manager.GetNumberOfVehicles()):
        contractor = schedule.contractors[vehicle_id]
        index = routing.Start(vehicle_id)
        plan_output = f"Route for contractor {contractor.id} (rate: ${contractor.rate:.2f}/min):\n"
        route_distance = 0
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            node = manager.IndexToNode(index)
            if node >= len(schedule.contractors):  # It's a customer
                customer = schedule.customers[node - len(schedule.contractors)]
                start_time = today + timedelta(minutes=solution.Min(time_var))
                end_time = start_time + get_errand_time(customer.desired_errand, contractor.location, customer.location)
                
                if contractor.calendar.is_available(start_time, end_time):
                    errand_id = f"errand_{customer.id}_{contractor.id}_{start_time.strftime('%Y%m%d%H%M')}"
                    if contractor.calendar.reserve_time_slot(errand_id, start_time, end_time):
                        new_schedule.add_assignment(start_time, customer, contractor)
                        plan_output += f" {node} Start: {start_time.time()} -> "
                    else:
                        logger.warning(f"Failed to reserve time slot for customer {customer.id} with contractor {contractor.id} at {start_time}")
                else:
                    logger.warning(f"Contractor {contractor.id} is not available for customer {customer.id} at {start_time}")
            
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)

        time_var = time_dimension.CumulVar(index)
        plan_output += f"{manager.IndexToNode(index)}"
        plan_output += f" Total distance: {route_distance}min\n"
        logger.info(plan_output)

    return new_schedule

def test_vrp_solver():
    """
    A comprehensive test suite for the VRP solver.
    """
    logger.info("Running VRP solver tests")
    
    # Test case 1: Simple case (should succeed)
    contractors = [Contractor(1, (0, 0), 0.5), Contractor(2, (10, 10), 0.6)]
    customers = [
        Customer(1, (5, 5), Errand(1, ErrandType.DELIVERY, timedelta(minutes=30), 1.0, None)),
        Customer(2, (15, 15), Errand(2, ErrandType.DOG_WALK, timedelta(minutes=45), 1.0, None)),
    ]
    test_schedule = Schedule(contractors, customers)
    initial_schedule, optimized_schedule = optimize_schedule_vrp(test_schedule)
    assert optimized_schedule.assignments, "Test case 1 failed: No solution found for simple case"
    logger.info("Test case 1 passed: Solution found for simple case")

    # Test case 2: More complex case (should succeed)
    contractors = [Contractor(i, (i*10, i*10), 0.5 + i*0.1) for i in range(1, 6)]
    customers = [
        Customer(i, (i*5, i*5), Errand(i, ErrandType.DELIVERY, timedelta(minutes=30), 1.0, None))
        for i in range(1, 11)
    ]
    test_schedule = Schedule(contractors, customers)
    initial_schedule, optimized_schedule = optimize_schedule_vrp(test_schedule)
    assert optimized_schedule.assignments, "Test case 2 failed: No solution found for complex case"
    logger.info("Test case 2 passed: Solution found for complex case")

    # Test case 3: Edge case - no customers (should succeed with empty assignments)
    contractors = [Contractor(1, (0, 0), 0.5)]
    customers = []
    test_schedule = Schedule(contractors, customers)
    initial_schedule, optimized_schedule = optimize_schedule_vrp(test_schedule)
    assert optimized_schedule.assignments == {}, "Test case 3 failed: Unexpected assignments for no customers"
    logger.info("Test case 3 passed: Correct handling of no customers")

    # Test case 4: Edge case - no contractors (should return original schedule)
    contractors = []
    customers = [Customer(1, (5, 5), Errand(1, ErrandType.DELIVERY, timedelta(minutes=30), 1.0, None))]
    test_schedule = Schedule(contractors, customers)
    initial_schedule, optimized_schedule = optimize_schedule_vrp(test_schedule)
    assert optimized_schedule == test_schedule, "Test case 4 failed: Unexpected result for no contractors"
    logger.info("Test case 4 passed: Correct handling of no contractors")

    # Test case 5: Large problem (may take longer to solve)
    contractors = [Contractor(i, (i*10, i*10), 0.5 + i*0.05) for i in range(1, 21)]
    customers = [
        Customer(i, (i*5, i*5), Errand(i, ErrandType.DELIVERY, timedelta(minutes=30), 1.0, None))
        for i in range(1, 101)
    ]
    test_schedule = Schedule(contractors, customers)
    initial_schedule, optimized_schedule = optimize_schedule_vrp(test_schedule)
    assert optimized_schedule.assignments, "Test case 5 failed: No solution found for large problem"
    logger.info("Test case 5 passed: Solution found for large problem")

    logger.info("All VRP solver tests passed successfully")