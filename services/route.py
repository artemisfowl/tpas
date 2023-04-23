"""
    @brief Services module component containing all the basic API routes
    @author oldgod
"""

from uuid import uuid4
from logging import info, debug

from fastapi import FastAPI, Request

from .model import Response, ResponseCode, SessionManager

app = FastAPI()
session_mgr = SessionManager()

@app.get("/")
async def get_root(request: Request):
    '''
        @brief async response function default index
        @author oldgod
    '''
    info("Welcome to the root URL of TPAS")
    return Response(code=ResponseCode.SUCCESS, message="Welcome to TPAS", ip=request.client[0]) # type: ignore

@app.get("/status")
async def get_service_status(request: Request):
    '''
        @brief async response function returning the status of the API(s) running
        @author oldgod
    '''
    info("Serving status of services")
    debug("Message from status : Working")
    # note: ignoring type check for request.client[0] - NoneType is not subscriptable
    return Response(code=ResponseCode.SUCCESS, message="Working", ip=request.client[0]) # type: ignore

@app.get("/init")
async def init_test(request: Request):
    info("Initializing a test session")
    session_mgr.uuid = str(uuid4())
    debug(f"Service Manager details : {session_mgr.__dict__}")
    return Response(code=ResponseCode.SUCCESS, message="Test initiated", ip=request.client[0]) # type: ignore
