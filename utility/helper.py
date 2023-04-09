'''
    @brief utility module component containing all the functions and classes for performing tasks for run
    @author oldgod
'''

from glob import glob
from sys import version_info, exit
from logging import info, debug, error

from uvicorn import run as uvrun

from .constants import PYVER_MAJOR, PYVER_MINOR

def list_submodules(dir: str) -> list:
    '''
        @brief function to list all the modules present under a specific directory
        @param dir : string containing the root path where all the modules are present
        @author oldgod
    '''

    modules = []

    if dir is None or not isinstance(dir, str) or len(dir) == 0:
        return modules

    # fixme: find the modules available
    result = glob(f"{dir}**/module")
    for module in result:
        module = module[:module.index("module")-1]
        module = module[module.rindex("/")+1:]
        modules.append(module)

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

def run_module(module_name: str, modules: set):
    '''
        @brief function to run the module specified, uses a switcher for any new module created
        @param module_name : String containing the name of the module to be run
            modules : A set containing the names of all the modules available.
        @author oldgod

        @note please give unique names to the modules, duplicate names can cause issues with the modules loading.
    '''
    if not isinstance(module_name, str) or len(module_name) == 0:
        return # fixme: add the code for raising a custom exception
    if not isinstance(modules, set):
        return # fixme: add the code for raising a custom exception

    # fixme: add a switcher based on the most recent change in Python
    # fixme: since this switch matching of Python 3.10 will be used, need to add the python version checking code in this program - should be done at the start

    for module in modules:
        match module:
            case "services":
                # fixme: add the code for taking in the values of host, port and worker number from the constant file - those would be default
                # fixme: add the capacity to accommodate changes as per module requirements
                uvrun(f"{module_name}:app", host="0.0.0.0", port=5000, workers=1)
            case _:
                error("Unknown module : {} specifed")

