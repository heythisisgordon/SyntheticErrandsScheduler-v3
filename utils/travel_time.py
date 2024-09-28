from utils.city_map import is_valid_road_location, GRID_SIZE

def get_nearest_road_point(point):
    """
    Find the nearest road point for a given point.
    
    :param point: Tuple (x, y) representing the point
    :return: Tuple (x, y) representing the nearest road point
    """
    x, y = point
    return (round(x / 10) * 10, round(y / 10) * 10)

def calculate_road_travel_time(start, end):
    """
    Calculate the travel time between two points along the city roads.
    Assume 1 grid unit = 1 minute.
    
    :param start: Tuple (x, y) representing the starting point
    :param end: Tuple (x, y) representing the ending point
    :return: Tuple (travel_time, route)
    """
    if start == end:
        return 0, [start]
    
    route = [start]
    
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
    travel_time = sum(abs(p2[0] - p1[0]) + abs(p2[1] - p1[1]) for p1, p2 in zip(route, route[1:]))
    
    return travel_time, route

def calculate_travel_time(start, end):
    """
    Calculate the travel time between two points using the road network.
    
    :param start: Tuple (x, y) representing the starting point
    :param end: Tuple (x, y) representing the ending point
    :return: Tuple (travel_time, route)
    """
    return calculate_road_travel_time(start, end)