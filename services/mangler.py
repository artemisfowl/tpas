'''
    @brief services module component containing all the routines for ironing out data [a controller layer kind of]
    @author oldgod
'''

from typing import Any
from logging import info, debug
from fastapi import Request

from .model import ResponseCode, TestResponse
from .constants import DEFAULT_BROWSER

def chk_browser(session_mgr: Any, lsbrowsers: list, request: Request):
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
    if not isinstance(lsbrowsers, list) or len(lsbrowsers) == 0:
        return None # raise a custom exception here


    # fixme: in the conditions below, add the code for creating a browser instance as well as a driver session for the UI - 
    # need to re-think though where to create the instance of the browser and driver, since test can be of only command type, no requirement 
    # could be there for a session of UI

    if session_mgr.config.get('config').get('browser'): # type: ignore
        debug(f"Session browser configuration : {session_mgr.config.get('config').get('browser')}") # type: ignore
        if session_mgr.config.get('config').get('browser') in lsbrowsers: # type: ignore
            debug("Configured browser found in list of browsers installed")
            return TestResponse(code=ResponseCode.SUCCESS, 
                    message=f"Test initiated, browser selected : {session_mgr.config.get('config').get('browser')}", # type: ignore
                    ip=request.client[0]) # type: ignore
        else:
            debug("Configured browser is not present in the list of browsers installed")
            return TestResponse(code=ResponseCode.FAILURE, 
                    message=f"Selected browser : {session_mgr.config.get('config').get('browser')} not installed in system", # type: ignore
                    ip=request.client[0]) # type: ignore
    else:
        # the browser is not configured in the configuration file, check for the presence of the default browser
        debug("Checking for the presence of default browser")
        if DEFAULT_BROWSER in lsbrowsers:
            debug("Found default browser in list of browsers")
            return TestResponse(code=ResponseCode.SUCCESS, message=f"Test initiated, {DEFAULT_BROWSER} has been selected", ip=request.client[0]) # type: ignore
        else:
            debug("Could not find default browser in list of browsers")
            return TestResponse(code=ResponseCode.FAILURE, message="Test initiated, but browser not set", ip=request.client[0]) # type: ignore
