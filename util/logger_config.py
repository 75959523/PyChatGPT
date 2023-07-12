import logging
import pytz
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


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


class CustomRotatingFileHandler(RotatingFileHandler):
    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        if self.backupCount > 0:
            for i in range(self.backupCount - 1, 0, -1):
                sfn = self._name_with_number(i)
                dfn = self._name_with_number(i + 1)
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
            dfn = self._name_with_number(1)
            if os.path.exists(dfn):
                os.remove(dfn)
            self.rotate(self.baseFilename, dfn)
        if not self.delay:
            self.stream = self._open()

    def _name_with_number(self, number):
        dir_name, base_name = os.path.split(self.baseFilename)
        base_name, ext = os.path.splitext(base_name)
        return os.path.join(dir_name, f"{number}{base_name}{ext}")


def setup_logger(name, log_file, max_bytes=1024 * 1024 * 0.3, backup_count=10000):
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

    handler = CustomRotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)

    return logger
