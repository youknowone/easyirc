
# -*- coding: utf-8 -*-
from easyirc.client.bot import BotClient
from easyirc.storage import make_storage
from easyirc.const import *
from easyirc import util

client = BotClient()
client.events.msgprefix.prefix = '.'

nicks = make_storage('nicks.json', 'nickmark')
if not nicks.known:
    nicks.known = []

@client.events.hookmsg(JOIN)
def on_join(connection, sender, target):
    identity = util.parseid(sender)
    nick = identity.nick
    if not nick in nicks.known:
        connection.privmsg(target, u'Hello, new user! ' + nick)
        nicks.known.append(nick)
        nicks._commit()

@client.events.msgprefix.hookback('sayback')
def on_dic(message=None):
    return message

client.start()

client.interactive()
client.quit(u'Keyboard Interuppt')
