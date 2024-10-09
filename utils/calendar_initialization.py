from models.contractor_calendar import ContractorCalendar
from models.master_contractor_calendar import MasterContractorCalendar
from typing import List
from models.contractor import Contractor

def initialize_calendars(contractors: List[Contractor]) -> MasterContractorCalendar:
    """
    Initialize calendars for each contractor and create a master calendar.

    Args:
    contractors (List[Contractor]): A list of Contractor objects.

    Returns:
    MasterContractorCalendar: The initialized master calendar containing all contractor calendars.
    """
    master_calendar = MasterContractorCalendar()

    for contractor in contractors:
        contractor_calendar = ContractorCalendar()
        master_calendar.add_contractor_calendar(contractor.id, contractor_calendar)

    return master_calendar