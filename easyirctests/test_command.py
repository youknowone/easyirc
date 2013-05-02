
import pytest

from mockconnection import MockCommandConnection
from easyirc.command import protocol

from mocksocket import *

connection = MockCommandConnection(None, protocol.manager)

@pytest.mark.parametrize(['line', 'result'], [
    [u'ping test', u'PING test'],
    [u'privmsg #channel :message send', u'PRIVMSG #channel :message send'],
    [u'part #channel thereason', u'PART #channel :thereason'],
    [u'part #channel', u'PART #channel'],
])
def test_cmdln(line, result):
    connection.cmdln(line)
    pop = connection.socket.sends.pop()
    assert pop == result + u'\r\n'

@pytest.mark.parametrize(['items', 'result'], [
    [(u'ping', u'test'), u'PING test'],
    [(u'privmsg', u'#channel', u'message send'), u'PRIVMSG #channel :message send'],
    [(u'part', u'#channel', u'thereason'), u'PART #channel :thereason'],
    [(u'part', u'#channel'), u'PART #channel'],
])
def test_cmd(items, result):
    connection.cmd(*items)
    pop = connection.socket.sends.pop()
    assert pop == result + u'\r\n'


