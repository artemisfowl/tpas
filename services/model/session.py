'''
    @brief Session file containing the routines for all kind of session management
    @author oldgod
'''

class SessionManager:
    def __init__(self) -> None:
        self.uuid = str()
        self.name = str()

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, value: str):
        self._uuid = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

