from datetime import datetime, timedelta

class Errand:
    def __init__(self, id, type, base_time, incentive, disincentive):
        self.id = id
        self.type = type
        self.base_time = base_time
        self.incentive = incentive
        self.disincentive = disincentive
        self.charge = self.calculate_base_charge()

    def calculate_base_charge(self):
        # Different rates for different errand types
        rates = {
            "Delivery": 2,
            "Dog Walk": 1.5,
            "Cut Grass": 2,
            "Detail Car": 2.5,
            "Outing": 3,
            "Moving": 3.5,
            "Grocery Shopping": 1.5  # Added Grocery Shopping
        }
        return self.base_time * rates.get(self.type, 1)  # Default to $1 per minute if type not found

    def apply_incentive(self, scheduled_date, request_date):
        if scheduled_date == request_date.date():
            return self.charge * self.incentive
        return self.charge

    def apply_disincentive(self, scheduled_date, request_date):
        if self.disincentive is None:
            return self.charge

        days_difference = (scheduled_date - request_date.date()).days
        if days_difference <= 14:
            return self.charge

        days_past = days_difference - 14
        if self.disincentive['type'] == 'percentage':
            reduction = min(self.disincentive['value'] * days_past / 100, 1)  # Cap at 100% reduction
            return max(0, self.charge * (1 - reduction))
        elif self.disincentive['type'] == 'fixed':
            return max(0, self.charge - (self.disincentive['value'] * days_past))

    def calculate_final_charge(self, scheduled_date, request_date):
        incentive_charge = self.apply_incentive(scheduled_date, request_date)
        final_charge = self.apply_disincentive(scheduled_date, request_date)
        return max(incentive_charge, final_charge)

    def __str__(self):
        return f"Errand(id={self.id}, type={self.type}, base_time={self.base_time}, charge=${self.charge:.2f})"

    def __repr__(self):
        return self.__str__()