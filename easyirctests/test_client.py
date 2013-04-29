
# -*- coding: utf-8 -*-
import time
import pytest
from easyirc.client import DispatchClient, CallbackClient, EventHookClient
from easyirc.command import protocol
from easyirc.const import *
from easyirc import util
from mocksocket import MockSocket

from test_socket import socktypes, test_create

import settings
connop = settings.TEST_CONNECTION


@pytest.mark.parametrize(['SocketType'], socktypes)
def test_dispatch(SocketType):
    print SocketType

    socket = test_create(SocketType)
    client = DispatchClient(socket, protocol.manager)
    msg = client.dispatch()
    client.connect()

    client.start()
    msg = client.dispatch()
    assert msg == CONNECTED

    def check_msg(themsg):
        while True:
            time.sleep(0.1)
            msg = client.dispatch()
            if msg is None: continue
            parts = util.cmdsplit(msg)
            if parts.cmd == PING:
                client.pong(parts[1])
                continue
            if parts.cmd == themsg:
                break
            else:
                print msg

    client.nick(connop['nick'])
    client.user(connop['nick'], 'Bot by EasyIRC')
    check_msg('375')

    client.join(connop['autojoins'][0])
    check_msg(JOIN)

    client.part(connop['autojoins'][0])
    check_msg(PART)

    client.quit(u'QUIT MESSAGE')
    check_msg('ERROR')
    client.disconnect()
    client.thread.join()


@pytest.mark.parametrize(['SocketType'], socktypes)
def test_callback(SocketType):
    print SocketType

    def callback(client, m):
        ps = util.cmdsplit(m)
        chan = connop['autojoins'][0]
        if m == CREATED:
            client.socket = test_create(SocketType)
            client.connect()
        elif m == CONNECTED:
            client.nick(connop['nick'])
            client.user(connop['nick'], 'Bot by EasyIRC')
        elif ps.cmd == PING:
            client.pong(ps[1])
        elif ps.cmd == '375':
            client.join(chan)
        elif ps.cmd == JOIN:
            client.privmsg(chan, u'test the 콜백')
            client.quit(u'전 이만 갑니다')
        elif ps.cmd == 'ERROR':
            print 'END!'
            client.disconnect()
        else:
            print m

    client = CallbackClient(callback, protocol.manager)
    client.start()
    client.thread.join()


@pytest.mark.parametrize(['SocketType'], socktypes)
def test_eventhook(SocketType):
    client = EventHookClient(protocol.manager)
    chan = connop['autojoins'][0]

    @client.hookmsg(CREATED)
    def created(client):
        print 'created?', client
        client.socket = test_create(SocketType)
        client.connect()

    @client.hookmsg(CONNECTED)
    def connected(client):
        print 'connected?', client
        client.nick(connop['nick'])
        client.user(connop['nick'], 'Bot by EasyIRC')

    @client.hookmsg(PING)
    def ping(client, tag):
        print 'ping? pong!', client
        client.pong(tag)

    @client.hookmsg('375')
    def msgofday(client, *args):
        print 'message of the day!', client
        client.join(chan)

    @client.hookmsg(JOIN)
    def join(client, *args):
        print 'joined?', client
        client.privmsg(chan, u'test the 이벤트훅')
        client.quit(u'전 이만 갑니다')

    @client.hookmsg('ERROR')
    def error(client, *args):
        print 'error?!', client
        client.disconnect()

    client.start()
    client.thread.join()

if __name__ == '__main__':
    #test_dispatch(socktypes[0][0])
    #test_dispatch(socktypes[1][0])
    #test_callback(socktypes[0][0])
    #test_callback(socktypes[1][0])
    test_eventhook(socktypes[0][0])
    test_eventhook(socktypes[1][0])
