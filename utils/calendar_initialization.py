import logging
from models.contractor_calendar import ContractorCalendar
from typing import List, Dict
from models.contractor import Contractor

logger = logging.getLogger(__name__)

def initialize_calendars(contractors: List[Contractor]) -> Dict[str, ContractorCalendar]:
    """
    Initialize calendars for each contractor.

    Args:
    contractors (List[Contractor]): A list of Contractor objects.

    Returns:
    Dict[str, ContractorCalendar]: A dictionary of contractor IDs to their respective ContractorCalendar instances.
    """
    contractor_calendars = {}

    logger.info(f"Initializing calendars for {len(contractors)} contractors")

    for contractor in contractors:
        contractor_calendars[contractor.id] = ContractorCalendar()
        logger.debug(f"Calendar initialized for contractor {contractor.id}")

    logger.info(f"Calendar initialization completed for {len(contractor_calendars)} contractors")
    return contractor_calendars
