
# NOTE: To set up, edit local_settings.py
CONNECTIONS = [
    {
        'name': 'localbot',
        'host': 'localhost',
        'port': 6667,
        'nick': 'easyirc',
        'autojoins': ['#easyirc'],
        'enabled': True,
        'admin': None,
        'invite': 'allow',
    }
]

RAW_LOG = True
AUTO_RECONNECT = True

try:
    from local_settings import *
except ImportError:
    print '*** NO local_settings.py file set up. read README! ***'
    pass

