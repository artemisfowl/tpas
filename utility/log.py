'''
    @brief Utility module component containing the details and functions for logging functionality
    @author oldgod
'''

from logging import getLogger

# fixme: check if it is better to use a class or a simple function should do
class Scribe:
    '''
        @brief Scribe class responsible for logging details
        @author oldgod
    '''
    def __init__(self) -> None:
        self._logger = getLogger()
