"""
FormattingUtils: Provides utility functions for formatting customer and contractor information.
"""

from typing import List
from models.customer import Customer
from models.contractor import Contractor

class FormattingUtils:
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
