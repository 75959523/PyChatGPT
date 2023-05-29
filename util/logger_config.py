import logging
from logging.handlers import RotatingFileHandler

from util.time_formatter import formatter


def setup_logger(name, log_file, max_bytes=1024 * 1024, backup_count=100):
    """Set up a logger that writes to a specified file.

    Args:
    name (str): Logger name.
    log_file (str): File path to write logs to.
    level (logging.level): Minimum severity of messages to handle.
    max_bytes (int): Maximum size in bytes for a single log file. When this size is reached, the file is rotated.
    backup_count (int): Number of old log files to keep.

    Returns:
    logger (logging.Logger): Configured logger.
    """

    handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger
