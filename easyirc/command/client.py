
from . import CommandManager

manager = CommandManager()

@manager.command
def connectionlist(client):
    client.println(*client.keys())

@manager.command
def connectionswitch(client, server):
    client.selected_connection = client[server]

@manager.command
def quitall(client, message=None):
    for connection in client.values():
        connection.quit(message)

@manager.command
def println(client, *args):
    print args
