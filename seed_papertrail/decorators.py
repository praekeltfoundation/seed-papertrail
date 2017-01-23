from functools import wraps
import logging
import time


# NOTE: got this from http://stackoverflow.com/a/14412901
def doublewrap(f):
    '''
    a decorator decorator, allowing the decorator to be used as:
    @decorator(with, arguments, and=kwargs)
    or
    @decorator
    '''
    @wraps(f)
    def new_dec(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            # actual decorated function
            return f(args[0])
        else:
            # decorator arguments
            return lambda realf: f(realf, *args, **kwargs)

    return new_dec


class PapertrailHelper(object):

    def __init__(self):
        self.debug = self.make_decorator('DEBUG', logger='papertrail')
        self.info = self.make_decorator('INFO', logger='papertrail')
        self.error = self.make_decorator('ERROR', logger='papertrail')
        self.warn = self.make_decorator('WARNING', logger='papertrail')

    def __call__(self, message, level='DEBUG', logger='papertrail'):
        return self.make_decorator(level, logger)(message)

    def make_decorator(self, level, logger):
        logger = logging.getLogger(logger)

        @doublewrap
        def decorator(f, message=''):
            @wraps(f)
            def wrap(*args, **kwargs):
                start = time.clock()
                resp = f(*args, **kwargs)
                duration = time.clock() - start
                logger.log(
                    getattr(logging, level),
                    '%s.%s %f: %s' % (
                        f.__module__,
                        f.__name__,
                        duration, message))
                return resp
            return wrap
        return decorator

papertrail = PapertrailHelper()