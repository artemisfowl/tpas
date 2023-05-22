'''
    @brief Session file containing the routines for all kind of session management
    @author oldgod
'''

class SessionManager:
    '''
        @brief Session Manager class for handling test session
        @author oldgod
    '''
    def __init__(self) -> None:
        '''
            @brief Default constructor for SessionManager class
            @author oldgod
        '''
        self.uuid = str()
        self.name = str()
        self.browser = list()
        self.config = dict()
        self.type = 0 # this needs to be set to the value of a constant

        '''
            @note the type property defines the type of test that is to be initiated. The values as of now could be SYSTEM/UI/MIXED
            SYSTEM - it is 
        '''

    @property
    def config(self):
        '''
            @brief configuration property of the SessionManager
            @author oldgod
        '''
        return self._config

    @config.setter
    def config(self, value: dict):
        '''
            @brief configuration property setter for SessionManager
            @author oldgod
            @param value: Dictionary containing the configuration information for this module
        '''
        self._config = value

    @property
    def browser(self):
        '''
            @brief browser property of SessionManager
            @author oldgod
        '''
        return self._browser

    @browser.setter
    def browser(self, value: list):
        '''
            @brief browser property setter for SessionManager
            @author oldgod
            @param value : List containing the browser information to be used
        '''
        self._browser = value

    @property
    def uuid(self):
        '''
            @brief uuid property of SessionManager
            @author oldgod
        '''
        return self._uuid

    @uuid.setter
    def uuid(self, value: str):
        '''
            @brief uuid property setter of SessionManager
            @author oldgod
            @param value : String containing the UUID
        '''
        self._uuid = value

    @property
    def name(self):
        '''
            @brief name property of SessionManager
            @author oldgod
        '''
        return self._name

    @name.setter
    def name(self, value: str):
        '''
            @brief name property setter of SessionManager
            @author oldgod
            @param value : String containing the name of the test being run
        '''
        self._name = value

