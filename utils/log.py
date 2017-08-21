"""Functions to manage logs."""
import logging
import os


def create_logger(name, log_level, log_path=None):
    """Create a logger.

    Args:
        name (str): name of logger
        log_level (str or NoneType, optional): level of log you want for logger
            can be any argument accepted bu logging.Loger.setLevel
        log_file_name (str or NoneType, optional): path to logs messages in
            set it to None if you want logs and stdout
    """
    log = logging.getLogger(name)

    while log.hasHandlers():
        log.removeHandler(log.handlers[0])

    if log_path:
        log_dir = os.path.dirname(log_path)
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)
        log_sh = logging.FileHandler(log_path, encoding="utf-8")
    else:
        log_sh = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s: [%(levelname)s] %(name)s - %(message)s")
    log_sh.setFormatter(formatter)
    log.setLevel(log_level)
    log.addHandler(log_sh)

    return log
