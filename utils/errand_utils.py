from utils.travel_time import calculate_travel_time

def calculate_errand_time(errand, start_location, end_location):
    travel_time, _ = calculate_travel_time(start_location, end_location)
    
    if errand.type == "Delivery":
        return travel_time + errand.base_time + 10  # Additional 10 minutes for delivery
    elif errand.type == "Dog Walk":
        return travel_time + errand.base_time
    elif errand.type == "Cut Grass":
        return travel_time + errand.base_time
    elif errand.type == "Detail Car":
        return travel_time + errand.base_time
    elif errand.type == "Outing":
        return errand.base_time  # No travel time for Outing
    elif errand.type == "Moving":
        return travel_time + errand.base_time
    else:
        return travel_time + errand.base_time  # Default case