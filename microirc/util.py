
class Line(list):
    def __init__(self, iterable=[]):
        list.__init__(self, iterable)
        self.header = None


def split(line):
    """General IRC line decoder"""
    def decolon(item):
        """Colon has special usage in IRC protocol"""
        if item[0] == ':':
            return item[1:]
        return item

    items = Line()

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
    items.cmd = items[0].lower()
    return items
