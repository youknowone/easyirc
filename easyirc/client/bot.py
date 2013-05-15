
from ..event import EventManager, bot
from . import BasicClient

class BotClient(BasicClient):
    pass

BotClient._events = _e = EventManager()
_e.extends(BasicClient._events)
_e.extends(bot.manager)
_e.msgprefix = bot.msgprefix
_e.msgregex = bot.msgregex
