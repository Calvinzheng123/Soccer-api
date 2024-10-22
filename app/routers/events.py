from fastapi import APIRouter, HTTPException
from app.services.sofascore_scrapes import date_query  # Ensure this import is correct
from typing import List

router = APIRouter()

@router.get("/events/", response_model=List[dict])
async def get_events(start_date: str, end_date: str):
    print(f"Received request for events from {start_date} to {end_date}")
    
    try:
        # Fetch data using the date_query function
        events = date_query(start_date, end_date)  # Get a list of events directly

        # Check if events is empty
        if not events:
            raise HTTPException(status_code=404, detail="No events found for the given date range.")

        return events  # Directly return the list of events
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Log the error
        raise HTTPException(status_code=500, detail=str(e))
