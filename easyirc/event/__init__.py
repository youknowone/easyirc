
import re
import traceback
from .. import util

class EventManager(object):
    def __init__(self, handlers=None):
        self.handlers = handlers if handlers is not None else []

    def putln(self, connection, message):
        # It is reversed to grant higher priority to new hook
        for handler in reversed(self.handlers):
            try:
                consumed = handler(connection, message)
            except:
                consumed = False
                traceback.print_exc()
            if consumed:
                break

    def extends(self, events):
        if isinstance(events, EventManager):
            events = events.handlers
        self.handlers += events

    # decorators
    def hook(self, handler):
        if not isinstance(handler, BaseHandler):
            handler = BaseHandler(handler)
        self.handlers.append(handler)
        return handler

    def hookglobal(self, job):
        handler = OnepassHandler(job)
        self.handlers.append(handler)
        return job

    def hookcond(self, condition): # condition is callable returns bool
        def decorator(job):
            handler = ConditionalHandler(condition, job)
            self.handlers.append(handler)
            return job
        return decorator

    def hookexc(self, exception):
        def decorator(job):
            handler = ExceptionHandler(exception, job)
            self.handlers.append(handler)
            return job
        return decorator

    def hookmsg(self, *messages):
        def decorator(job):
            handler = MessageHandler(messages, job)
            self.handlers.append(handler)
            return job
        return decorator

    def hookregex(self, regex):
        def decorator(job):
            handler = RegexHandler(regex, job)
            self.handlers.append(handler)
            return job
        return decorator


class BaseHandler(object):
    """Base handler interface.
    Process the message and return True or False.
    True to mark the message consumed. Otherwise False.
    Consumed message will not pass other handlers.
    Inherit to implement handlers.
    """
    def __call__(self, connection, message):
        raise NotImplementedError
        return False # notify handler didn't consume the message


class OnepassHandler(BaseHandler):
    """One-pass handler interface.
    Pass an function. It will acts like BaseHandler.__call__ method.
    """
    def __init__(self, action):
        self.action = action

    def __call__(self, connection, message):
        return self.action(connection, message)


class ConditionalHandler(BaseHandler):
    """Conditional handler interface.
    Pass condition callback and job callback to create a handler.
    """
    def __init__(self, condition, action):
        self.condition_func = condition
        self.job_func = action

    def condition(self, connection, message):
        """Override to ignore given condition"""
        return self.condition_func(connection, message)

    def job(self, connection, message):
        """Override to ignore given job"""
        return self.job_func(connection, message)

    def __call__(self, connection, message):
        if not self.condition(connection, message):
            return False
        return self.job(connection, message)


class ExceptionHandler(ConditionalHandler):
    """Conditional handler interface for exceptions.
    Pass exception and job callback to create a handler.
    NOTE: Ancestor exception handler may consume decestors.
    """
    def __init__(self, exception, action):
        self.exception = exception
        def condition(connection, message):
            return isinstance(message, self.exception)
        ConditionalHandler.__init__(self, condition, action)

    def __repr__(self):
        return u'<ExceptionHandler({},{})>'.format(self.exception, self.job_func)


class MessageHandler(ConditionalHandler):
    """Conditional handler interface.
    Pass command and job callback to create a handler.
    NOTE: Multiple command handler works - if message is not consumed.
    """
    def __init__(self, msgtypes, job):
        if isinstance(msgtypes, unicode):
            msgtypes = [msgtypes]
        self.types = msgtypes
        def condition(connection, message):
            if not isinstance(message, unicode):
                return False
            return util.msgsplit(message).type in self.types
        ConditionalHandler.__init__(self, condition, job)

    def job(self, connection, message):
        msgline = util.msgsplit(message)
        return self.job_func(connection, msgline.sender, *util.msgsplit(message)[2:])

    def __repr__(self):
        return u'<MessageHandler({},{})>'.format(self.types, self.job_func)


class RegexHandler(ConditionalHandler):
    """Regular Expression handler interface.
    Pass regex and job callback to create a handler.
    NOTE: Multiple command handler works - if message is not consumed.
    """
    def __init__(self, regex, job):
        self.regex = regex
        def condition(connection, message):
            if not isinstance(message, unicode):
                return False
            return re.search(self.regex, message) is not None
        ConditionalHandler.__init__(self, condition, job)

    def job(self, connection, message):
        match = re.search(self.regex, message)
        return self.job_func(connection, match.group(0), *match.groups())

    def __repr__(self):
        return u'<RegexHandler({},{})>'.format(self.regex, self.job_func)

