
from ..const import *
from . import EventManager
from ..model import DataDict, Channel, User

manager = EventManager()

@manager.hookmsg(PING)
def on_ping(client, sender, tag):
    client.pong(tag)

@manager.hookmsg(CONNECTED)
def on_connected(client, sender):
    client.welcome = u''
    client.identifier = u''
    client.loaded = False
    client.channels = DataDict()

@manager.hookmsg(RPL_WELCOME)
def on_welcome(client, *args):
    welcome = args[-1]
    client.identifier = welcome.rsplit(' ', 1)[-1]
    client.enqueue(LOADED)

@manager.hookmsg(JOIN)
def on_join(client, sender, channel):
    if not channel in client.channels:
        client.channels.add(Channel(channel))

