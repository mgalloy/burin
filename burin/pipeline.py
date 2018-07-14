import datetime
import functools
import logging
import math

logger = logging.getLogger()


class WrappedFormatter(logging.Formatter):
    """Custom formatter, overrides funcName with value of funcName_override if
       it exists."""
    def format(self, record):
        if hasattr(record, 'func'):
            record.funcName = record.func.__name__
        return super(WrappedFormatter, self).format(record)


def human_timedelta(timedelta):
    secs = timedelta.total_seconds()

    units = [('day', 60 * 60 * 24),
             ('hr', 60 * 60),
             ('min', 60),
             ('sec', 1)]
    parts = []
    for unit, mul in units:
        if secs / mul >= 1 or mul == 1:
            if mul > 1:
                n = int(math.floor(secs / mul))
                secs -= n * mul
            else:
                n = '%d' % secs
            parts.append("%s %s%s" % (n, unit, '' if n == 1 else "s"))
    return ' '.join(parts)


def step():
    def actual_decorator(func):
        @functools.wraps(func)
        def func_wrapper(*args, skip=False, **kwargs):
            e = {'func': func}

            if skip:
                if logger:
                    logger.info(f'skipping {func.__name__}', extra=e)
            else:
                if logger:
                    logger.info(f'starting {func.__name__}', extra=e)
                    start_dt = datetime.datetime.now()
                func(*args, **kwargs)
                if logger:
                    end_dt = datetime.datetime.now()
                    time_interval = end_dt - start_dt
                    human_time = human_timedelta(time_interval)
                    logger.info(f'done with {func.__name__}: {human_time}',
                                extra=e)

        return func_wrapper
    return actual_decorator



class Run:

    def __init__(self, options, epochs):
        self.options = options
        self.epochs = epochs

        self.logger = self.setup_logging()

    def setup_logging(self):
        # TODO: use options to configure logger
        handler = logging.StreamHandler()
        formatter = WrappedFormatter('%(asctime)s %(funcName)s: %(levelname)s: %(message)s',
                                     datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger
