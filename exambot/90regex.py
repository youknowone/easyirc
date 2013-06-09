
# -*- coding: utf-8 -*-
"""Example bot code for basic regex-based bot using regular expression.

This is advanced issue.
This is recommended only if you alreasy are familiar with regular expression.
"""

# Creates a bot client to write a new bot.
from easyirc.client.bot import BotClient
client = BotClient()

# General message hook.
# You can hook any message of IRC.
# See RFC to know real message format of IRC.
@client.events.hookregex('PRIVMSG ([^ ]+) :regex(.*)')
def on_regex(connection, message, chan, match):
    """Regex event handler.

    :param connection: Handlable connection to send command.
    :param message: Full matching regex. In this case,
        'PRIVMSG <chan> :regex<yourmessage>'
    :param chan: First group of matching. In this case, matching value of ([^ ]+)
    :param regex: Second group of matching. In this case, matching value of (.*)
    """
    connection.privmsg(chan, u'regex:' + match)
    connection.privmsg(chan, message)


# PRIVMSG/NOTICE message hook.
# You can hook privmsg/notice in easy way.
@client.events.msgregex.hookback('^hello *(.*)')
def on_hello(context, message, name):
    if name:
        return u'Hello, {} and {}'.format(context.nick, name)
    else:
        return u'Hello, {}'.format(context.nick)


# Client starts connection.
client.start()

client.interactive()
client.quit(u'Keyboard Interuppt')
