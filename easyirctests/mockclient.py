
from easyirc.client import BaseClient
from mocksocket import Socket

class MockCommandSocket(Socket):
    def __init__(self):
        self.sends = []

    def send(self, line):
        self.sends.append(line)


class MockCommandClient(BaseClient):
    def __init__(self, eventmanager, cmdmanager):
        BaseClient.__init__(self, eventmanager, cmdmanager)

        self.cmdbuffer = []
        self.socket = MockCommandSocket()
