'''
    @brief Utility module component containing the details and functions for logging functionality
    @author oldgod
'''

from os import getcwd, sep
from datetime import datetime
from logging import INFO, getLogger, Formatter, FileHandler, StreamHandler, DEBUG

# fixme: check if it is better to use a class or a simple function should do
class Scribe:
    '''
        @brief Scribe class responsible for logging details
        @author oldgod
    '''
    def __init__(self, ilogdir: str="", enable_file: bool=True, enable_stream: bool=False, enable_debug: bool=False) -> None:
        self._logger = getLogger()
        self._log_format = Formatter("%(asctime)s : <%(threadName)-12.12s>" +
			"(%(levelname)-5.5s) " +
			"-: %(filename)s:%(lineno)s - %(funcName)s() :-" +
			" %(message)s")

        self._logdir = f"{getcwd()}{sep}logs{sep}{str(datetime.now().date()).replace('-', '_')}_tpas.log" if len(ilogdir) == 0 else ilogdir

        # fixme: Add the functionality for checking the logs in a web format so that one can check the logs in a browser
        self._fhandler = FileHandler(self._logdir) # note: this will be responsible for writing to a file
        self._fhandler.setFormatter(self._log_format)

        self._shandler = StreamHandler() # note: this will be responsible for writing the logs to the stream
        self._shandler.setFormatter(self._log_format)

        if enable_file:
            self._logger.addHandler(self._fhandler)
        if enable_stream:
            self._logger.addHandler(self._shandler)

        if enable_debug:
            self._logger.setLevel(DEBUG)
        else:
            self._logger.setLevel(INFO)

    def set_log_file(self, log_file_path: str):
        if not isinstance(log_file_path, str) or len(log_file_path) == 0:
            return # fixme: this should not return the control, rather should be raising a custom Exception.
        # fixme: add the module which will house the custom exceptions
        # fixme: also think about providing the user with the capacity to perform changes on the fly and see the changes getting reflected
        self._logdir = log_file_path

        # testme: this function should automatically allow for creating a new file handler temporarily

    def set_log_level(self, log_level: int):
        self._logger.setLevel(log_level)
