'''
    @brief utils submodule component containing all the routines for which no specific file has been decided
    @author oldgod

    @note this file contains all the functions/routines/sub-routines which does not a have a properly 
    purposed filename specified. For example, file system specific functions/structures will be going into 
    fileutils, but this file is created only for housing the orphaned functions for now. Kind of like __future__
'''

from typing import Any
from browsers import browsers

def update_test_response(test_response: Any, code: int, message: str, uuid: str, name: str="", ip: str="", **kwargs):
    '''
        @brief function to modify the test_response object based on the values provided
        @author oldgod
        @param code: Integer containing the Response Code
                message: String containing the message to be shown to the developer/coder
                uuid: String containing the uuid of the test created while initiating a test
                name: String containing the name of the test which is being run, 
                defaults to empty string
                ip: String containing the ip of the machine requesting the REST API resource, 
                defaults to empty string
        @return returns a modified version of the test response object
    '''
    if not test_response:
        raise ValueError("Test Response Object not provided")
    if not isinstance(code, int):
        raise ValueError("Response Code is not a proper value")
    if not isinstance(message, str):
        raise ValueError("Response Message is not a proper value")
    if not isinstance(uuid, str):
        raise ValueError("Response UUID is not a proper value")

    # member updates
    test_response._code = code
    test_response._message = message
    test_response._ip = ip

    # property updates
    test_response.uuid = uuid
    test_response.name = name
    test_response.obj = kwargs

    return test_response

def find_installed_browsers() -> list:
    '''
        @brief function to find the installed browsers
        @return returns a list containing all the details of the browsers installed 
        @author oldgod
    '''
    installed_browsers = list(browsers())
    rlist = []

    for browser in installed_browsers:
        tmp = {}
        tmp['browser_type'] = browser.get('browser_type')
        tmp['install_path'] = browser.get('path').split()[-1]
        tmp["version"] = browser.get("version")
        rlist.append(tmp)

    return rlist
