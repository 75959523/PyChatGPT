import time


def execute(begin):
    elapsed_seconds = time.time() - begin
    return "{:.3f}".format(elapsed_seconds)

