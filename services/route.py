"""
    @brief Services module component containing all the basic API routes
    @author oldgod
"""

from os import sep
from uuid import uuid4
from logging import info, debug

from fastapi import FastAPI, Request
from browsers import browsers

from .model import ResponseCode, SessionManager, TestResponse
from .model import test_response
from .utils import read_module_config, update_test_response
# fixme: add the right API for calling the check browser function
#from .mangler import chk_browser

app = FastAPI()
session_mgr = SessionManager()
# setting up the module specific configuration details in the config property
# ignoring the property warning 
session_mgr.config = read_module_config(configpath=f"{__file__[:__file__.rindex(sep)+1]}module.ini") # type: ignore

# root services
@app.get("/")
async def get_root(request: Request):
    '''
        @brief async response function default index
        @param request : fastapi.Request object, automatically taken when this endpoint is hit
        @return returns a Response object containing the necessary details
        @author oldgod
    '''
    info("Welcome to the root URL of TPAS")
    return update_test_response(test_response=test_response, code=ResponseCode.SUCCESS, message='Welcome to TPAS', 
            uuid=session_mgr.uuid, name=session_mgr.name, 
            ip=request.client[0] if request.client else "")

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

    if len(session_mgr.uuid) > 0:
        return update_test_response(test_response=test_response, code=ResponseCode.SUCCESS, message=f"Running Test : {session_mgr.name}", 
                uuid="", name=session_mgr.name, 
                ip=request.client[0] if request.client else "")

    return update_test_response(test_response=test_response, code=ResponseCode.SUCCESS, message="IDLE", 
            uuid="", name=session_mgr.name, 
            ip=request.client[0] if request.client else "")

# utility services
# fixme: the code for this one will be added later
@app.get("/utils/list-browsers")
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
        return update_test_response(test_response=test_response, code=ResponseCode.FAILURE, message="No known browsers installed", 
                uuid="", name=session_mgr.name, ip=request.client[0] if request.client else "")

    lsbrowsers = [browser.get("browser_type") for browser in lsbrowsers]

    # a special formatting for showing the list of browsers installed
    lsbrowsers = ','.join(lsbrowsers)
    debug(f'List of browsers installed : {lsbrowsers}')

    return update_test_response(test_response=test_response, code=ResponseCode.SUCCESS, message=f"List of browsers found : {lsbrowsers}", 
            uuid="", name=session_mgr.name, 
            ip = request.client[0] if request.client else "")

# test session services
@app.get("/test/init-test/name={test_name}")
async def get_init_test(request: Request, test_name: str):
    '''
        @brief async response function for initializing a test session
        @param request : fastapi.Request object, automatically taken when this endpoint is hit
        @return : returns a Response object containing the necessary details
        @author oldgod
    '''
    info("Initializing a test session")
    if len(session_mgr.uuid) != 0 and len(session_mgr.name) != 0:
        # fixme: update the code to return the updated test response
        return update_test_response(test_response=test_response, code=ResponseCode.FAILURE, 
                message="Test could not be initiated, test session already active", 
                uuid="", name=session_mgr.name, ip=request.client[0] if request.client else "")

    # fixme: the uuid value is not getting pushed into the TestResponse object, that needs to be corrected [VVI]
    session_mgr.uuid = str(uuid4())
    debug(f"Session Manager set with UUID : {session_mgr.uuid}")
    session_mgr.name = test_name
    debug(f"Session Manager set with test name : {session_mgr.name}")

    # fixme: add the code for returning the updated test response
    return update_test_response(test_response=test_response, code=ResponseCode.SUCCESS, message=f"Test initiated, name: {session_mgr.name}", 
            uuid=session_mgr.uuid, name=session_mgr.name, 
            ip=request.client[0] if request.client else "")

# fixme: convert this into a POST API call
@app.get("/test/clear-session/uuid={uuid}")
async def get_clear_test_session(request: Request, uuid: str):
    if session_mgr.uuid != uuid:
        return TestResponse(code=ResponseCode.FAILURE, message=f"Invalid Test UUID provided : {uuid}", ip=request.client[0]) # type: ignore

    # if the uuid is matching, then clear the session and the test name
    session_mgr.uuid = str()
    session_mgr.name = str()
    return TestResponse(code=ResponseCode.SUCCESS, message=f"Test session with UUID : {uuid} cleared", ip=request.client[0]) # type: ignore
