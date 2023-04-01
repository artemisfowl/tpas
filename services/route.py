"""
    @brief Services module component containing all the basic API routes
    @author oldgod
"""

from fastapi import FastAPI

from .model import Response, ResponseCode

app = FastAPI()

@app.get("/")
async def get_root():
    '''
        @brief async response function default index
        @author oldgod
    '''
    return Response(code=ResponseCode.SUCCESS, message="Welcome to TPAS")

@app.get("/status")
async def get_service_status():
    '''
        @brief async response function returning the status of the API(s) running
        @author oldgod
    '''
    return Response(code=ResponseCode.SUCCESS, message="Working")
