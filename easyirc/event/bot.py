
from ..const import *
from . import EventManager
from ..model import DataDict, Channel, User
from .. import settings

manager = EventManager()

@manager.hookmsg(INVITE)
def on_invite(connection, sender, target, channel):
    connopt = settings.connections[connection.name]
    if connopt.invite not in ['allow', 'admin']:
        return
    if connopt.invite == 'admin' and not connopt.is_admin(sender):
        return
    connection.join(channel)

