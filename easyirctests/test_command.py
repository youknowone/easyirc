
import pytest

from mockclient import MockCommandClient
from easyirc.command import protocol

from mocksocket import *

client = MockCommandClient(protocol.commands)

@pytest.mark.parametrize(['line', 'result'], [
    [u'ping test', u'PING test'],
    [u'privmsg #channel :message send', u'PRIVMSG #channel :message send'],
    [u'part #channel thereason', u'PART #channel :thereason'],
    [u'part #channel', u'PART #channel'],
])
def test_cmdln(line, result):
    client.cmdln(line)
    pop = client.socket.sends.pop()
    assert pop == result + u'\r\n'

@pytest.mark.parametrize(['items', 'result'], [
    [(u'ping', u'test'), u'PING test'],
    [(u'privmsg', u'#channel', u'message send'), u'PRIVMSG #channel :message send'],
    [(u'part', u'#channel', u'thereason'), u'PART #channel :thereason'],
    [(u'part', u'#channel'), u'PART #channel'],
])
def test_cmd(items, result):
    client.cmd(*items)
    pop = client.socket.sends.pop()
    assert pop == result + u'\r\n'


