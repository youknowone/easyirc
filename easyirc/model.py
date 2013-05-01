
"""Not nessessary, but good to save your time."""

from collections import OrderedDict

class DataDict(OrderedDict):
    def add(self, item):
        self[item.name] = item

class Channel(object):
    def __init__(self, name):
        self.name = name
        self.users = DataDict()


class User(object):
    def __init__(self, name):
        self.name = name

    @property
    def nick(self):
        return name.split('@', 1)[0]

