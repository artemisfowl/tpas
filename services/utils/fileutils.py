'''
    @brief Utility submodule containing all the service based routines and subroutines
    @author oldgod
'''

from typing import Union
from configparser import ConfigParser
from logging import info, debug
from pathlib import Path

def read_module_config(configpath: str) -> Union[None, dict]:
    '''
        @brief function to read the module specific configuration file
        @author oldgod
        @param configpath: String containing the path to the configuration file
        @return Returns a dictionary containing the details of the configuration file

        @note The configuration file needs to be an INI format file, else this function will 
        have issues parsing the information
    '''
    if not isinstance(configpath, str) or len(configpath) == 0:
        return None

    info("Creating the parser instance")
    _parser = ConfigParser()
    debug(f"Reading the configuration file from : {configpath}")
    _parser.read(configpath)

    debug("Returning the parser instance")
    return _parser.__dict__.get("_sections")

def file_exists(filepath: str) -> bool:
    '''
        @brief function to check if the file specified by the filepath exists or not
        @params filepath: String containing the filepath
        @return returns a boolean value, True if the file exists, else False
        @author oldgod

        @note If the filepath is not a string or an empty string, 
        the result will always be a False value
    '''
    if len(filepath) == 0:
        return False
    elif not isinstance(filepath, str):
        return False
    return Path(filepath).exists()
