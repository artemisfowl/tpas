'''
    @brief services module component containing all the constants to be used by respective module
    @author oldgod
'''

from enum import Enum
from platform import architecture

DEFAULT_BROWSER = "chrome"
DEFAULT_DRIVER_BINARY = "services/driver/chromedriver"

# note: this URL will be used to query the most recent version of driver present -
# the following constants can be used later for enhancements
DEFAULT_LATEST_DRIVER_URL = "https://github.com/mozilla/geckodriver/releases/latest"
DEFAULT_BROWSER_DRIVER_BASE_URL = "https://github.com/mozilla/geckodriver/releases/download/{}/geckodriver-{}-{}.{}"

DEFAULT_BROWSER_REMOTE_CONTROL_MODE = "--remote-debugging-port"

DEFAULT_ADMIN_USER = "oldgod"
DEFAULT_ADMIN_PASSWORD = "oldgod"

# fixme: add proper documentation strings for enum constants
class TestType(Enum):
    UI = 100
    SHELL = 200
    MISC = 300
    NONE = 1000

class UiActionType(Enum):
    CLICK = 10              # CLICK and LEFT_CLICK are basically the same
    LEFT_CLICK = 100        # this is just an overzealous identification
    RIGHT_CLICK = 200
    MIDDLE_CLICK = 300
    DRAG_N_DROP = 400
    SCROLL = 500
    TYPE = 600

EXIT_SUCCESS = 0
EXIT_FAILURE = -1
