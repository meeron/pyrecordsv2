import json
from os import path
from enum import Enum
from security import Passwd

class OpenDbStaus(Enum):
    success = 0
    not_found = 1
    invalid_password = 2

class OpenDbResult(object):
    def __init__(self, status, workers=None):
        self.status = status
        self.workers = workers

class Storage(object):
    def __init__(self, dbFile, password):
        self._passwd = Passwd(password)
        self._dbFile = path.expanduser(dbFile)

    def open(self):
        if not path.isfile(self._dbFile):
            return OpenDbStaus.not_found

        with open(self._dbFile, "rb") as f:
            json_content = self._passwd.decrypt(f.read())

        if json_content is None:
            return OpenDbStaus.invalid_password

        #TODO: read data from json content

        return OpenDbStaus.success
