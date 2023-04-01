"""
    @brief Services module component containing all the basic API routes
    @author oldgod
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/status")
async def get_service_status():
    '''
        @brief async response function returning the status of the API(s) running
        @author oldgod
    '''
    return {"status": "Working"}
