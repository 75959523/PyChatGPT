def execute(cost):
    result = "{:.10f}".format(cost).rstrip('0') + "$"
    if result[-2] == '.':
        result = result[:-1]
    return result
