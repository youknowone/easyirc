
import pytest

from microirc import util
from microirc.hook import BaseHook, ConditionalHook, ExceptionHook, CommandHook

class PingHook(BaseHook):
    def run(self, client, message):
        if not isinstance(message, unicode):
            return False
        items = util.split(message)
        if items.cmd == 'ping':
            client.cmd('PONG', items[1])
            return True
        return False


ping_base = PingHook()

def cond_conditional(client, message):
    if not isinstance(message, unicode):
        return False
    items = util.split(message)
    return items.cmd == 'ping'

def pong_conditional(client, message):
    items = util.split(message)
    client.cmd('PONG', items[1])
    return True

ping_conditional = ConditionalHook(cond_conditional, pong_conditional)

def pong_command(client, message):
    client.cmd('PONG', message[1])
    return True

ping_command = CommandHook('ping', pong_command)


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