
from easyirc.client import BaseClient
from mocksocket import Socket

class MockCommandSocket(Socket):
    def __init__(self):
        self.sends = []

    def send(self, line):
        self.sends.append(line)


class MockCommandClient(BaseClient):
    def __init__(self, commands):
        self.cmdbuffer = []
        self.socket = MockCommandSocket()
        self.commands = commands

        BaseClient.__init__(self)

