"""
Functions to set up the program logger.

from https://github.com/stevekm/logging-demo
"""
import yaml
import logging
import logging.config
import datetime


def timestamp():
    """Return a timestamp string."""
    return '{:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now)


def logpath(logfile='log.txt'):
    """Return the path to the main log file; needed by the logging.yml

    Use this for the dynamic output log file paths and names.
    """
    return logging.FileHandler(logfile)


def log_setup(config_yaml, logger_name):
    """Set up the logger for the script."""
    with open(config_yaml, 'r') as f:
        logging.config.dictConfig(yaml.safe_load(f.read()))
    return logging.getLogger(logger_name)


def logger_filepath(logger, handler_name):
    """Get the path to the filehandler log file."""
    log_file = None
    for h in logger.__dict__['handlers']:
        if h.__class__.__name__ == 'FileHandler':
            logname = h.get_name()
            if handler_name == logname:
                log_file = h.baseFilename
    return log_file