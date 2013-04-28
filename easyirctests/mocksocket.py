
# -*- coding: utf-8 -*-
from easyirc import util
from easyirc.const import *
from easyirc.socket import Socket

class MockSocket(Socket):
    def create_socket(self):
        self.socket = MockServerSocket()
        self.msgqueue = [CREATED] # EVERYTHING-IS-RESPONSE!
        self.recvbuffer = ''

    def connect(self):
        self.msgqueue.append(CONNECTED) # EVERYTHING-IS-RESPONSE!

    def put(self, line):
        self.recvbuffer += line

    def putln(self, line):
        self.put(line + '\r\n')


class MockServerSocket(object):
    def __init__(self):
        self.buff = ''

    def connect(self, addr):
        self.buff += ':localhost NOTICE Auth :*** Looking up your hostname...\r\n'

    def send(self, line):
        cmds = line.split(' ')
        table = {
            'PING': ':localhost PONG ' + cmds[1],
            'USER': ':localhost 375 the day of message',
            'JOIN': ':localhost JOIN :blah',
            'PART': ':localhost PART :blah',
        }
        if cmds[0] in table:
            self.buff += table[cmds[0]] + '\r\n'

    def recv(self, size):
        buff = self.buff
        self.buff = ''
        return buff


