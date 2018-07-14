import os
import random
import time

import burin

n = 5


@burin.pipeline.step()
def inventory(run):
    run.logger.debug('doing inventory stuff...')
    time.sleep(n * random.random())


@burin.pipeline.step()
def l1_process(run):
    run.logger.debug('L1 processing stuff...')
    time.sleep(n * random.random())


@burin.pipeline.step()
def averaging(run):
    run.logger.debug('doing averaging stuff...')
    time.sleep(n * random.random())


@burin.pipeline.step()
def dynamics(run):
    run.logger.debug('doing dynamics stuff...')
    time.sleep(n * random.random())


@burin.pipeline.step()
def polarization(run):
    run.logger.debug('doing polarization stuff...')
    time.sleep(n * random.random())


@burin.pipeline.step()
def quick_invert(run):
    run.logger.debug('doing quick invert stuff...')
    time.sleep(n * random.random())


@burin.pipeline.step()
def l2_process(run):
    run.logger.debug('L2 processing stuff...')
    averaging(run)
    dynamics(run)
    polarization(run)
    quick_invert(run)


@burin.pipeline.step()
def main(run):
    inventory(run, skip=False)
    l1_process(run, skip=not run.options.get('level1', 'process'))
    l2_process(run, skip=not run.options.get('level2', 'process'))


if __name__ == '__main__':
    # initialize the run
    config = burin.config.ConfigParser('example_spec.cfg')
    if config.is_valid('example.cfg'):
        config.read('example.cfg')
    epochs = burin.config.EpochParser('epochs.cfg', 'epochs_spec.cfg')
    run = burin.pipeline.Run(config, epochs)

    log_filename = os.path.join(config.get('logging', 'basedir'),
                                'example.log')
    log_level = burin.logging.get_level(config.get('logging', 'level'))
    run.setup_logging(log_filename,
                      level=log_level,
                      rotate=config.get('logging', 'rotate'),
                      max_version=config.get('logging', 'max_version'))
    print(f'See log output in {log_filename}')

    # start the pipeline
    main(run)
