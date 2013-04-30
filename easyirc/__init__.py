
from __future__ import absolute_import
#from .core import *
from .settingloader import load as load_settings

try:
    settings = load_settings()
except ImportError:
    print 'Warning: No settings.py or easyirc_settings.py file found.'
    settings = None