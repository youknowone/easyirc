
import traceback
from collections import OrderedDict

def load(source=None):
    if source is None:
        try:
            import easyirc_settings as source
        except ImportError as e:
            #traceback.print_exc()
            try:
                import settings as source
            except ImportError as e:
                #traceback.print_exc()
                raise e
    settings = Setting(source)
    return settings

class Setting(object):
    def __init__(self, settings):
        self.settings = settings
        self.connections = OrderedDict()
        for CONNECTION in settings.CONNECTIONS:
            connection = Connection(CONNECTION)
            self.connections[connection.name] = connection

    def __getattr__(self, key):
        try:
            return getattr(self.settings, key)
        except AttributeError:
            try:
                return self.__getattr__(key)
            except:
                return self.__getattribute__(key)

    @property
    def first_connection(self):
        return self.connections.values()[0]


class Connection(object):
    def __init__(self, optdict):
        self.opt = optdict

    @property
    def enabled(self):
        try:
            return self.opt['enabled']
        except KeyError:
            return True

    @property
    def name(self):
        try:
            return self.opt['name']
        except KeyError:
            return self.host

    @property
    def host(self):
        return self.opt['host']

    @property
    def port(self):
        return self.opt['port']

    @property
    def addr(self):
        return self.host, self.port

    @property
    def autojoins(self):
        return self.opt['autojoins']

    @property
    def nick(self):
        return self.opt['nick']

    @property
    def username(self):
        try:
            return self.opt['username']
        except KeyError:
            return self.nick

    @property
    def realname(self):
        try:
            return self.opt['realname']
        except KeyError:
            return self.username

    @property
    def admin(self):
        try:
            return self.opt['admin']
        except KeyError:
            return None

    def is_admin(self, ident):
        """Used to check mask, in future."""
        return ident == self.admin or ident == self.admin.split('!')[0]

    @property
    def invite(self):
        try:
            return self.opt['invite']
        except KeyError:
            return 'disallow'

    @property
    def autoreconnect(self):
        try:
            return self.opt['autoreconnect']
        except KeyError:
            try:
                return self.AUTO_RECONNECT
            except AttributeError:
                return True
