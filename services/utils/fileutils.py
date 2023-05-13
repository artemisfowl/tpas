'''
    @brief Utility submodule containing all the service based routines and subroutines
    @author oldgod
'''

from typing import Union
from configparser import ConfigParser
from logging import info, debug

def read_module_config(configpath: str) -> Union[None, ConfigParser]:
    if not isinstance(configpath, str) or len(configpath) == 0:
        return None

    info("Creating the parser instance")
    _parser = ConfigParser()
    debug(f"Reading the configuration file from : {configpath}")
    _parser.read(configpath)

    debug("Returning the parser instance")
    return _parser
