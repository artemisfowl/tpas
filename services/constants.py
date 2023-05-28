'''
    @brief services module component containing all the constants to be used by respective module
    @author oldgod
'''

from enum import Enum

DEFAULT_BROWSER = "firefox"

DEFAULT_ADMIN_USER = "oldgod"
DEFAULT_ADMIN_PASSWORD = "oldgod"

class TestType(Enum):
    UI = 100
    SHELL = 200
    MISC = 300
    NONE = 1000

EXIT_SUCCESS = 0
EXIT_FAILURE = -1
