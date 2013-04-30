
# -*- coding: utf-8 -*-
import pytest

from easyirc import util
from easyirc.socket import Socket

import settings

from mocksocket import *

@pytest.mark.parametrize(['line', 'items'], [
    [':localhost PING :thepingstring', ['localhost', 'PING', 'thepingstring']],
    ['PRIVMSG #chan nick :this is the msg', [None, 'PRIVMSG', '#chan', 'nick', 'this is the msg']],
])
def test_msgsplit(line, items):
    splited = util.msgsplit(line)
    assert splited == items

socktypes = [[MockSocket]]
if settings.TEST_REALSERVER:
    socktypes.append([Socket])

@pytest.mark.parametrize(['SocketType'], [
    [Socket],
    [MockSocket],
])
def test_create(SocketType):
    connop = settings.TEST_CONNECTION
    addr = (connop['host'], connop['port'])
    sock = SocketType(addr, 'utf-8')
    assert sock.dispatch() is None
    return sock

@pytest.mark.parametrize(['SocketType'], socktypes)
def test_enqueue(SocketType):
    print SocketType

    sock = test_create(SocketType)
    sock.connect()
    for msg in sock.dispatch_all():
        print msg
        assert msg == 'CONNECTED'
    assert sock.dispatch() is None

    def dispatch_useful():
        print '--> throwing out unusefuls'
        for msg in sock.dispatch_all():
            msg = util.msgsplit(msg)
            print 'type:', msg.type, 'msg:', u' '.join(msg).encode('utf-8')
            if msg.type == PING:
                sock.cmd(PONG, msg[1])
                continue
            if msg.type == PRIVMSG:
                continue
            if msg.type == '375':
                break
            if len(msg.type) == 3 or msg.type in [NOTICE, MODE]:
                continue
            else:
                break
        else:
            print '<-- skipped all the trashes'
            return None
        print '<-- get a message'
        return msg

    sock.cmd('NICK', 'easybot')
    sock.cmdl('USER', 'easybot', 'localhost', '0', 'realname')

    msg = None
    while msg is None:
        sock.recv()
        msg = dispatch_useful()
    assert msg.type == '375' # message of the day - for the registered user only

    connop = settings.TEST_CONNECTION
    chan = connop['autojoins'][0]
    sock.cmd(JOIN, chan)
    msg = None
    while msg is None:
        sock.recv()
        msg = dispatch_useful()
    assert msg.type == JOIN
    sock.cmdl(PRIVMSG, chan, 'can you see my message?')
    sock.cmdl(PRIVMSG, chan, u'can you see my 한글 message?')
    sock.cmdl(PART, chan, u'test did end with non-ascii 한글')
    msg = None
    while msg is None:
        sock.recv()
        msg = dispatch_useful()
    assert msg.type == 'PART'

if __name__ == '__main__':
    test_enqueue(MockSocket)
    if settings.TEST_REALSERVER:
        test_enqueue(Socket)
