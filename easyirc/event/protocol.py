
from ..const import *
from . import EventManager
from ..model import DataDict, Channel, User

manager = EventManager()

@manager.hookmsg(PING)
def ping(client, sender, tag):
    client.pong(tag)

@manager.hookmsg(CONNECTED)
def ping(client, sender):
    client.channels = DataDict()

@manager.hookmsg(JOIN)
def join(client, sender, channel):
    if not channel in client.channels:
        client.channels.add(Channel(channel))

