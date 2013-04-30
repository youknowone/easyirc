
from .. import util

class EventManager(object):
    def __init__(self, handlers=None):
        self.handlers = handlers if handlers is not None else []

    def putln(self, client, message):
        # It is reversed to grant higher priority to new hook
        for handler in reversed(self.handlers):
            consumed = handler.run(client, message)
            if consumed:
                break

    # decorators
    def hook(self, handler):
        if not isinstance(handler, BaseHandler):
            handler = BaseHandler(handler)
        self.handlers.append(handler)
        return handler

    def hookglobal(self, job):
        handler = OnepassHandler(job)
        self.handlers.append(handler)
        return handler

    def hookcond(self, condition): # condition is callable returns bool
        def decorator(job):
            handler = ConditionalHandler(condition, job)
            self.handlers.append(handler)
            return handler
        return decorator

    def hookexc(self, exception):
        def decorator(job):
            handler = ExceptionHandler(exception, job)
            self.handlers.append(handler)
            return handler
        return decorator

    def hookmsg(self, message):
        def decorator(job):
            handler = MessageHandler(message, job)
            self.handlers.append(handler)
            return handler
        return decorator


class BaseHandler(object):
    """Base handler interface.
    Process the message and return True or False.
    True to mark the message consumed. Otherwise False.
    Consumed message will not pass other handlers.
    Inherit to implement handlers.
    """
    def run(self, client, message):
        raise NotImplementedError
        return False # notify handler didn't consume the message


class OnepassHandler(BaseHandler):
    """One-pass handler interface.
    Pass an function. It will acts like BaseHandler.run method.
    """
    def __init__(self, action):
        self.action = action

    def run(self, client, message):
        return self.action(client, message)


class ConditionalHandler(BaseHandler):
    """Conditional handler interface.
    Pass condition callback and job callback to create a handler.
    """
    def __init__(self, condition, action):
        self.condition_func = condition
        self.job_func = action

    def condition(self, client, message):
        """Override to ignore given condition"""
        return self.condition_func(client, message)

    def job(self, client, message):
        """Override to ignore given job"""
        return self.job_func(client, message)

    def run(self, client, message):
        if not self.condition(client, message):
            return False
        return self.job(client, message)


class ExceptionHandler(ConditionalHandler):
    """Conditional handler interface for exceptions.
    Pass exception and job callback to create a handler.
    NOTE: Ancestor exception handler may consume decestors.
    """
    def __init__(self, exception, action):
        self.exception = exception
        def condition(client, message):
            return isinstance(message, self.exception)
        ConditionalHandler.__init__(self, condition, action)

    def __repr__(self):
        return u'<ExceptionHandler({},{})>'.format(self.exception, self.job_func)


class MessageHandler(ConditionalHandler):
    """Conditional handler interface.
    Pass command and job callback to create a handler.
    NOTE: Multiple command handler works - if message is not consumed.
    """
    def __init__(self, msgtype, job):
        self.messagetype = msgtype
        def condition(client, message):
            if not isinstance(message, unicode):
                return False
            return util.msgsplit(message).type == self.messagetype
        ConditionalHandler.__init__(self, condition, job)

    def job(self, client, message):
        msgline = util.msgsplit(message)
        return self.job_func(client, msgline.sender, *util.msgsplit(message)[2:])

    def __repr__(self):
        return u'<MessageHandler({},{})>'.format(self.messagetype, self.job_func)

