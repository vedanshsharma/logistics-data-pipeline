from pydantic import BaseModel
from typing import Optional, List


class LogisticsEvent(BaseModel):
    BookingID: str
    customerID: str
    Origin_Location: str
    Destination_Location: str
    Current_Location: str
    # Planned_ETA : str
    # some_optional_field: Optional[str] = None #example of optional field.
    _id: Optional[str] = None  # Add the mongo _id here.


class LogisticsEventResponse(BaseModel):
    events: List[LogisticsEvent]
