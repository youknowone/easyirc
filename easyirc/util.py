
class MessageLine(list):
    @property
    def sender(self):
        return self[0]

    @property
    def nick(self):
        return self[0].split('!', 1)[0]

    @property
    def type(self):
        return self[1]


class CommandLine(list):
    @property
    def cmd(self):
        return self[0]


class Identity(unicode):
    @property
    def nick(self):
        return self.split('!', 1)[0]

    @property
    def username(self):
        return self.split('@', 1)[0].split('!', 1)[1]

    @property
    def host(self):
        return self.split('@', 1)[1]


def decolon(item):
    """Colon has special usage in IRC protocol"""
    if item[0] == ':':
        return item[1:]
    return item

def msgsplit(line):
    """General IRC message decoder"""
    items = MessageLine()

    #Append the sender, if not exists
    if line[0] == ':':
        item, line = line.split(' ', 1)
        items.append(decolon(item))
    else:
        items.append(None)

    items += cmdsplit(line)
    return items

def cmdsplit(line):
    items = CommandLine()

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

def parseid(identity):
    return Identity(identity)
