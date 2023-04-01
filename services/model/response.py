'''
    @brief model module component containing the class for a response from API
    @author oldgod
'''

class ResponseCode:
    '''
        @brief class containing the custom response codes for the API(s)
        @author oldgod

        @note All success codes should start with 2 and contain at least one 0
        all failure codes should start with 1 and contain at least one 0
    '''
    SUCCESS = 200
    FAILURE = 100

class ResponseMessage:
    '''
        @brief class containing the custom message for the API(s)
        @author oldgod
    '''
    SUCCESS = "succeeded"
    FAILURE = "failed"
    DEFAULT = "default-mesage"

class Response:
    '''
        @brief class containing the response details when API(s) will be hit
        @author oldgod
    '''
    def __init__(self, code: int, message: str) -> None:
        '''
            @brief default constructor for Response class
            @param code : integer containing the ResponseCode
            message: string containing the message of the response
        '''
        self._code = ResponseCode.SUCCESS if code is None else code
        self._message = ResponseMessage.DEFAULT if message is None else message

    def update(self, code: int=0, message: str=ResponseMessage.DEFAULT):
        if self._code != code:
            self._code = code
        if self._message != message:
            self._message = message
