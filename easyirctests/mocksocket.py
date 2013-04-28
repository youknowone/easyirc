
# -*- coding: utf-8 -*-
import socket
from easyirc import util
from easyirc.const import *
from easyirc.socket import Socket

class MockSocket(Socket):
    def __init__(self, addr=('localhost', 8080), charset='utf-8'):
        Socket.__init__(self, addr, charset)

    def create_socket(self):
        self.socket = MockServerSocket()

    def put(self, line):
        self.recvbuffer += line

    def putln(self, line):
        self.put(line + '\r\n')


class MockServerSocket(object):
    def __init__(self):
        self.buff = ''
        self.connected = False

    def connect(self, addr):
        self.buff += ':localhost NOTICE Auth :*** Looking up your hostname...\r\n'
        self.connected = True

    def send(self, line):
        cmds = line.split(' ')
        table = {
            'PING': ':localhost PONG ' + cmds[1],
            'USER': ':localhost 375 the day of message',
            'JOIN': ':localhost JOIN :blah',
            'PART': ':localhost PART :blah',
            'QUIT': 'ERROR :Closing link: (uname@14.36.48.145) [Quit: message]',
        }
        if cmds[0] in table:
            self.buff += table[cmds[0]] + '\r\n'
        if cmds[0] == 'QUIT':
            self.close()

    def recv(self, size):
        while len(self.buff) == 0:
            if not self.connected:
                raise socket.error(9, 'Bad descriptor')
        buff = self.buff
        self.buff = ''
        return buff

    def shutdown(self, how):
        self.connected = False

    def close(self):
        self.connected = False
