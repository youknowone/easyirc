
from . import MessageHook

hooks = []

def _add(handler):
    hook = MessageHook(handler)
    hooks.append(hook)
    return hook

@_add
def ping(client, message):
    
