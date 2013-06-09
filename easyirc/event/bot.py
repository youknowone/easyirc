
import re
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


class BotEventContext(object):
    def __init__(self, manager, connection, ident, msgtype, target, **kwargs):
        self.manager = manager
        self.connection = connection
        self.ident = ident
        self.msgtype = msgtype
        self.target = target
        for k, v in kwargs.items():
            setattr(self, k, v)

    def reply(self, *msgs):
        msg = u' '.join([unicode(msg) for msg in msgs])
        self.connection.sendl(self.msgtype, self.target, msg)

    @property
    def nick(self):
        return self.ident.nick

class BaseBotCommandManager(BaseHandler):
    def __init__(self, handlers=None):
        self.handlers = handlers if handlers is not None else OrderedDict()

    def extends(self, events):
        if isinstance(events, EventManager):
            events = events.handlers
        self.handlers += events


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

        sender, msgtype, target = ln[0], ln[1], ln[2]
        sender = util.parseid(sender)
        if target[0] not in ('#', '&', '%'):
            target = sender.nick

        context = BotEventContext(self, connection, sender, msgtype, target, prefix=parts[0])

        try:
            action(context, parts[1] if len(parts) > 1 else None)
        except:
            traceback.print_exc()

    def hook(self, *prefixes):
        def decorator(action):
            def on_event(context, message=None):
                action(context, message)
            on_event.__doc__ = action.__doc__
            for prefix in prefixes:
                self.handlers[prefix] = on_event
            return action
        return decorator

    def hookback(self, *prefixes):
        def decorator(action):
            def on_event(context, message=None):
                result = action(context, message)
                if not result:
                    return
                context.reply(result)
            on_event.__doc__ = action.__doc__
            for prefix in prefixes:
                self.handlers[prefix] = on_event
            return action
        return decorator


class RegexBotCommandManager(BaseBotCommandManager):
    def __init__(self, handlers=None):
        self.handlers = [] if handlers is None else handlers

    def __call__(self, connection, line):
        ln = util.msgsplit(line)

        msg = ln[-1]

        sender, msgtype = ln[0], ln[1]
        sender = util.parseid(sender)
        if len(ln) > 2:
            target = ln[2]
            if target[0] not in ('#', '&', '%'):
                target = sender.nick
        else:
            target = None

        context = BotEventContext(self, connection, sender, msgtype, target)

        for regex, action in self.handlers:
            m = re.search(regex, msg)
            if m is None: continue

            action(context, msg, *m.groups())

    def hook(self, pattern):
        def decorator(action):
            def on_event(context, msg, *regexargs):
                action(context, msg, *regexargs)
            on_event.__doc__ = action.__doc__
            self.handlers.append((pattern, on_event))
            return action
        return decorator

    def hookback(self, pattern):
        def decorator(action):
            def on_event(context, msg, *regexargs):
                result = action(context, msg, *regexargs)
                if not result:
                    return
                context.reply(result)
            on_event.__doc__ = action.__doc__
            self.handlers.append((pattern, on_event))
            return action
        return decorator


msgprefix = PrefixBotCommandManager('/') # change me!
manager.hook(msgprefix)
msgregex = RegexBotCommandManager()
manager.hook(msgregex)

@msgprefix.hook('help')
def on_help(context, message=None):
    """Show help/description of given command"""
    if message is None:
        items = u' '.join(context.manager.handlers.keys())
        context.reply(items)
    else:
        try:
            handler = context.manager.handlers[message]
        except KeyError:
            context.reply(u'"{}" is not a command'.format(message))
        if handler.__doc__:
            context.reply(handler.__doc__.decode('utf-8'))
        else:
            context.reply(u'"{}" has no help'.format(message))

