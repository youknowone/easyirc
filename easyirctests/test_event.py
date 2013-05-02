
# -*- coding: utf-8 -*-
import pytest

from easyirc import util
from easyirc.const import *
from easyirc.event import EventManager, BaseHandler, ConditionalHandler, ExceptionHandler, MessageHandler

class PingHandler(BaseHandler):
    def run(self, connection, message):
        if not isinstance(message, unicode):
            return False
        items = util.cmdsplit(message)
        if items.cmd == PING:
            connection.cmd(PONG, items[1])
            return True
        return False


ping_base = PingHandler()

def cond_conditional(connection, message):
    if not isinstance(message, unicode):
        return False
    items = util.cmdsplit(message)
    return items.cmd == PING

def pong_conditional(connection, message):
    items = util.cmdsplit(message)
    connection.cmd(PONG, items[1])
    return True

ping_conditional = ConditionalHandler(cond_conditional, pong_conditional)

def pong_message(connection, sender, message):
    connection.cmd(PONG, message)
    return True

ping_message = MessageHandler(PING, pong_message)


@pytest.mark.parametrize(['hook', 'ping'], [
    [ping_base, u'JFIOSJIEF'],
    [ping_conditional, u'한글핑'],
    [ping_message, u'()@#RJIOEW'],
])
def test_hook(hook, ping):
    class Connection(object):
        def __init__(self):
            self.pong = False
        def cmd(self, *args):
            self.pong = args[1]

    connection = Connection()
    consumed = hook.run(connection, 'PING :' + ping)
    assert True == consumed
    assert connection.pong == ping
