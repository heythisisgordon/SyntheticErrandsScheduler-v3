class Customer:
    def __init__(self, id, location, desired_errand, availability):
        self.id = id
        self.location = location
        self.desired_errand = desired_errand
        self.availability = availability  # dictionary of day: list of available time slots