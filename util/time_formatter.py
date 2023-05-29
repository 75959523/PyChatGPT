import logging
import pytz
from datetime import datetime


class MyFormatter(logging.Formatter):
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


handler = logging.StreamHandler()
formatter = MyFormatter(fmt="%(asctime)s %(name)-15s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
