"""
    @brief Services module component containing all the basic API routes
    @author oldgod
"""

from os import sep, makedirs
from uuid import uuid4
from logging import info, debug, warn

from fastapi import FastAPI, Request
from browsers import browsers

from .model import ResponseCode, SessionManager
from .model import test_response
from .model import AdminRequest, InitTestRequest, EndTestRequest
from .constants import DEFAULT_ADMIN_PASSWORD, DEFAULT_ADMIN_USER, DEFAULT_DRIVER_BINARY
from .constants import TestType
from .utils import read_module_config, update_test_response

# fixme: add the right API for calling the check browser function
from .mangler import create_ui_test_session_resources

app = FastAPI()
session_mgr = SessionManager()
# setting up the module specific configuration details in the config property
# ignoring the property warning 
session_mgr.config = read_module_config(configpath=f"{__file__[:__file__.rindex(sep)+1]}module.ini") # type: ignore

# create the web UI default browser driver binary path at runtime
g_module_directory_path = __file__[:__file__.rfind(__name__[:__name__.find('.')])]
if not g_module_directory_path.endswith(sep):
    g_module_directory_path += sep
g_final_driver_location = f"{g_module_directory_path}{DEFAULT_DRIVER_BINARY}"
debug(f"Creating driver binary directory path : {g_final_driver_location[:g_final_driver_location.rfind(sep)]}")
makedirs(g_final_driver_location[:g_final_driver_location.rfind(sep)], exist_ok=True)

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

# admin services { will be added here later }
@app.post("/admin/clearall")
async def post_clear_all_sessions(request: Request, test_request: AdminRequest):
    info("Admin being called in order to clear all test sessions")
    debug(f"Admin credentials provided : user -> {test_request.admin_user} and password -> {test_request.admin_password}")
    debug(f"Clearing of all sessions requested from : {request.client[0] if request.client else 'Unidentified'}")

    if test_request.admin_user == DEFAULT_ADMIN_USER:
        if test_request.admin_password == DEFAULT_ADMIN_PASSWORD:
            session_mgr.uuid = ""
            session_mgr.name = ""

            debug("Test session clear succesful, returning the updated response")
            return update_test_response(test_response=test_response, code=ResponseCode.SUCCESS, 
                    message="Test session invalidated", 
                    uuid="", name="", ip=request.client[0] if request.client else "")
        else:
            warn("Admin user is not recognized, username/password might be incorrect")
            return update_test_response(test_response=test_response, code=ResponseCode.FAILURE, 
                    message="Admin username and password not matching",
                    uuid="", name=session_mgr.name, ip=request.client[0] if request.client else "")
    else:
        warn("Admin user is not recognized, username/password might be incorrect")
        update_test_response(test_response=test_response, code=ResponseCode.FAILURE, 
                message="Admin username and password not matching",
                uuid="", name=session_mgr.name, ip=request.client[0] if request.client else "")

# utility services
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
    debug(f"Entire information of lsbrowsers: {lsbrowsers}")
    lbrowsers = []

    for browser in lsbrowsers:
        tmp = {}
        tmp['browser_type'] = browser.get('browser_type')
        tmp['install_path'] = browser.get('path').split()[-1]
        tmp["version"] = browser.get("version")
        debug(f"tmp data : {tmp}")
        lbrowsers.append(tmp)

    if len(lsbrowsers) == 0:
        warn("No known browsers are installed in the system")
        return update_test_response(test_response=test_response, code=ResponseCode.FAILURE, message="No known browsers installed", 
                uuid="", name=session_mgr.name, ip=request.client[0] if request.client else "")

    return update_test_response(test_response=test_response, code=ResponseCode.SUCCESS, message=f"List of browsers found : {lbrowsers}", 
            uuid="", name=session_mgr.name, 
            ip = request.client[0] if request.client else "")

