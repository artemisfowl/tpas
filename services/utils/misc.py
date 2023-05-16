'''
    @brief utils submodule component containing all the routines for which no specific file has been decided
    @author oldgod

    @note this file contains all the functions/routines/sub-routines which does not a have a properly 
    purposed filename specified. For example, file system specific functions/structures will be going into 
    fileutils, but this file is created only for housing the orphaned functions for now. Kind of like __future__
'''

from typing import Any

def update_test_response(test_response: Any, code: int, message: str, uuid: str, name: str="", ip: str=""):
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

    return test_response
