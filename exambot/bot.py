
# -*- coding: utf-8 -*-
from easyirc.client.bot import BotClient

client = BotClient()
client.events.msgprefix.prefix = '.'


@client.events.msgprefix.hookback('sayback')
def on_dic(message=None):
    return message

client.start()

client.interactive()
client.quit(u'Keyboard Interuppt')
