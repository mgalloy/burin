import functools
import logging
import random
import time


logger = logging.getLogger()


class WrappedFormatter(logging.Formatter):
    """Custom formatter, overrides funcName with value of funcName_override if
       it exists."""
    def format(self, record):
        if hasattr(record, 'func'):
            record.funcName = record.func.__name__
        return super(WrappedFormatter, self).format(record)


def step(logger=logger):
    def actual_decorator(func):
        @functools.wraps(func)
        def func_wrapper(*args, skip=False, **kwargs):
            #log_options = {'funcName_override': func.__name__}
            log_options = {'func': func}
            if skip:
                if logger:
                    logger.info(f'skipping {func.__name__}', extra=log_options)
            else:
                if logger:
                    logger.info(f'starting {func.__name__}', extra=log_options)
                start_time = time.time()
                func(*args, **kwargs)
                end_time = time.time()
                if logger:
                    logger.info(f'done with {func.__name__}: {end_time - start_time:0.1f} sec',
                                extra=log_options)

        return func_wrapper
    return actual_decorator


@step(logger=logger)
def inventory():
    logger.debug('doing inventory stuff...')
    time.sleep(3.0 * random.random())


@step(logger=logger)
def l1_process():
    logger.debug('L1 processing stuff...')
    time.sleep(3.0 * random.random())


@step(logger=logger)
def averaging():
    logger.debug('doing averaging stuff...')
    time.sleep(3.0 * random.random())


@step(logger=logger)
def dynamics():
    logger.debug('doing dynamics stuff...')
    time.sleep(3.0 * random.random())


@step(logger=logger)
def polarization():
    logger.debug('doing polarization stuff...')
    time.sleep(3.0 * random.random())


@step(logger=logger)
def quick_invert():
    logger.debug('doing quick invert stuff...')
    time.sleep(3.0 * random.random())


@step(logger=logger)
def l2_process():
    logger.debug('L2 processing stuff...')
    averaging()
    dynamics()
    polarization()
    quick_invert()


@step(logger=logger)
def main():
    inventory(skip=False)
    l1_process(skip=False)
    l2_process()


def setup():
    handler = logging.StreamHandler()
    formatter = WrappedFormatter('%(asctime)s %(funcName)s: %(levelname)s: %(message)s',
                                 datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    setup()
    main()
