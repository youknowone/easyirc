
from . import CommandManager

manager = CommandManager()

@manager.override
def run(client, super, *args):
    try:
        super(client, *args)
    except KeyError:
        client.connection.cmd(*args)

@manager.command
def println(client, *args):
    print ' '.join(map(str, args))

@manager.command
def start(client):
    for connection in client.values():
        connection.start()

@manager.command
def list(client):
    client.println('connections:', *client.keys())
    if client.connection:
        client.connection.list()

@manager.command
def switch(client, target):
    if target in client:
        client.connection = client[target]
    else:
        client.connection.switch(target)

@manager.command
def quit(client, message=None):
    for connection in client.connections:
        connection.quit(message)

@manager.command
def disconnect(client):
    for connection in client.connections:
        connection.disconnect(message)

@manager.command
def privmsg(client, connection, channel=None, message=None):
    if channel is None and message is None:
        message = connection
        client.connection.privmsg(message)
    elif message is None:
        channel, message = connection, channel
        client.connection.privmsg(channel, message)
    else:
        client[connection].privmsg(channel, message)

@manager.command
def notice(client, connection, channel=None, message=None):
    if channel is None and message is None:
        message = connection
        client.connection.notice(message)
    elif message is None:
        channel, message = connection, channel
        client.connection.notice(channel, message)
    else:
        client[connection].notice(channel, message)
