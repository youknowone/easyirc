
import pytest

from mockcommand import MockCommandManager
from easyirc.command import protocol

from mocksocket import *

manager = MockCommandManager(None, protocol.commands)

@pytest.mark.parametrize(['line', 'result'], [
    [u'ping test', u'PING test'],
    [u'privmsg #channel :message send', u'PRIVMSG #channel :message send'],
    [u'part #channel thereason', u'PART #channel :thereason'],
    [u'part #channel', u'PART #channel'],
])
def test_putln(line, result):
    manager.putln(line)
    pop = manager.cmdbuffer.pop()
    assert pop == result

@pytest.mark.parametrize(['items', 'result'], [
    [(u'ping', u'test'), u'PING test'],
    [(u'privmsg', u'#channel', u'message send'), u'PRIVMSG #channel :message send'],
    [(u'part', u'#channel', u'thereason'), u'PART #channel :thereason'],
    [(u'part', u'#channel'), u'PART #channel'],
])
def test_put(items, result):
    manager.put(items)
    pop = manager.cmdbuffer.pop()
    assert pop == result


