"""
    @brief Services module component containing all the basic API routes
    @author sb
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/status")
async def get_service_status():
    return {"status": "Working"}
