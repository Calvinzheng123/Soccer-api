from fastapi import FastAPI
from LionAPI.routers import events  


app = FastAPI()

app.include_router(events.router)

@app.get("/")
async def root():
    return {"message": "welcome to our soccer data api"}

