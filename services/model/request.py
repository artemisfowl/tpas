'''
    @brief request component of model of services, houses the request class
    @author oldgod
'''

from pydantic import BaseModel

class TestRequest(BaseModel):
    name: str | None = None
    uuid: str
