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
    admin_user: str = ""
    admin_password: str = ""
    test_type: str = TestType.NONE.name

    # required values [to be added later]
