
# -*- coding: utf-8 -*-
"""Example bot code for basic command-based bot using prefix command."""

from easyirc.client.bot import BotClient

# Creates a bot client to write a new bot.
client = BotClient()
pevent = client.events.msgprefix # alias to avoid verbosity

# Change the prefix to '.'
# Now commands are used like: .help .hello .sayback
pevent.prefix = '.'

# 'help' is embedded command. Lists all the prefix commands.

# 'hookback' is used to write simple command.
# When you return a unicode string, it would be reply message of the bot.
@pevent.hookback('hello')
def on_hello(context, message=None):
    # Context includes many informations.
    # For example, you can access nick of sender like context.nick
    return context.nick + u', Hello!'

# 'hook' is a general version of 'hookback'.
# Unlike 'hookback', you should describe your action.
@pevent.hook('sayback')
def on_sayback(context, message=None):
    # Doccomment for 'hook' or 'hookback' will be used for help message for
    # 'help' commend of bot.
    """Reply the given input."""
    # Unlike 'hookback', you should describe action of bot with your own code.
    # 'context' has 'reply' method to reply to the sender in easy way.
    context.reply(message)

# Client starts connection.
client.start()

# Enable interactive command mode (optional)
client.interactive()
client.quit(u'Keyboard Interuppt')
