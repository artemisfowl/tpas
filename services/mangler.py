'''
    @brief services module component containing all the routines for ironing out data [a controller layer kind of]
    @author oldgod
'''

from typing import Any
from logging import info, debug
from fastapi import Request

from .model import ResponseCode, TestResponse, ResponseMessage
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


    # fixme: this should be a persistent object - better create the same in the init file
    test_response = TestResponse(code=ResponseCode.DEFAULT, message=ResponseMessage.DEFAULT)
    test_response._ip = request.client[0] # type: ignore
    test_response.uuid = session_mgr.uuid

    if session_mgr.config.get('config').get('browser'): # type: ignore
        debug(f"Session browser configuration : {session_mgr.config.get('config').get('browser')}") # type: ignore
        if session_mgr.config.get('config').get('browser') in lsbrowsers: # type: ignore
            debug("Configured browser found in list of browsers installed")
            test_response._code = ResponseCode.SUCCESS
            test_response._message = f"Test initiated, browser selected : {session_mgr.config.get('config').get('browser')}", # type: ignore
            return test_response
        else:
            debug("Configured browser is not present in the list of browsers installed")
            test_response._code = ResponseCode.FAILURE
            test_response._message = f"Selected browser : {session_mgr.config.get('config').get('browser')} not installed in system", # type: ignore
            return test_response
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
