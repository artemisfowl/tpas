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
from selenium.webdriver.common.by import By
from .model import ResponseCode, SessionManager
from .model import test_response
from .model import AdminRequest, InitTestRequest, EndTestRequest, FileUploadRequest, UiRequest, NavigationRequest
from .constants import DEFAULT_ADMIN_PASSWORD, DEFAULT_ADMIN_USER, DEFAULT_DRIVER_BINARY, EXIT_FAILURE
from .constants import TestType
from .utils import read_module_config, update_test_response, find_installed_browsers

# fixme: add more functions to mangler and reduce the number of LoC in the route file
from .mangler import create_ui_test_session_resources, perform_operation, get_supported_ui_actions

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

@app.get("/version", tags=["module"])
async def get_module_version(request: Request):
    '''
        - **@brief** async function to show the release version of this module
        - **@param** request : fastapi.Request object, automatically taken when this endpoint is hit
        - **@return** returns the version number of the module based on the version specified in module configuration
        - **@author** oldgod
    '''
    info("Getting the version number of the module")

    # fixme: add the relevant function in mangler and call it here
    debug(f"Session manager details : {session_mgr.__dict__}")
    version_number = session_mgr.config.get('config').get('version') if session_mgr.config.get('config') else None # type: ignore
    debug(f"Version number as present in configuration file : {version_number}")

    if not version_number:
        error("Version number not specified in configuration file")
        return update_test_response(test_response=test_response, code=ResponseCode.FAILURE, 
                message="Version number of release not specified",
                uuid="", name="", 
                ip=request.client[0] if request.client else "")

    # fixme: add the version number in the obj
    return update_test_response(test_response=test_response, code=ResponseCode.SUCCESS, 
            message=f"Version number updated in the obj attribute",
            uuid="", name="", 
            ip=request.client[0] if request.client else "", 
            module_version_no=version_number)

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
            uuid_tmp = session_mgr.uuid
            name_tmp = session_mgr.name
            session_mgr.uuid = ""
            session_mgr.name = ""

            if session_mgr.driver:
                session_mgr.driver.close()
                session_mgr.driver = None

            debug("Test session clear succesfull, returning the updated response")
            return update_test_response(test_response=test_response, code=ResponseCode.SUCCESS, 
                    message="Test session invalidated", 
                    uuid="", name="", ip=request.client[0] if request.client else "",
                    invalidated_test_session_details={"uuid": uuid_tmp, "name": name_tmp})
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
        return update_test_response(test_response=test_response, code=ResponseCode.FAILURE, 
                message="No known browsers installed", 
                uuid="", name="", ip=request.client[0] if request.client else "")

    return update_test_response(test_response=test_response, code=ResponseCode.SUCCESS, 
            message="Installed browser details updated, check obj", 
            uuid="", name=session_mgr.name, 
            ip = request.client[0] if request.client else "",
            installed_browser_list=lbrowsers)

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

@app.get("/utils/locator-techniques", tags=["utils"])
async def get_locator_techniques(request: Request):
    # fixme: add the proper documentation string for this function
    # fixme: add the provision in the test_response to send out a dictionary containing miscellaneous details
    get_supported_ui_actions() # fixme: add the necessary code in order to parse the output
    return update_test_response(test_response=test_response, code=ResponseCode.SUCCESS, 
            message="Locator techniques are as follows", 
            uuid="", name="", ip = request.client[0] if request.client else "")

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

    if session_mgr.driver:
        session_mgr.driver.close()
        session_mgr.driver = None
    return update_test_response(test_response=test_response, code=ResponseCode.SUCCESS, message=f"Test session with UUID : {test_request.uuid} cleared", 
            uuid=session_mgr.uuid, name=session_mgr.name, 
            ip=request.client[0] if request.client else "")

@app.post("/ui/navigate", tags=["ui"])
async def post_navigate_to(request: Request, test_request: NavigationRequest):
    # fixme: add documentation string for this function
    info("Navigating to the specified URL")
    if session_mgr.uuid != test_request.uuid:
        return update_test_response(test_response=test_response, code=ResponseCode.FAILURE, 
                message="Inavlid UUID provided", uuid="", name=session_mgr.name, 
                ip=request.client[0] if request.client else "")

    if len(test_request.url) == 0:
        return update_test_response(test_response=test_response, code=ResponseCode.FAILURE, 
                message=f"Invalid URL to navigate to", uuid=session_mgr.uuid, name=session_mgr.name, 
                ip=request.client[0] if request.client else "")

    debug(f"Navigating to : {test_request.url}")
    session_mgr.driver.get(test_request.url)

    return update_test_response(test_response=test_response, code=ResponseCode.SUCCESS,
            message=f"Navigation to URL : {test_request.url} successful", uuid=session_mgr.uuid, name=session_mgr.name, 
            ip=request.client[0] if request.client else "")

@app.post("/ui/find-element", tags=["ui"])
async def post_find_element(request: Request, test_request: UiRequest):
    # fixme: add proper documentation string for this function
    info("Trying to find the element specified")
    if session_mgr.uuid != test_request.uuid:
        return update_test_response(test_response=test_response, code=ResponseCode.FAILURE, 
                message="Inavlid UUID provided", uuid="", name=session_mgr.name, 
                ip=request.client[0] if request.client else "")

    debug(f"Finding element with locator : {test_request.locator} by {test_request.by}")
    match test_request.by.lower():
        case "id":
            session_mgr.ui_element = session_mgr.driver.find_element(By.ID, test_request.locator)
        case "css selector":
            session_mgr.ui_element = session_mgr.driver.find_element(By.CSS_SELECTOR, test_request.locator)
        case _:
            return update_test_response(test_response=test_response, code=ResponseCode.FAILURE,
                    message=f"Unknown location technique specified : {test_request.by}",
                    uuid=session_mgr.uuid, name=session_mgr.name, 
                    ip=request.client[0] if request.client else "")

    return update_test_response(test_response=test_response, code=ResponseCode.SUCCESS, 
            message=f"Element found : {session_mgr.ui_element.text}", uuid=session_mgr.uuid, name=session_mgr.name, 
            ip=request.client[0] if request.client else "")

@app.post("/ui/perform-operation", tags=["ui"])
async def post_perform_operation(request: Request, test_request: UiRequest):
    info("Performing operation on element")
    if session_mgr.uuid != test_request.uuid:
        return update_test_response(test_response=test_response, code=ResponseCode.FAILURE, 
                message="Inavlid UUID provided", uuid="", name=session_mgr.name, 
                ip=request.client[0] if request.client else "")

    debug(f"Performing operation : {test_request.action} on element of type : {test_request.locator} to be found by : {test_request.by}")
    if perform_operation(session_mgr=session_mgr, by=test_request.by, locator=test_request.locator, action=test_request.action) == EXIT_FAILURE:
        return update_test_response(test_response=test_response, code=ResponseCode.FAILURE, 
                message=f"Unable to perform operation : {test_request.action} on element of type : {test_request.locator} to be found by : {test_request.by}",
                uuid=session_mgr.uuid, name=session_mgr.name, 
                ip=request.client[0] if request.client else "")

    return update_test_response(test_response=test_response, code=ResponseCode.SUCCESS, 
            message="Performed operation: {}", uuid=session_mgr.uuid, name=session_mgr.name, 
            ip=request.client[0] if request.client else "")
