
from . import CommandManager

manager = CommandManager()

@manager.override
def run(client, super, *args):
    try:
        super(client, *args)
    except KeyError:
        client.connection.cmd(*args)

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
def quitall(client, message=None):
    for connection in client.values():
        connection.quit(message)

@manager.command
def println(client, *args):
    print ' '.join(map(str, args))
