'''
    @brief services module component containing all the routines for ironing out data [a controller layer kind of]
    @author oldgod
'''

from logging import info, debug, warn
from browsers import browsers
from os import sep
from pathlib import Path

from .model import SessionManager
from .constants import (DEFAULT_BROWSER, EXIT_SUCCESS, EXIT_FAILURE, DEFAULT_DRIVER_BINARY)

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

    debug(f"Session Manager contents (post update) : {session_mgr.__dict__}")
    config = session_mgr.config.get("config")
    if config:
        if not config.get("browser"): # default browser handling
            warn(f"Browser is not specified, creating webdriver session for default browser : {DEFAULT_BROWSER}")

            module_directory_path = __file__[:__file__.rfind(__name__[:__name__.find('.')])]
            if not module_directory_path.endswith(sep):
                module_directory_path += sep
            debug(f"Module directory path : {module_directory_path}")

            final_driver_location = f"{module_directory_path}{DEFAULT_DRIVER_BINARY}"
            debug(f"Final default driver binary location : {final_driver_location}")

            if Path(final_driver_location).is_file():
                debug("Web driver binary file found")
                # fixme: add the code for creating a webdriver session based on the parameters provided in the request
                # fixme: add the code for creating the driver based on the installed browser and update the same in the session manager
                # design: how the latching can also be done for the browser - default as well as configured
            else:
                # fixme: add the endpoint /utils/fileupload and allow for uploading file from the remote machine
                warn("Web driver binary file not found, kindly upload the file using /utils/fileupload endpoint in services/driver location")
                return EXIT_FAILURE
        else:
            debug(f"Creating webdriver session for specified browser : {config.get('browser')}")
            # fixme: add the code for creating the webdriver for the specified browser
            pass

    return EXIT_SUCCESS
