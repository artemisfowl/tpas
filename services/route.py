"""
    @brief Services module component containing all the basic API routes
    @author oldgod
"""

from os import sep, makedirs
from uuid import uuid4
from logging import info, debug, warn, error
from pathlib import Path
from traceback import format_exc
from platform import system, release, version as platform_version
from json import dumps

from fastapi import FastAPI, Request, File, UploadFile, Depends
from browsers import browsers

from .model import ResponseCode, SessionManager
from .model import test_response
from .model import AdminRequest, InitTestRequest, EndTestRequest, FileUploadRequest
from .constants import DEFAULT_ADMIN_PASSWORD, DEFAULT_ADMIN_USER, DEFAULT_DRIVER_BINARY, EXIT_FAILURE
from .constants import TestType
from .utils import read_module_config, update_test_response, find_installed_browsers

# fixme: add the right API for calling the check browser function
from .mangler import create_ui_test_session_resources

app = FastAPI()
session_mgr = SessionManager()
# setting up the module specific configuration details in the config property
session_mgr.config = read_module_config(configpath=f"{__file__[:__file__.rindex(sep)+1]}module.ini") # type: ignore
session_mgr.browser = find_installed_browsers()

# create the web UI default browser driver binary path at runtime
g_module_directory_path = __file__[:__file__.rfind(__name__[:__name__.find('.')])]
if not g_module_directory_path.endswith(sep):
    g_module_directory_path += sep
g_final_driver_location = f"{g_module_directory_path}{DEFAULT_DRIVER_BINARY}"
debug(f"Creating driver binary directory path : {g_final_driver_location[:g_final_driver_location.rfind(sep)]}")
makedirs(g_final_driver_location[:g_final_driver_location.rfind(sep)], exist_ok=True)

# root services
@app.get("/", tags=["module"])
async def get_root(request: Request):
    '''
        - **@brief** async response function default index
        - **@param** request : fastapi.Request object, automatically taken when this endpoint is hit
        - **@return** returns a Response object containing the necessary details
        - **@author** oldgod
    '''
    info("Welcome to the root URL of TPAS")

    return update_test_response(test_response=test_response, code=ResponseCode.SUCCESS, message='Welcome to TPAS', 
            uuid=session_mgr.uuid, name=session_mgr.name, 
            ip=request.client[0] if request.client else "")

@app.get("/status", tags=["module"])
async def get_service_status(request: Request):
    '''
        - **@brief** async response function returning the status of the API(s) running
        - **@param** request : fastapi.Request object, automatically taken when this endpoint is hit
        - **@return** returns a Response object stating if the sessions is in IDLE state(when no test sessions are being executed) 
                    else shows the name of the test session UUID
        - **@author** oldgod
    '''
    info("Serving status of services")

    if len(session_mgr.uuid) > 0:
        debug(f"Test session active, session name : {session_mgr.name}, session UUID : {session_mgr.uuid}")
        return update_test_response(test_response=test_response, code=ResponseCode.SUCCESS, message=f"Running Test : {session_mgr.name}", 
                uuid="", name=session_mgr.name, 
                ip=request.client[0] if request.client else "")

    debug("Services are idle, no test session is running")
    return update_test_response(test_response=test_response, code=ResponseCode.SUCCESS, message="IDLE", 
            uuid="", name=session_mgr.name, 
            ip=request.client[0] if request.client else "")

