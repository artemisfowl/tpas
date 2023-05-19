'''
    @brief Model module initializer
    @author oldgod
'''

# custom module
from .response import Response, TestResponse
from .response import ResponseCode, ResponseMessage
from .request import TestRequest
from .session import SessionManager

test_response = TestResponse(code=ResponseCode.DEFAULT, message=ResponseMessage.DEFAULT)
