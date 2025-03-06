from fastapi import APIRouter, HTTPException, Query 
from typing import Optional, List
from api.schemas.logistics import LogisticsEvent, LogisticsEventResponse
from common.mongodb_client import db


router = APIRouter()


@router.get("/events/", response_model=LogisticsEventResponse)
async def get_logistics_events(
    BookingID: Optional[str] = None ,
    customerID: Optional[str] = None ,
    Origin_Location: Optional[str] = None ,
    Destination_Location: Optional[str] = None ,
    Current_Location: Optional[str] = None ,
):
    collection = db["logistics_data"]
    query = {}
    if BookingID is not None:
        query["BookingID"] = BookingID
    if customerID is not None:
        query["customerID"] = customerID
    if Origin_Location is not None:
        query["Origin_Location"] = Origin_Location
    if Destination_Location is not None:
        query["Destination_Location"] = Destination_Location
    if Current_Location is not None:
        query["Current_Location"] = Current_Location
    
    events = list(collection.find(query))
    for event in events:
        event["_id"] = str(event["_id"])

    return LogisticsEventResponse(events=events)


# @router.get("/events/", response_model=LogisticsEventResponse)
# async def get_logistics_event_by_order_id():
#     if not db:
#         raise HTTPException(status_code=500, detail="Database connection failed")
#     collection = db["logistics_data"]
#     events = list(collection.find({"customerID": customerID}))
#     for event in events:
#         event["_id"] = str(event["_id"])
#     if not events:
#         raise HTTPException(status_code=404, detail="Order ID not found")
#     return LogisticsEventResponse(events=events)


@router.get("/events/{customerID}", response_model=LogisticsEventResponse)
async def get_logistics_event_by_order_id(customerID: str):
    if not db:
        raise HTTPException(status_code=500, detail="Database connection failed")
    collection = db["logistics_data"]
    events = list(collection.find({"customerID": customerID}))
    for event in events:
        event["_id"] = str(event["_id"])
    if not events:
        raise HTTPException(status_code=404, detail="Order ID not found")
    return LogisticsEventResponse(events=events)
