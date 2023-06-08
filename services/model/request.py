'''
    @brief request component of model of services, houses the request class
    @author oldgod
'''

from pydantic import BaseModel

from ..constants import TestType

class TestRequest(BaseModel):
    # optional values
    name: str = ""
    uuid: str = ""
    test_type: str = TestType.NONE.name

    # required values [to be added later]

class InitTestRequest(BaseModel):
    # optional values [to be added later]
    latch: bool = False

    # required values
    name: str
    test_type: str

class EndTestRequest(BaseModel):
    # required values
    uuid: str

    # optional value [to be added later]

class AdminRequest(BaseModel):
    # required values
    admin_user: str
    admin_password: str
