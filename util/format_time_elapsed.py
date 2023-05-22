import time


def format_time_elapsed(begin):
    elapsed_seconds = time.time() - begin
    return "{:.3f}".format(elapsed_seconds)
