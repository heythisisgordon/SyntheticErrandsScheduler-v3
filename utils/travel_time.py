from typing import Tuple, List
from datetime import timedelta
from utils.city_map import is_valid_road_location, GRID_SIZE
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_nearest_road_point(point: Tuple[int, int]) -> Tuple[int, int]:
    """
    Find the nearest road point for a given point.
    
    :param point: Tuple[int, int] representing the point
    :return: Tuple[int, int] representing the nearest road point
    """
    x, y = point
    return (round(x / 10) * 10, round(y / 10) * 10)

@lru_cache(maxsize=10000)
def calculate_road_travel_time(start: Tuple[int, int], end: Tuple[int, int]) -> Tuple[timedelta, Tuple[Tuple[int, int], ...]]:
    """
    Calculate the travel time between two points along the city roads.
    Assume 1 grid unit = 1 minute.
    
    :param start: Tuple[int, int] representing the starting point
    :param end: Tuple[int, int] representing the ending point
    :return: Tuple[timedelta, Tuple[Tuple[int, int], ...]] representing (travel_time, route)
    """
    if start == end:
        return timedelta(), (start,)
    
    route: List[Tuple[int, int]] = [start]
    
    # Find nearest road points
    start_road = get_nearest_road_point(start)
    end_road = get_nearest_road_point(end)
    
    # Add start road point if it's different from start
    if start != start_road:
        route.append(start_road)
    
    # Add intermediate road points
    if start_road != end_road:
        route.append((end_road[0], start_road[1]))
    
    # Add end road point if it's different from end
    if end_road not in route:
        route.append(end_road)
    
    # Add end point if it's different from end road point
    if end != end_road:
        route.append(end)
    
    # Calculate total travel time
    travel_time_minutes = sum(abs(p2[0] - p1[0]) + abs(p2[1] - p1[1]) for p1, p2 in zip(route, route[1:]))
    
    return timedelta(minutes=travel_time_minutes), tuple(route)

def calculate_travel_time(start: Tuple[int, int], end: Tuple[int, int]) -> Tuple[timedelta, List[Tuple[int, int]]]:
    """
    Calculate the travel time between two points using the road network.
    
    :param start: Tuple[int, int] representing the starting point
    :param end: Tuple[int, int] representing the ending point
    :return: Tuple[timedelta, List[Tuple[int, int]]] representing (travel_time, route)
    """
    travel_time, route_tuple = calculate_road_travel_time(start, end)
    return travel_time, list(route_tuple)

# Clear the cache when the module is reloaded (useful for testing and development)
calculate_road_travel_time.cache_clear()
get_nearest_road_point.cache_clear()