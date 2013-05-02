
"""Not nessessary, but good to save your time."""

from collections import OrderedDict

class DataDict(OrderedDict):
    def add(self, item):
        self[item.name] = item

class NamedObject(object):
    def __init__(self, name):
        self.name = name

class Channel(NamedObject):
    def __init__(self, name):
        self.name = name
        self.users = DataDict()

class User(NamedObject):
    @property
    def nick(self):
        return name.split('!', 1)[0]

