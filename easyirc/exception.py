
from prettyexc import PrettyException as E

class IRCException(E):
    pass

class Disconnected(IRCException):
    pass