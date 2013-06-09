
# -*- coding: utf-8 -*-
"""Example bot code for basic command-based bot using prefix command."""

from easyirc.client.bot import BotClient

# Creates a bot client to write a new bot.
client = BotClient()
pevent = client.events.msgprefix # alias to avoid verbosity

# Change the prefix to '.'
# Now commands are used like: .help .hello .sayback
pevent.prefix = '.'

@pevent.hook('reply')
def on_reply(context, reply='No message to reply'):
    # 'reply' is a convinient tool to reply sender.
    # If message comes from channel, reply to channel. If message comes from
    # user, reply to user.
    # If message is privmsg, reply as privmsg. If message is notice, reply as
    # notice.
    context.reply(reply)

@pevent.hook('ident')
def on_ident(context, message=None):
    # 'ident' is a user identifier in irc protocol.
    # 'ident' consists with parts of identity: nick, username, host
    context.reply('ident:' + context.ident)
    context.reply('nick:' + context.ident.nick)
    context.reply('username:' + context.ident.username)
    context.reply('host:' + context.ident.host)

@pevent.hook('msgtype')
def on_msgtype(context, message=None):
    # 'msgtype' is type of sent message. Usually 'PRIVMSG' or 'NOTICE'
    context.reply('msgtype:' + context.msgtype)

@pevent.hook('target')
def on_target(context, message=None):
    # 'target' is the target to expected to reply. Channel or user.
    context.reply('target:' + context.target)

@pevent.hook('reply2')
def on_reply2(context, message=None):
    # Actually, reply is a shortcut of components of context.
    context.connection.sendl(context.msgtype, context.target, 'Reply by msgtype')
    context.connection.privmsg(context.target, 'Reply by privmsg')
    context.connection.notice(context.target, 'Reply by notice')

# Client starts connection.
client.start()

# Enable interactive command mode (optional)
client.interactive()
client.quit(u'Keyboard Interuppt')
