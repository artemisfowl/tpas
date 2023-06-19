'''
    @brief services module component containing all the constants to be used by respective module
    @author oldgod
'''

from enum import Enum
from platform import architecture

DEFAULT_BROWSER = "firefox"
# fixme: add the default driver binary location to this constant - DEFAULT_DRIVER_BINARY
# append to this the home location and the location of the file or module
DEFAULT_DRIVER_BINARY = "services/driver/geckodriver"

# note: this URL will be used to query the most recent version of driver present -
# the following constants can be used later for enhancements
DEFAULT_LATEST_DRIVER_URL = "https://github.com/mozilla/geckodriver/releases/latest"
DEFAULT_BROWSER_DRIVER_BASE_URL = "https://github.com/mozilla/geckodriver/releases/download/{}/geckodriver-{}-{}.{}"
DEFAULT_BROWSER_REMOTE_CONTROL_MODE = "--marionette"

DEFAULT_ADMIN_USER = "oldgod"
DEFAULT_ADMIN_PASSWORD = "oldgod"

class TestType(Enum):
    UI = 100
    SHELL = 200
    MISC = 300
    NONE = 1000

EXIT_SUCCESS = 0
EXIT_FAILURE = -1
