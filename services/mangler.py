'''
    @brief services module component containing all the routines for ironing out data [a controller layer kind of]
    @author oldgod
'''

from logging import info, debug, warn
from os import sep
from pathlib import Path
from psutil import process_iter

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from .model import SessionManager
from .constants import (DEFAULT_BROWSER, EXIT_SUCCESS, EXIT_FAILURE, DEFAULT_DRIVER_BINARY, DEFAULT_BROWSER_REMOTE_CONTROL_MODE)
from .constants import UiActionType

def perform_operation(session_mgr: SessionManager, by: str, locator: str, action: str) -> int:
    if not session_mgr and not by and not locator and not action:
        return EXIT_FAILURE

    match by.lower():
        case "id":
            session_mgr.ui_element = session_mgr.driver.find_element(By.ID, locator)
        case "css selector":
            session_mgr.ui_element = session_mgr.driver.find_element(By.CSS_SELECTOR, locator)
        case _:
            return EXIT_FAILURE

    match action.upper():
        case UiActionType.CLICK.name:
            session_mgr.ui_element.click()
        case UiActionType.TYPE.name:
            session_mgr.ui_element.send_keys("speedtest")

    return EXIT_SUCCESS

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
                # this portion checks if the instance is already open
                for process in process_iter():
                    if DEFAULT_BROWSER in process.name():
                        if any(DEFAULT_BROWSER_REMOTE_CONTROL_MODE in cmd for cmd in process.cmdline()):
                            cmd = [s for s in process.cmdline() if DEFAULT_BROWSER_REMOTE_CONTROL_MODE in s][0]

                            if not session_mgr.driver:
                                for browser_details in session_mgr.browser:
                                    if browser_details.get("browser_type") == DEFAULT_BROWSER: 
                                        options = Options()
                                        # fixme: update the code so that the strings are not present here
                                        options.add_experimental_option("debuggerAddress", f"127.0.0.1:{int(cmd[cmd.index('=')+1:])}")
                                        session_mgr.driver = webdriver.Chrome(executable_path=final_driver_location, 
                                                options=options)
                else:
                    info("Starting default web browser in nomal mode")
                    if not session_mgr.driver:
                        for browser_details in session_mgr.browser:
                            if browser_details.get("browser_type") == DEFAULT_BROWSER:
                                session_mgr.driver = webdriver.Chrome(executable_path=final_driver_location)
            else:
                warn("Web driver binary file not found, kindly upload the file using /utils/fileupload endpoint in services/driver location")
                return EXIT_FAILURE
        else:
            debug(f"Creating webdriver session for specified browser : {config.get('browser')}")
            # fixme: add the code for creating the webdriver for the specified browser
            pass

    return EXIT_SUCCESS
