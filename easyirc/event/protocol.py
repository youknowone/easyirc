
import time

from ..const import *
from . import EventManager
from ..model import DataDict, Channel, User
from .. import settings

manager = EventManager()

@manager.hookmsg(PING)
def on_ping(connection, sender, tag):
    connection.pong(tag)

@manager.hookmsg(CONNECTED)
def on_connected(connection, sender):
    connection.welcome = u''
    connection.identifier = u''
    connection.loaded = False
    connection.channels = DataDict()

@manager.hookmsg(RPL_WELCOME)
def on_welcome(connection, *args):
    welcome = args[-1]
    connection.identifier = welcome.rsplit(' ', 1)[-1]
    connection.enqueue(LOADED)

@manager.hookmsg(JOIN)
def on_join(connection, sender, channel):
    if not channel in connection.channels:
        connection.channels.add(Channel(channel))

@manager.hookmsg(ERROR)
def on_error(connection, *args):
    if connection.quitting:
        connection.disconnect()
        return

    if connection.settings.autoreconnect:
        time.sleep(3)
        connection.reconnect()
    else:
        connection.disconnect()

