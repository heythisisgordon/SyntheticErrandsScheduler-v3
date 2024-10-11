from typing import List, Tuple
from models.customer import Customer
from models.contractor import Contractor
from utils.problem_manager import ProblemManager

class ProblemGenerationController:
    def __init__(self):
        self.problem_manager = ProblemManager()

    def generate_problem(self, num_customers: int, num_contractors: int, contractor_rate: float) -> Tuple[List[Customer], List[Contractor]]:
        return self.problem_manager.generate_problem(num_customers, num_contractors, contractor_rate)

    @staticmethod
    def format_customer_info(customer: Customer) -> List[str]:
        return [
            f"Location: {customer.location}",
            f"Errand: {customer.desired_errand.type.name}",
            f"Base Time: {customer.desired_errand.base_time}",
            f"Charge: ${customer.desired_errand.charge:.2f}"
        ]

    @staticmethod
    def format_contractor_info(contractor: Contractor) -> str:
        return f"Contractor {contractor.id}: Location {contractor.location}"

    @staticmethod
    def format_contractor_rate(rate: float) -> str:
        return f"Contractor Rate: ${rate:.2f} per minute"
