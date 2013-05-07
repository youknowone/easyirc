
import traceback
from collections import OrderedDict

from ..const import *
from . import EventManager, BaseHandler
from ..model import DataDict, Channel, User
from .. import util, settings


manager = EventManager()

@manager.hookmsg(INVITE)
def on_invite(connection, sender, target, channel):
    connopt = settings.connections[connection.name]
    if connopt.invite not in ['allow', 'admin']:
        return
    if connopt.invite == 'admin' and not connopt.is_admin(sender):
        return
    connection.join(channel)


class BaseBotCommandManager(BaseHandler):
    def __init__(self, handlers=None):
        self.handlers = handlers if handlers is not None else OrderedDict()

    def extends(self, events):
        if isinstance(events, EventManager):
            events = events.handlers
        self.handlers += events

    # decorators
    def hook(self, pattern):
        def decorator(action):
            self.handlers[pattern] = action
            return action
        return decorator

    def hookback(self, pattern):
        def decorator(action):
            def on_event(connection, manager, sender, msgtype, target, prefix, message=None):
                result = action(message)
                if not result:
                    return
                result = unicode(result)
                connection.sendl(msgtype, target, result)
            self.handlers[pattern] = on_event
            return on_event
        return decorator


class PrefixBotCommandManager(BaseBotCommandManager):
    def __init__(self, prefix, handlers=None):
        BaseBotCommandManager.__init__(self, handlers)
        self.prefix = prefix

    def __call__(self, connection, line):
        ln = util.msgsplit(line)
        msg = ln[-1]
        if not msg.startswith(self.prefix):
            return False
        parts = msg.split(' ', 1)
        prefix = parts[0][len(self.prefix):]
        try:
            action = self.handlers[prefix]
        except KeyError:
            return

        try:
            action(*([connection, self] + ln[:-1] + parts))
        except:
            traceback.print_exc()


msgprefix = PrefixBotCommandManager('/') # change me!
manager.hook(msgprefix)

@msgprefix.hook('help')
def on_help(connection, manager, sender, msgtype, target, prefix, message=None):
    items = u' '.join(manager.handlers.keys())
    connection.sendl(msgtype, target, items)
