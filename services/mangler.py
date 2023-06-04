'''
    @brief services module component containing all the routines for ironing out data [a controller layer kind of]
    @author oldgod
'''

from typing import Any
from logging import info, debug, warn
from fastapi import Request
from browsers import browsers

from .model import ResponseCode, SessionManager
from .utils import update_test_response, get_url_details, get_latest_default_driver_url
from .constants import (DEFAULT_BROWSER, EXIT_SUCCESS, EXIT_FAILURE, DEFAULT_DRIVER_BINARY, 
        DEFAULT_LATEST_DRIVER_URL, DEFAULT_BROWSER_DRIVER_BASE_URL)

# fixme: recreate the function for the creation of the UI session
def create_ui_test_session_resources(session_mgr: SessionManager) -> int:
    '''
        @brief function to create ui test resource.
        @author oldgod
        @return Returns an integer, 0 when opertion is successfull else -1
    '''
    if not isinstance(session_mgr, SessionManager):
        warn("Session instance not provided, returning control to calling function")
        return EXIT_FAILURE

    info("Starting to create the test session")

    # fixme: check the browser which is installed in the system
    installed_browsers = list(browsers())
    debug(f"Installed browsers : {installed_browsers}")

    # fixme: add the code for creating the driver based on the installed browser and update the same in the session manager
    for browser in installed_browsers:
        tmp = {}
        tmp['browser_type'] = browser.get('browser_type')
        tmp['install_path'] = browser.get('path').split()[-1]
        tmp["version"] = browser.get("version")
        debug(f"tmp data : {tmp}")
        session_mgr.browser.append(tmp)

    debug(f"Session Manager contents (post update) : {session_mgr.__dict__}")

    # fixme: check if the browser information is provided or not - if the browser is not configured, use the default browser, 
    # update the same in the log file
    config = session_mgr.config.get("config")
    if config:
        if not config.get("browser"): # if the browser is not specified, please select the default browser
            warn(f"Browser is not specified, creating webdriver session for default browser : {DEFAULT_BROWSER}")

            debug(f"Version of latest geckodriver : {get_url_details(url=DEFAULT_LATEST_DRIVER_URL).split('/')[-1]}")
            final_download_url = get_latest_default_driver_url(driver_version=get_url_details(url=DEFAULT_LATEST_DRIVER_URL).split('/')[-1],
                    driver_download_base_url=DEFAULT_BROWSER_DRIVER_BASE_URL) # type: ignore

            # fixme: add the code for creating the webdriver for the default browser
        else:
            debug(f"Creating webdriver session for specified browser : {config.get('browser')}")
            # fixme: add the code for downloading the right binary based on the configured browser version
            # fixme: add the code for creating the webdriver for the specified browser
            pass

    return EXIT_SUCCESS

# fixme: the following function needs to be rewritten
def chk_browser(test_response: Any, session_mgr: Any, lsbrowsers: list, request: Request):
    '''
        @brief check if the configured browser/default browser is installed in the system and set up the instance accordingly
        @author oldgod
        @param session_mgr: An object of the Session class
                lsbrowsers: list containing the names of the browsers installed

        @return returns None in case the parameters are not provided, else returns a TestResponse object with the appropriate message
    '''
    info("About to check if the required browser is installed on the system or not")

    if not session_mgr:
        return None # raise a custom exception here
    if not test_response:
        return None # raise a custom exception here
    if not isinstance(lsbrowsers, list) or len(lsbrowsers) == 0:
        return None # raise a custom exception here


    # fixme: this should be a persistent object - better create the same in the init file
    test_response.uuid = session_mgr.uuid # this will also not be required

    if session_mgr.config.get('config').get('browser'): # type: ignore
        debug(f"Session browser configuration : {session_mgr.config.get('config').get('browser')}") # type: ignore
        if session_mgr.config.get('config').get('browser') in lsbrowsers: # type: ignore
            debug("Configured browser found in list of browsers installed")
            return update_test_response(test_response=test_response, code=ResponseCode.SUCCESS, 
                    message=f"Test initiated, browser selected : {session_mgr.config.get('config').get('browser')}", 
                    uuid=session_mgr.uuid, name=session_mgr.name, ip=request.client[0] if request.client else "")
        else:
            debug("Configured browser is not present in the list of browsers installed")
            # fixme: if this is to be returned, make sure the test instance is also cleared off, add the necessary code for this
            return update_test_response(test_response=test_response, code=ResponseCode.FAILURE, 
                    message=f"Selected browser : {session_mgr.config.get('config').get('browser')} not installed in system",
                    uuid=session_mgr.uuid, name=session_mgr.name, ip=request.client[0] if request.client else "")
    else:
        # the browser is not configured in the configuration file, check for the presence of the default browser
        debug("Checking for the presence of default browser")
        if DEFAULT_BROWSER in lsbrowsers:
            debug("Found default browser in list of browsers")
            test_response._code = ResponseCode.SUCCESS
            test_response._message = f"Test initiated, {DEFAULT_BROWSER} has been selected"
            return test_response
        else:
            debug("Could not find default browser in list of browsers")
            test_response._code = ResponseCode.FAILURE
            test_response._message = "Test initiated, but browser not set"
            return test_response