@app.get("/utils/list-test-types")
async def get_test_types_supported(request: Request):
    '''
        @brief async response function returning the list of test types supported by the platform
        @param request : fastapi.Request object, automatically taken when this endpoint is hit
        @return returns a Response object containing the necessary details
        @author oldgod
    '''
    info("Returning the list of Test Types")
    return update_test_response(test_response=test_response, code=ResponseCode.SUCCESS, message="List of Test Types : UI, SHELL, MISC", 
            uuid="", name="", ip=request.client[0] if request.client else "")

# test session services
@app.post("/test/init-test")
async def get_init_test(request: Request, test_request: InitTestRequest):
    '''
        @brief async response function for initializing a test session
        @param request : fastapi.Request object, automatically taken when this endpoint is hit
        @return : returns a Response object containing the necessary details
        @author oldgod
    '''
    info("Initializing a test session")
    if len(session_mgr.uuid) != 0 and len(session_mgr.name) != 0:
        warn("Session already active, will not be starting a new test session")
        return update_test_response(test_response=test_response, code=ResponseCode.FAILURE, 
                message="Test could not be initiated, test session already active", 
                uuid="", name=session_mgr.name, ip=request.client[0] if request.client else "")

    if len(test_request.name) == 0:
        warn("Test name has not been provided, will not be able to create a test session")
        return update_test_response(test_response=test_response, code=ResponseCode.FAILURE, message="Test name was not provided", 
                uuid="", name="", ip=request.client[0] if request.client else "")

    match test_request.test_type:
        case TestType.UI.name:
            debug("Test type is of UI - meaning automated test would be running on the UI")
            session_mgr.type = TestType.UI.value

            create_ui_test_session_resources(session_mgr=session_mgr)
        case TestType.SHELL.name:
            debug("Test type is of SHELL - meaning the automated test would be running shell commands")
            # fixme: add the respective code in mangler for handling the creation of a session with shell details
            session_mgr.type = TestType.SHELL.value
        case TestType.MISC.name:
            debug("Test type is of MISC - meaning the automated test can use a mixture of UI as well as SHELL commands")
            # fixme: add the code for handling the creating of both UI session as well as a shell instance
            session_mgr.type = TestType.MISC.value
        case _:
            warn("Unknown Test Type defined - return appropriate test response")
            return update_test_response(test_response=test_response, code=ResponseCode.FAILURE, 
                    message="Unknown Test Type defined, supported types are UI/SHELL/MISC", 
                    uuid="", name="", ip=request.client[0] if request.client else "")

    session_mgr.uuid = str(uuid4())
    debug(f"Session Manager set with UUID : {session_mgr.uuid}")
    session_mgr.name = test_request.name
    debug(f"Session Manager set with test name : {session_mgr.name}")
    debug(f"Session Manager set with test_type : {session_mgr.type}")

    return update_test_response(test_response=test_response, code=ResponseCode.SUCCESS, message=f"Test initiated, name: {session_mgr.name}", 
            uuid=session_mgr.uuid, name=session_mgr.name, 
            ip=request.client[0] if request.client else "")

@app.post("/test/clear-session/")
async def get_clear_test_session(request: Request, test_request: EndTestRequest): 
    info(f"About to clear session running with UUID : {test_request.uuid}")
    if session_mgr.uuid != test_request.uuid:
        warn("Requested UUID is not in session, please check the UUID again and then clear the test session")
        return update_test_response(test_response=test_response, code=ResponseCode.FAILURE, message=f"Invalid Test UUID provided : {test_request.uuid}", 
                uuid="", name=session_mgr.name, 
                ip=request.client[0] if request.client else "")

    # if the uuid is matching, then clear the session and the test name
    debug("Clearing the session manager UUID and name of the test being run")
    session_mgr.uuid = str()
    session_mgr.name = str()
    debug("Returning the proper updated response")
    return update_test_response(test_response=test_response, code=ResponseCode.SUCCESS, message=f"Test session with UUID : {test_request.uuid} cleared", 
            uuid=session_mgr.uuid, name=session_mgr.name, 
            ip=request.client[0] if request.client else "")
