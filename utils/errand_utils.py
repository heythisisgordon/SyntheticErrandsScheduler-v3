from utils.travel_time import calculate_travel_time
from constants import DELIVERY_ADDITIONAL_TIME

def calculate_errand_time(errand, start_location, end_location):
    travel_time, _ = calculate_travel_time(start_location, end_location)
    
    if errand.type == "Delivery":
        return travel_time + errand.base_time + DELIVERY_ADDITIONAL_TIME
    elif errand.type == "Outing":
        return errand.base_time  # No travel time for Outing
    else:
        return travel_time + errand.base_time  # Default case for all other errand types