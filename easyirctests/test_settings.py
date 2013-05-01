
from easyirc.settingloader import load

import settings
settings = load(settings)

def test_settings():
    conn = settings.connections.values()[0]
    conn.name
    conn.host
    conn.port
    assert conn.addr == (conn.host, conn.port)
    assert conn.username == conn.nick
    assert conn.realname == conn.nick