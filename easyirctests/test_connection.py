
# -*- coding: utf-8 -*-
import time
import pytest
from easyirc.connection import DispatchConnection, CallbackConnection, EventHookConnection
from easyirc.command import protocol
from easyirc.event import EventManager
from easyirc.const import *
from easyirc import util
from mocksocket import MockSocket

from test_socket import socktypes, test_create

import settings
connop = settings.TEST_CONNECTION


@pytest.mark.parametrize(['SocketType'], socktypes)
def test_dispatch(SocketType):
    print SocketType

    connection = DispatchConnection(None, protocol.manager)
    msg = connection.dispatch()
    assert msg == CREATED
    connection.socket = test_create(SocketType)
    connection.connect()

    connection.start()
    msg = connection.dispatch()
    assert msg == CONNECTED

    def check_msg(themsg):
        while True:
            time.sleep(0.1)
            msg = connection.dispatch()
            if msg is None: continue
            parts = util.msgsplit(msg)
            if parts.type == PING:
                connection.pong(parts[1])
                continue
            if parts.type == themsg:
                break
            else:
                print msg

    connection.nick(connop['nick'])
    connection.user(connop['nick'], 'Bot by EasyIRC')
    check_msg('375')

    connection.join(connop['autojoins'][0])
    check_msg(JOIN)

    connection.part(connop['autojoins'][0])
    check_msg(PART)

    connection.quit(u'QUIT MESSAGE')
    check_msg('ERROR')
    connection.disconnect()
    connection.thread.join()


@pytest.mark.parametrize(['SocketType'], socktypes)
def test_callback(SocketType):
    print SocketType

    def callback(connection, m):
        ps = util.msgsplit(m)
        chan = connop['autojoins'][0]
        if m == CREATED:
            connection.socket = test_create(SocketType)
            connection.connect()
        elif m == CONNECTED:
            connection.nick(connop['nick'])
            connection.user(connop['nick'], 'Bot by EasyIRC')
        elif ps.type == PING:
            connection.pong(ps[1])
        elif ps.type == '375':
            connection.join(chan)
        elif ps.type == JOIN:
            connection.privmsg(chan, u'test the 콜백')
            connection.quit(u'전 이만 갑니다')
        elif ps.type == 'ERROR':
            print 'END!'
            connection.disconnect()
        else:
            print m

    connection = CallbackConnection(callback, protocol.manager)
    connection.start()
    connection.thread.join()


event = EventManager()
chan = connop['autojoins'][0]
@event.hookmsg(CREATED)
def created(connection, sender):
    print 'created?', connection
    connection.socket = event.socket
    connection.connect()

@event.hookmsg(CONNECTED)
def connected(connection, sender):
    print 'connected?', connection
    connection.nick(connop['nick'])
    connection.user(connop['nick'], 'Bot by EasyIRC')

@event.hookmsg(PING)
def ping(connection, sender, tag):
    print 'ping? pong!', connection
    connection.pong(tag)

@event.hookmsg('375')
def msgofday(connection, sender, *args):
    print 'message of the day!', connection
    connection.join(chan)

@event.hookmsg(JOIN)
def join(connection, sender, *args):
    print 'joined?', connection
    connection.privmsg(chan, u'test the 이벤트훅')
    connection.quit(u'전 이만 갑니다')

@event.hookmsg('ERROR')
def error(connection, sender, *args):
    print 'error?!', connection
    connection.disconnect()


@pytest.mark.parametrize(['SocketType'], socktypes)
def test_dispatch_event(SocketType):
    event.socket = test_create(SocketType)
    connection = DispatchConnection(event, protocol.manager)
    connection.start()
    while connection.thread.is_alive():
        connection.handle_message()
    connection.thread.join()

@pytest.mark.parametrize(['SocketType'], socktypes)
def test_eventhook(SocketType):
    event.socket = test_create(SocketType)
    connection = EventHookConnection(event, protocol.manager)
    connection.start()
    connection.thread.join()


if __name__ == '__main__':
    test_dispatch(socktypes[0][0])
    #test_dispatch(socktypes[1][0])
    test_callback(socktypes[0][0])
    #test_callback(socktypes[1][0])
    test_eventhook(socktypes[0][0])
    #test_eventhook(socktypes[1][0])
