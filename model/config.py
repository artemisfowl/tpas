'''
    @brief Model module component which contains the models for all types of configuration.
    @author oldgod
'''

from typing import Any, Union
from configparser import ConfigParser

class GeneralConfig:
    '''
        @brief GeneralConfig class for containing the general configuration of the TPAS framework itself
        @author oldgod
    '''
    def __init__(self) -> None:
        '''
            @brief default constructor for GeneralConfig class
            @author oldgod
        '''

        self._parser = ConfigParser()

    def read_config(self, config_file_path: str) -> None:
        '''
            @brief function to read the configuration specified
            @author oldgod
            @params config_file_path : String containing the configuration file path to be read
        '''
        if not isinstance(config_file_path, str) or len(config_file_path) == 0:
            return # fixme: add the code for raising a proper exception

        self._parser.read(config_file_path)

    def get_config(self, section_name: str, option_name: str, config_file_path: str="") -> Union[None,str]:
        '''
            @brief function to get the configuration from an INI file based on the section and option specified
            @author oldgod
            @return Returns either None or a string containing the value
        '''
        if not isinstance(section_name, str) or len(section_name) == 0:
            return None # fixme: add the code for raising a proper exception
        if not isinstance(option_name, str) or len(option_name) == 0:
            return None # fixme: add the code for raising a proper exception
        
        self.read_config(config_file_path=config_file_path)
        return self._parser.get(section_name, option_name)


class ModuleConfig(GeneralConfig):
    def __init__(self, name: Any=None) -> None:
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

