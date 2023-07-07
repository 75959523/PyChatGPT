import logging
import pytz
from concurrent_log_handler import ConcurrentRotatingFileHandler
from datetime import datetime


class TimeFormatter(logging.Formatter):
    converter = pytz.timezone("Asia/Shanghai")

    def formatTime(self, record, dateformat=None):
        dt = datetime.fromtimestamp(record.created, self.converter)
        if dateformat:
            s = dt.strftime(dateformat)
        else:
            try:
                s = dt.isoformat(timespec="milliseconds")
            except TypeError:
                s = dt.isoformat()
        return s


formatter = TimeFormatter(fmt="%(asctime)s %(name)-15s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")


def setup_logger(name, log_file, max_bytes=1024 * 1024 * 0.3, backup_count=100):
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

    handler = ConcurrentRotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)

    return logger
