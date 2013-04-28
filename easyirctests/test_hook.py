
import pytest

from easyirc import util
from easyirc.const import *
from easyirc.hook import BaseHook, ConditionalHook, ExceptionHook, MessageHook

class PingHook(BaseHook):
    def run(self, client, message):
        if not isinstance(message, unicode):
            return False
        items = util.cmdsplit(message)
        if items.cmd == PING:
            client.cmd(PONG, items[1])
            return True
        return False


ping_base = PingHook()

def cond_conditional(client, message):
    if not isinstance(message, unicode):
        return False
    items = util.cmdsplit(message)
    return items.cmd == PING

def pong_conditional(client, message):
    items = util.cmdsplit(message)
    client.cmd(PONG, items[1])
    return True

ping_conditional = ConditionalHook(cond_conditional, pong_conditional)

def pong_command(client, message):
    client.cmd(PONG, message[1])
    return True

ping_command = MessageHook(PING, pong_command)


@pytest.mark.parametrize(['hook', 'ping'], [
    [ping_base, u'JFIOSJIEF'],
    [ping_conditional, u'한글핑'],
    [ping_command, u'()@#RJIOEW'],
])
def test_hook(hook, ping):
    class Client(object):
        def __init__(self):
            self.pong = False
        def cmd(self, *args):
            self.pong = args[1]

    client = Client()
    consumed = hook.run(client, 'PING :' + ping)
    assert True == consumed
    assert client.pong == ping