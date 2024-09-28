# Same-day incentives for each errand type
DELIVERY_INCENTIVE = 1.2
DOG_WALK_INCENTIVE = 1.1
CUT_GRASS_INCENTIVE = 1.3
DETAIL_CAR_INCENTIVE = 1.2
OUTING_INCENTIVE = 1.05
MOVING_INCENTIVE = 1.5

# Maximum incentive multiplier
MAX_INCENTIVE_MULTIPLIER = 1.5

# Errand types with their characteristics
ERRAND_TYPES = [
    ("Delivery", 10, DELIVERY_INCENTIVE, {"type": "percentage", "value": 25, "days": 14}),
    ("Dog Walk", 20, DOG_WALK_INCENTIVE, None),
    ("Cut Grass", 10, CUT_GRASS_INCENTIVE, None),
    ("Detail Car", 15, DETAIL_CAR_INCENTIVE, {"type": "percentage", "value": 10, "days": 14}),
    ("Outing", 15, OUTING_INCENTIVE, {"type": "percentage", "value": 10, "days": 14}),
    ("Moving", 120, MOVING_INCENTIVE, {"type": "fixed", "value": 300, "days": 14})
]

# Errand rates ($ per minute)
ERRAND_RATES = {
    "Delivery": 2,
    "Dog Walk": 1.5,
    "Cut Grass": 2,
    "Detail Car": 2.5,
    "Outing": 3,
    "Moving": 3.5,
    "Grocery Shopping": 1.5
}

# Additional time for specific errand types (in minutes)
DELIVERY_ADDITIONAL_TIME = 10

# Working hours
WORK_START_TIME = 480  # 8:00 AM in minutes
WORK_END_TIME = 1020  # 5:00 PM in minutes

# Default problem generation parameters
DEFAULT_NUM_CUSTOMERS = 10
DEFAULT_NUM_CONTRACTORS = 2

# Scheduling period
SCHEDULING_DAYS = 14