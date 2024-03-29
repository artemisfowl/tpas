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

    # required values
    name: str
    test_type: str

class EndTestRequest(BaseModel):
    # required values
    uuid: str

    # optional value [to be added later]

class FileUploadRequest(BaseModel):
    # required values
    destination_dir: str

    # optional values [will be added later]

class AdminRequest(BaseModel):
    # required values
    admin_user: str
    admin_password: str

    # optional values [tobe added later]

class NavigationRequest(BaseModel):
    # required values
    uuid: str
    url: str

    # optional values
    open_in_new_tab: bool = False

class UiRequest(BaseModel):
    # required values
    uuid: str

    # optional values
    by: str = ""
    locator: str = ""
    url: str = ""
    action: str = ""
    value: str = ""

class ShellRequest(BaseModel):
    # required values
    uuid: str
    command: str    # Note: this command should also contain the arguments to be passed to the actual command

    # optional values
    persistent: bool = False # Note: if this is enabled, every time the API is called, it will store the command and then perform all the
    # command before sending out the last shell command output
