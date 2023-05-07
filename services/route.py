"""
    @brief Services module component containing all the basic API routes
    @author oldgod
"""

from uuid import uuid4
from logging import info, debug

from fastapi import FastAPI, Request
from browsers import browsers

from .model import Response, ResponseCode, SessionManager, TestResponse
from .constants import DEFAULT_BROWSER

app = FastAPI()
# testme: test this portion of the code
session_mgr = SessionManager()

@app.get("/")
async def get_root(request: Request):
    '''
        @brief async response function default index
        @param request : fastapi.Request object, automatically taken when this endpoint is hit
        @return returns a Response object containing the necessary details
        @author oldgod
    '''
    info("Welcome to the root URL of TPAS")
    return Response(code=ResponseCode.SUCCESS, message="Welcome to TPAS", ip=request.client[0]) # type: ignore

@app.get("/status")
async def get_service_status(request: Request):
    '''
        @brief async response function returning the status of the API(s) running
        @param request : fastapi.Request object, automatically taken when this endpoint is hit
        @return returns a Response object containing the necessary details
        @author oldgod
    '''
    info("Serving status of services")
    debug("Message from status : Working")
    # note: ignoring type check for request.client[0] - NoneType is not subscriptable
    return TestResponse(code=ResponseCode.SUCCESS, message="Working", ip=request.client[0]) # type: ignore

# fixme: the code for this one will be added later
@app.get("/list-browsers")
async def get_installed_browsers(request: Request):
    '''
        @brief async response function returning the list of browsers installed in the system
        @param request : fastapi.Request object, automatically taken when this endpoint is hit
        @return returns a Response object containing the necessary details
        @author oldgod
    '''
    info("Listing the browsers installed in the system")
    lsbrowsers = list(browsers())
    if len(lsbrowsers) == 0:
        return TestResponse(code=ResponseCode.FAILURE, message="No known browsers are installed", ip=request.client[0]) # type: ignore
    lsbrowsers = [browser.get("browser_type") for browser in lsbrowsers]

    # a special formatting for showing the list of browsers installed
    lsbrowsers = ','.join(lsbrowsers)
    debug(f'List of browsers installed : {lsbrowsers}')

    # fixme: add the code to return the proper response in case no browsers are found installed in the system

    return TestResponse(code=ResponseCode.SUCCESS, message=f"List of browsers found : {lsbrowsers}", ip=request.client[0]) # type: ignore

@app.get("/init-test/name={test_name}")
async def get_init_test(request: Request, test_name: str):
    '''
        @brief async response function for initializing a test session
        @param request : fastapi.Request object, automatically taken when this endpoint is hit
        @return : returns a Response object containing the necessary details
        @author oldgod
    '''
    info("Initializing a test session")
    if len(session_mgr.uuid) != 0 and len(session_mgr.name) != 0:
        return TestResponse(code=ResponseCode.FAILURE, 
                message="Test could not be initiated, test session already active", ip=request.client[0]) # type: ignore
    session_mgr.uuid = str(uuid4())
    debug(f"Session Manager set with UUID : {session_mgr.uuid}")
    session_mgr.name = test_name
    debug(f"Session Manager set with test name : {test_name}")

    # fixme: add the code portion of the code for setting up the browser of choice in the session manager
    # fixme: add the code for creating a browser session
    lsbrowsers = list(browsers())
    lsbrowsers = [browser.get("browser_type") for browser in lsbrowsers]
    # check in the configuration file if the browser of choice is configured or not
    if DEFAULT_BROWSER not in lsbrowsers:
        return TestResponse(code=ResponseCode.FAILURE, message="Test initiated, but browser not set", ip=request.client[0]) # type: ignore

    response = TestResponse(code=ResponseCode.SUCCESS, message="Test initiated", ip=request.client[0]) # type: ignore
    response.uuid = session_mgr.uuid
    return response

@app.get("/clear-session/uuid={uuid}")
async def get_clear_test_session(request: Request, uuid: str):
    if session_mgr.uuid != uuid:
        return TestResponse(code=ResponseCode.FAILURE, message=f"Invalid Test UUID provided : {uuid}", ip=request.client[0]) # type: ignore

    # if the uuid is matching, then clear the session and the test name
    session_mgr.uuid = str()
    session_mgr.name = str()
    return TestResponse(code=ResponseCode.SUCCESS, message=f"Test session with UUID : {uuid} cleared", ip=request.client[0]) # type: ignore
