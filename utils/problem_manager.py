from typing import List, Tuple
from models.customer import Customer
from models.contractor import Contractor
from utils.problem_generator import generate_problem

class ProblemManager:
    @staticmethod
    def generate_problem(num_customers: int, num_contractors: int, contractor_rate: float) -> Tuple[List[Customer], List[Contractor]]:
        return generate_problem(num_customers, num_contractors, contractor_rate)
