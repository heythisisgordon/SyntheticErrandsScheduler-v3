class Contractor:
    def __init__(self, id, location):
        self.id = id
        self.location = location
        self.schedule = {}  # dictionary of day: list of assignments