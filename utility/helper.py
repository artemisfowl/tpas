'''
    @brief utility module component containing all the functions and classes for performing tasks for run
    @author oldgod
'''

from glob import glob

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

