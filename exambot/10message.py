
# -*- coding: utf-8 -*-
"""Example bot code for basic command-based bot using prefix command."""

# Creates a bot client to write a new bot.
from easyirc.client.bot import BotClient
client = BotClient()

# Creates a simple storage
from easyirc.storage import make_storage
nicks = make_storage('nicks.json', 'nickmark')
# Initializes a list.
if not nicks.known:
    nicks.known = []

from easyirc.const import JOIN # You can use 'JOIN' in simple way.
from easyirc import util


# Message hook of JOIN message
# We will say 'hello' to new nick for this bot.
# About number of params of each message, refer to RFC.
@client.events.hookmsg(JOIN)
def on_join(connection, sender, channel):
    ident = util.parseid(sender) # 'util' has parsers of irc text.
    nick = ident.nick # Got a nick now!
    if not nick in nicks.known:
        # You can use irc protocols-wrapper for connection.
        # See easyirc.command.protocol
        connection.privmsg(channel, u'Hello, new user! ' + nick)
        nicks.known.append(nick)
        nicks._commit() # save to storage


# Client starts connection.
client.start()

# Enable interactive command mode (optional)
client.interactive()
client.quit(u'Keyboard Interuppt')
