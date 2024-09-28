from datetime import datetime, timedelta
from constants import MAX_INCENTIVE_MULTIPLIER, ERRAND_RATES, SCHEDULING_DAYS

class Errand:
    def __init__(self, id, type, base_time, incentive, disincentive):
        self.id = id
        self.type = type
        self.base_time = base_time
        self.incentive = incentive
        self.disincentive = disincentive
        self.charge = self.calculate_base_charge()

    def calculate_base_charge(self):
        return self.base_time * ERRAND_RATES.get(self.type, 1)  # Default to $1 per minute if type not found

    def apply_incentive(self, scheduled_date, request_date):
        if scheduled_date == request_date.date():
            incentive_charge = self.charge * self.incentive
            return min(incentive_charge, self.charge * MAX_INCENTIVE_MULTIPLIER)
        return self.charge

    def apply_disincentive(self, scheduled_date, request_date):
        if self.disincentive is None:
            return self.charge

        days_difference = (scheduled_date - request_date.date()).days
        if days_difference <= SCHEDULING_DAYS:
            return self.charge

        days_past = days_difference - SCHEDULING_DAYS
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