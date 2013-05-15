
# -*- coding: utf-8 -*-
"""Test regex command interface"""

from easyirc.client.bot import BotClient

client = BotClient()

@client.events.hookregex('PRIVMSG ([^ ]+) :regex(.*)')
def on_regex(client, chan, msg):
    client.privmsg(chan, u'regex:' + msg)

revent = client.events.msgregex

@revent.hookback('^hello *(.*)')
def on_hello(line, name):
    return u'Hello, {}'.format(name)

client.start()

client.interactive()
client.quit(u'Keyboard Interuppt')
