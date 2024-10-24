from fastapi import APIRouter, HTTPException
from LionAPI.services.sofascore_scrapes import date_query
from LionAPI.services.database import insert_event  # Ensure this import is correct
from typing import List

router = APIRouter()

@router.get("/events/", response_model=List[dict])
async def get_events(start_date: str, end_date: str):
    print(f"Received request for events from {start_date} to {end_date}")
    
    try:
        events = date_query(start_date, end_date)  

        if not events:
            raise HTTPException(status_code=404, detail="No events found for the given date range.")

        for event in events:
            insert_event(event)

        return events  
    except Exception as e:
        print(f"Error occurred: {str(e)}")  
        raise HTTPException(status_code=500, detail=str(e))
