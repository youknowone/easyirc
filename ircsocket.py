
#-*- coding: utf-8 -*-

import socket


CREATED = 'CREATED'
CONNECTED = 'CONNECTED'


class IRCLine(list):
    def __init__(self, iterable=[]):
        list.__init__(self, iterable)
        self.header = None


def split_line(line):
    """General IRC line decoder"""
    def decolon(item):
        """Colon has special usage in IRC protocol"""
        if item[0] == ':':
            return item[1:]
        return item

    items = IRCLine()

    #Remove the line header, if exists
    if line[0] == ':':
        item, line = line.split(' ', 1)
        items.header = decolon(item)

    while ' ' in line:
        # Colon-headed item means it is long argument
        if line[0] == ':':
            break
        item, line = line.split(' ', 1)
        # Skip zero-lengthed item - split is not good enough for this case
        if len(item) == 0:
            continue
        items.append(decolon(item))
    # Attach the last item
    items.append(decolon(line))
    return items


class IRCSocket(object):
    def __init__(self, addr, charset='utf-8'):
        """addr is a tuple represents (host, port)"""
        self.addr = addr
        self.charset = charset
        self.create_socket()

    def create_socket(self):
        self.socket = socket.socket()
        self.queue = [CREATED] # EVERYTHING-IS-RESPONSE!
        self.recvbuffer = ''

    def send(self, line):
        self.socket.send(line.encode(self.charset))

    def sendln(self, line, *arg, **kwargs):
        if len(arg) or len(kwargs):
            line = line.format(*arg, **kwargs)
        #print '--> SEND', line
        self.send(line + '\r\n')

    def connect(self):
        self.socket.connect(self.addr)
        self.queue.append(CONNECTED) # EVERYTHING-IS-RESPONSE!

    def cmd(self, cmd, *args):
        self.sendln(u' '.join(map(unicode, [cmd] + list(args))))

    def cmdl(self, cmd, *args): # destructive!
        nargs = list(args[:-1]) + [':' + args[-1]]
        self.cmd(cmd, *nargs)

    def cmda(self, cmd, *args):
        if ' ' in args[-1]:
            self.cmdl(cmd, *args)
        else:
            self.cmd(cmd, *args)

    def dispatch(self):
        """Dispatch an item from queue."""
        if len(self.queue) == 0:
           return None
        msg = self.queue[0]
        del(self.queue[0])
        return msg

    def dispatch_all(self):
        msg = True
        while msg:
            msg = self.dispatch()
            if msg:
                yield msg
        raise StopIteration

    def _recv(self):
        """NOTE: blocking"""
        received = self.socket.recv(1024) # 1kb is enough for irc
        #print '<-- RECV:', received
        self.recvbuffer += received

    def _debuffer(self):
        """Catch 'ValueError' to check unsplitable"""
        newline, self.recvbuffer = self.recvbuffer.split('\r\n', 1)
        try:
            return newline.decode(self.charset)
        except:
            print 'Supposed charset is', self.charset, ', but undecodable string found:', newline
            return newline

    def _enqueue(self, line):
        self.queue.append(line)

    def _enqueue_buffer(self):
        newline = self._debuffer()
        self._enqueue(newline)

    def _enqueue_buffer_all(self):
        try:
            while True:
                self._enqueue_buffer()
        except ValueError:
            pass

    def recv_enqueue(self, force_queue=False):
        """NOTE: blocking"""
        while True:
            try:
                self._recv()
                self._enqueue_buffer_all()
            except Exception as e:
                self._enqueue(e)
            if not force_queue or len(self.queue) > 0:
                break

    def dispatch_cmd(self):
        """Actually, not a socket-level but for easy-debug."""
        msg = self.dispatch()
        if msg is None:
            return None
        return split_line(msg)

    def dispatch_all_cmd(self):
        """Actually, not a socket-level but for easy-debug."""
        for msg in self.dispatch_all():
            yield split_line(msg)

