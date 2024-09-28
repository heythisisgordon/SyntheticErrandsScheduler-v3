class Contractor:
    def __init__(self, id, location):
        self.id = id
        self.location = location
        self.initial_location = location  # Add this line
        self.schedule = {}  # dictionary of day: list of assignments