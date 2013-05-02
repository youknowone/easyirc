
from easyirc.connection import BaseConnection
from mocksocket import Socket

class MockCommandSocket(Socket):
    def __init__(self):
        self.sends = []

    def send(self, line):
        self.sends.append(line)


class MockCommandConnection(BaseConnection):
    def __init__(self, eventmanager, cmdmanager):
        BaseConnection.__init__(self, eventmanager, cmdmanager)

        self.cmdbuffer = []
        self.socket = MockCommandSocket()