# admin services { will be added here later }
@app.post("/admin/clearall", tags=["admin"])
async def post_clear_all_sessions(request: Request, test_request: AdminRequest):
    '''
        - **@brief** async response function used for clearing the Test session when the session UUID is misplaced
        - **@param** request : fastapi.Request object, automatically taken when this endpoint is hit
        - **@param** test_request : AdminRequest object, contains the administrator username and password
        - **@return** returns a successful response in case the session is invalidated/cleared, else a failure response
        - **@author** oldgod
    '''
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
@app.get("/utils/list-browsers", tags=["utils"], deprecated=True)
async def get_installed_browsers(request: Request):
    '''
        - **@brief** async response function returning the list of browsers installed in the system
        - **@param** request : fastapi.Request object, automatically taken when this endpoint is hit
        - **@return** returns a Response object containing the necessary details
        - **@author** oldgod

        **@note** this is a deprecated service, please use /utils/system-details endpoint for the entire system information
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

@app.get("/utils/list-test-types", tags=["utils"])
async def get_test_types_supported(request: Request):
    '''
        - **@brief** async response function returning the list of test types supported by the platform
        - **@param** request : fastapi.Request object, automatically taken when this endpoint is hit
        - **@return** returns a Response object containing the necessary details
        - **@author** oldgod
    '''
    info("Returning the list of Test Types")
    return update_test_response(test_response=test_response, code=ResponseCode.SUCCESS, message="List of Test Types : UI, SHELL, MISC", 
            uuid="", name="", ip=request.client[0] if request.client else "")

@app.get("/utils/system-details", tags=["utils"])
async def get_system_details(request: Request):
    '''
        - **@brief** function to get the system details - architecture, software version, OS version and the like
        - **@param** request : fastapi.Request object, automatically taken when this endpoint is hit
        - **@return** returns a Response object containing the system details
        - **@author** oldgod
    '''
    info("Getting the system details")

    # fixme: move the code to proper functions in mangler
    system_details = {}
    system_details["os_type"] = system()
    system_details["os_release"] = release()
    system_details["os_release_version"] = platform_version()
    system_details["browsers"] = session_mgr.browser
    debug(f"System Details : {dumps(system_details, indent=2)}")

    rval = {}
    rval["response"] = test_response.__dict__
    rval["system_details"] = system_details
    rval["response"] = update_test_response(test_response=test_response, code=ResponseCode.SUCCESS, message=f"System details are as follows", 
            uuid="", name="",
            ip=request.client[0] if request.client else "")
    return rval

@app.post("/utils/upload-file/", tags=["utils"])
async def post_upload_file(request: Request, upload_request: FileUploadRequest = Depends(), file: UploadFile = File(...)):
    '''
        - **@brief** utility function for uploading a specified file to the desired location
        - **@param** request : fastapi.Request object, automatically taken when this endpoint is hit
        - **@param** upload_request : FileUploadRequest object, contains the value of destination directory in the server
        - **@return** returns a Response object containing the necessary details
        - **@author** oldgod
    '''
    info("Starting upload of file")

    # fixme: transfer the logic of uploading the file to a separate common function
    if not isinstance(upload_request.destination_dir, str):
        warn(f"Destination directory : {upload_request.destination_dir} is not proper")
        return update_test_response(test_response=test_response, code=ResponseCode.FAILURE, 
                message="Destination directory value is not proper", 
                uuid=session_mgr.uuid, name=session_mgr.name,
                ip=request.client[0] if request.client else "")

    debug(f"Checking if the directory specified exists or not : {upload_request.destination_dir}")
    if not Path(upload_request.destination_dir).is_dir():
        debug(f"Destination directory : {upload_request.destination_dir} not present, creating it")
        makedirs(upload_request.destination_dir)
    else:
        debug(f"Destination directory : {upload_request.destination_dir} already exists")

    try:
        remote_dir = f"{upload_request.destination_dir}{sep}{file.filename}"
        debug(f"Uploading file : {remote_dir}")
        with open(remote_dir, "wb") as uf: # uf is short for uploaded file # type: ignore
            debug("Writing to file")
            while contents := file.file.read(1024 * 1024):
                debug(f"Written : {len(contents)}")
                uf.write(contents)
    except Exception as _:
        warn("Exception occurred while trying to upload file")
        error(format_exc())
        return update_test_response(test_response=test_response, code=ResponseCode.FAILURE, 
                message=f"Exception occurred while trying to upload file : {file.filename}",
                uuid="", name="", 
                ip=request.client[0] if request.client else "")

    return update_test_response(test_response=test_response, code=ResponseCode.SUCCESS, 
            message=f"Uploaded file : {file.filename} saved in destination : {upload_request.destination_dir}", 
            uuid=session_mgr.uuid, name=session_mgr.name,
            ip=request.client[0] if request.client else "")


# test session services
@app.post("/test/init-test", tags=["test"])
async def post_init_test(request: Request, test_request: InitTestRequest):
    '''
        - **@brief** async response function for initializing a test session
        - **@param** request : fastapi.Request object, automatically taken when this endpoint is hit
        - **@return** : returns a Response object containing the necessary details
        - **@author** oldgod
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

    match test_request.test_type.upper():
        case TestType.UI.name:
            debug("Test type is of UI - meaning automated test would be running on the UI")
            session_mgr.type = TestType.UI.value
            if create_ui_test_session_resources(session_mgr=session_mgr) == EXIT_FAILURE:
                return update_test_response(test_response=test_response, code=ResponseCode.FAILURE, 
                        message="Kindly upload the file using /utils/fileupload endpoint in services/driver location", 
                        uuid="", name="", ip=request.client[0] if request.client else "")
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

@app.post("/test/clear-session/", tags=["test"])
async def post_clear_test_session(request: Request, test_request: EndTestRequest): 
    '''
        - **@brief** async function for clearing a test session
        - **@param** request : fastapi.Request object, automatically taken when this endpoint is hit
        - **@param** test_request : EndTestRequest object, containing the UUID of the test session which needs to be invalidated
        - **@return** returns a successful response if the UUID provided matches with the current active test session and the same is cleared/invalidted.
                    else returns a failure response
    '''
    # fixme: add the proper documentation string for this function
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
