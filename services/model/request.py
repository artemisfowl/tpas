'''
    @brief request component of model of services, houses the request class
    @author oldgod
'''

from pydantic import BaseModel

class TestRequest(BaseModel):
    # optional values
    name: str = ""
    uuid: str = ""
    admin_user: str = ""
    admin_password: str = ""

    # required values [to be added later]
