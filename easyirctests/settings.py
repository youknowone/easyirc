
# NOTE: To set up, edit local_settings.py
CONNECTIONS = [
    {
        'name': 'localbot',
        'host': 'localhost',
        'port': 6667,
        'nick': 'easyirc',
        'autojoins': ['#easyirc'],
        'enabled': True,
    }
]

TEST_REALSERVER = False

try:
    from local_settings import *
except ImportError:
    print '*** NO local_settings.py file set up. read README! ***'
    pass

TEST_CONNECTION = CONNECTIONS[0]
