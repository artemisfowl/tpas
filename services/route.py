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
async def get_root(request: Request) -> Response:
    '''
        @brief async response function default index
        @param request : fastapi.Request object, automatically taken when this endpoint is hit
        @return returns a Response object containing the necessary details
        @author oldgod
    '''
    info("Welcome to the root URL of TPAS")
    return Response(code=ResponseCode.SUCCESS, message="Welcome to TPAS", ip=request.client[0]) # type: ignore

@app.get("/status")
async def get_service_status(request: Request) -> Response:
    '''
        @brief async response function returning the status of the API(s) running
        @param request : fastapi.Request object, automatically taken when this endpoint is hit
        @return returns a Response object containing the necessary details
        @author oldgod
    '''
    info("Serving status of services")
    debug("Message from status : Working")
    # note: ignoring type check for request.client[0] - NoneType is not subscriptable
    return Response(code=ResponseCode.SUCCESS, message="Working", ip=request.client[0]) # type: ignore

@app.get("/browsers")
async def get_installed_browsers(request: Request) -> Response:
    '''
        @brief async response function returning the list of browsers installed in the system
        @param request : fastapi.Request object, automatically taken when this endpoint is hit
        @return returns a Response object containing the necessary details
        @author oldgod
    '''
    # note: there is a module called pybrowsers - but I wish to write a custom implementation - this will require some 
    # time for implementing the same thing but with a code twisted for me - need to decide on the core logic 
    # implementation as well.

    # fixme: Add the code for finding the browsers installed on the system
    # note: this code should be working in all types of systems
    return Response(code=ResponseCode.SUCCESS, message="List of browsers found", ip=request.client[0]) # type: ignore

@app.get("/init/name={test_name}")
async def get_init_test(request: Request, test_name: str) -> Response:
    '''
        @brief async response function for initializing a test session
        @param request : fastapi.Request object, automatically taken when this endpoint is hit
        @return : returns a Response object containing the necessary details
        @author oldgod
    '''
    info("Initializing a test session")
    session_mgr.uuid = str(uuid4())
    debug(f"Session Manager set with UUID : {session_mgr.uuid}")
    session_mgr.name = test_name
    debug(f"Session Manager set with test name : {test_name}")

    # fixme: return the uuid created which will be used to allow for the next steps to be done on the machine
    # fixme: replace response with a derived class providing more details - maybe can be named as TestDetails
    return Response(code=ResponseCode.SUCCESS, message="Test initiated", ip=request.client[0]) # type: ignore
