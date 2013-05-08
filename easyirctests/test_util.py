
# -*- coding: utf-8 -*-
import pytest

from easyirc import util

@pytest.mark.parametrize(['line', 'items'], [
    [':localhost PING :thepingstring', ['localhost', 'PING', 'thepingstring']],
    ['PRIVMSG #chan nick :this is the msg', [None, 'PRIVMSG', '#chan', 'nick', 'this is the msg']],
])
def test_msgsplit(line, items):
    splited = util.msgsplit(line)
    assert splited == items

@pytest.mark.parametrize(['sender', 'nick', 'username', 'host'], [
    ['easybot!~easyirc@127.0.0.1', 'easybot', '~easyirc', '127.0.0.1'],
])
def test_identify(sender, nick, username, host):
    identity = util.parseid(sender)
    assert identity.nick == nick
    assert identity.username == username
    assert identity.host == host

