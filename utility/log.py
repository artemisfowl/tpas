'''
    @brief Utility module component containing the details and functions for logging functionality
    @author oldgod
'''

from logging import getLogger, Formatter

# fixme: check if it is better to use a class or a simple function should do
class Scribe:
    '''
        @brief Scribe class responsible for logging details
        @author oldgod
    '''
    def __init__(self) -> None:
        self._logger = getLogger()
        self._log_format = Formatter("%(asctime)s : <%(threadName)-12.12s>" +
			"(%(levelname)-5.5s) " +
			"-: %(filename)s:%(lineno)s - %(funcName)s() :-" +
			" %(message)s")
