'''
    @brief utility module component containing all the functions and classes for performing tasks for run
    @author oldgod
'''

from copy import deepcopy
from os import sep
from glob import glob
from sys import version_info, exit
from logging import info, debug, error, root, DEBUG

from uvicorn import run as uvrun

from .constants import PYVER_MAJOR, PYVER_MINOR
from model import ModuleConfig, ConfigContainer

def list_submodules(dir: str) -> dict:
    '''
        @brief function to list all the modules present under a specific directory
        @param dir : string containing the root path where all the modules are present
        @return Returns a dictionary of the modules found, keys are the names of the modules, values are the paths to module specific INI files
        @author oldgod
    '''

    # fixme: convert this into a dictionary, key : string containing the name of the module, value: string containing the path of the module.ini file
    modules = {}

    if dir is None or not isinstance(dir, str) or len(dir) == 0:
        return modules

    result = glob(f"{dir}{sep}**{sep}module.ini")
    for module in result:
        path = deepcopy(module)
        module = module[:module.index("module")-1]
        module = module[module.rindex(f"{sep}")+1:]
        modules[module] = path

    return modules

def chk_pyver():
    '''
        @brief function to check the version of Python being used in order to run TPAS.
        @author oldgod

        @note If the Python version does not match Python 3.10, the program will be exiting immediately
    '''

    if version_info.major == PYVER_MAJOR:
        if version_info.minor != PYVER_MINOR:
            print(f"Python version to be used with this program : 3.10+, current version is {version_info.major}.{version_info.minor}")
            exit(-1)
    else:
        print(f"Python version to be used with this program : 3.10+, current version is {version_info.major}.{version_info.minor}")
        exit(-1)

# fixme: provide the entire dictionary to this function, since the module configuration file needs to be read
def run_module(module_name: str, modules: dict):
    '''
        @brief function to run the module specified, uses a switcher for any new module created
        @param module_name : String containing the name of the module to be run
            modules : A dictionary containing the names of all the modules available, name of module (key) and module.ini file path (value)
        @author oldgod

        @note please give unique names to the modules, duplicate names can cause issues with the modules loading.
    '''
    info("Checking if the module name is a string or is not an empty string")
    if not isinstance(module_name, str) or len(module_name) == 0:
        error("Module name value is either not a string or is empty")
        return # fixme: add the code for raising a custom exception

    info("Checking if the modules is a set or not")
    if not isinstance(modules, dict):
        error(f"Modules value is not a dict")
        return # fixme: add the code for raising a custom exception

    # remove the brackets from the module name
    module_name = module_name.strip("]")
    module_name = module_name.strip("[")
    module_name = module_name.strip("'")
    debug(f"Module name provided : {repr(module_name)}")

    match module_name:
        case "services":
            # fixme: Add the code for reading the module specific configuration file
            service_config = ModuleConfig()
            service_config.name = "services"
            ConfigContainer["services"] = service_config
            host = service_config.get_config(section_name="config", option_name="host", config_file_path=modules.get(module_name))
            port = int(service_config.get_config(section_name="config", option_name="port", config_file_path=modules.get(module_name)))
            workers = int(service_config.get_config(section_name="config", option_name="workers", config_file_path=modules.get(module_name)))
            if module_name in modules:
                debug("Service module will be started")

                if root.level == DEBUG:
                    uvrun(f"{module_name}:app", host=host, port=port, workers=workers, reload=True)
                else:
                    uvrun(f"{module_name}:app", host=host, port=port, workers=workers, reload=False)

        case _:
            error(f"Unknown module : {module_name} specifed to be started")
