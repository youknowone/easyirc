
#-*- coding: utf-8 -*-

from .. import util

class BaseHook(object):
    """Base hook interface.
    Process the message and return True or False.
    True to mark the message consumed. Otherwise False.
    Consumed message will not pass other hooks.
    Inherit to implement hooks.
    """
    def run(self, client, message):
        raise NotImplementedError
        return False # notify hook didn't consume the message


class ConditionalHook(BaseHook):
    """Conditional hook interface.
    Pass condition callback and job callback to create a hook.
    """
    def __init__(self, condition, job):
        self.condition_func = condition
        self.job_func = job

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


class ExceptionHook(ConditionalHook):
    """Conditional hook interface for exceptions.
    Pass exception and job callback to create a hook.
    NOTE: Ancestor exception hook may consume decestors.
    """
    def __init__(self, exception, job):
        def condition(client, message):
            return isinstance(message, exception)
        ConditionalHook.__init__(self, condition, job)


class MessageHook(ConditionalHook):
    """Conditional hook interface.
    Pass command and job callback to create a hook.
    NOTE: Multiple command hook works - if message is not consumed.
    """
    def __init__(self, cmd, job):
        def condition(client, message):
            if not isinstance(message, unicode):
                return False
            return util.cmdsplit(message).cmd.lower() == cmd.lower()
        ConditionalHook.__init__(self, condition, job)

    def job(self, client, message):
        return self.job_func(client, util.cmdsplit(message))


