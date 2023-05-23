def execute(price):
    result = "{:.10f}".format(price).rstrip('0') + "$"
    if result[-2] == '.':
        result = result[:-1]
    return result
