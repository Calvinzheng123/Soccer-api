from fastapi import FastAPI
from app.routers import events  

app = FastAPI()

# Include the events router
app.include_router(events.router)

@app.get("/")
async def root():
    return {"message": "welcome to our soccer data api"}

