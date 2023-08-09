'''
    @brief services module component containing all the routines for ironing out data [a controller layer kind of]
    @author oldgod
'''

from typing import Union
from logging import info, debug, warn, error
from os import sep
from pathlib import Path
from psutil import process_iter
from platform import system, release, version as platform_version

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from .model import SessionManager
from .constants import (DEFAULT_BROWSER, EXIT_SUCCESS, EXIT_FAILURE, DEFAULT_DRIVER_BINARY, DEFAULT_BROWSER_REMOTE_CONTROL_MODE)
from .constants import UiActionType

def prepare_system_details(browser_list: list) -> dict:
    '''
        @brief function to prepare the system details
        @param browser_list: List containing the installed browser details
        @return returns a dictionary containing the system details
        @author oldgod

        @note This function will throw an exception is the list of installed browsers are not provided to it.
    '''
    system_details = {}

    # fixme: add a message to the test response which will be returned
    if not isinstance(browser_list, list):
        error(f"Installed Browser details should be a list, found {type(browser_list)}")
    elif len(browser_list) == 0:
        warn(f"No browsers were detected installed in the system, kindly contact system administrator to install a browser")
    
    system_details["os_type"] = system()
    system_details["os_release"] = release()
    system_details["os_release_version"] = platform_version()
    system_details["browsers"] = browser_list

    return system_details

def perform_operation(session_mgr: SessionManager, by: str, locator: str, action: str, value: str="") -> int:
    '''
        @brief function to perform a specified operation
        @param session_mgr: SessionManager object containing the details of the test session
        @param by: Enum containing the various ways with which an element could be identified
        @param locator: str containing the locator to be used in order to find the element
        @param action: str containing the type of action to be performed on the identified element
        @param value: str containing the value to be sent to the identified element [this is only to be provided if the action is to type something]
        @return returns an integer; -1 on failure, 0 on success
        @author oldgod

        @note There are certain portions of the implementation which are left out, they need to be implemented
    '''
    if not session_mgr and not by and not locator and not action:
        return EXIT_FAILURE

    info("Locating the element mentioned")
    debug(f"Locating the element by : {by} with locator : {locator}")

    match by.lower():
        case "id":
            session_mgr.ui_element = session_mgr.driver.find_element(By.ID, locator)
        case "name":
            session_mgr.ui_element = session_mgr.driver.find_element(By.NAME, locator)
        case "xpath":
            session_mgr.ui_element = session_mgr.driver.find_element(By.XPATH, locator)
        case "link text":
            session_mgr.ui_element = session_mgr.driver.find_element(By.LINK_TEXT, locator)
        case "partial link text":
            session_mgr.ui_element = session_mgr.driver.find_element(By.PARTIAL_LINK_TEXT, locator)
        case "tag name":
            session_mgr.ui_element = session_mgr.driver.find_element(By.TAG_NAME, locator)
        case "class name":
            session_mgr.ui_element = session_mgr.driver.find_element(By.CLASS_NAME, locator)
        case "css selector":
            session_mgr.ui_element = session_mgr.driver.find_element(By.CSS_SELECTOR, locator)
        case _:
            return EXIT_FAILURE

    debug(f"About to perform action: {action} on the element")
    match action.upper():
        case UiActionType.CLICK.name:
            session_mgr.ui_element.click()
        case UiActionType.LEFT_CLICK.name:
            session_mgr.ui_element.click()
        case UiActionType.RIGHT_CLICK.name:
            # fixme: add the code for moving the identified element to view and then RIGHT CLICKING on it, perform the operations using pynput
            # performing the right click might be a bit tricky, so, in order to do that, we will be using pynput
            pass
        case UiActionType.MIDDLE_CLICK.name:
            # fixme: add the code for performing the action on MIDDLE MOUSE BUTTON click, perform the operations using pynput
            pass
        case UiActionType.DRAG_N_DROP.name:
            # fixme: add the code for performing the action on DRAG and DROP, perform the operations using pynput
            pass
        case UiActionType.SCROLL.name:
            # fixme: add the code for performing the action on SCROLL, perform the fallback operation using pynput
            pass
        case UiActionType.TYPE.name:
            if len(value) > 0:
                session_mgr.ui_element.send_keys(value)

    return EXIT_SUCCESS

def get_supported_ui_actions() -> list:
    '''
        @brief function to return the list of UI actions supported
        @return returns a list containing the actions which are supported
        @author oldgod
    '''
    info("Checking supported UI Actions")
    debug(f"Returning supported UI actions : {UiActionType._member_names_}")
    return UiActionType._member_names_

def create_ui_test_session_resources(session_mgr: SessionManager) -> int:
    '''
        @brief function to create ui test resource.
        @return Returns an integer, 0 when opertion is successfull else -1
        @author oldgod
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
