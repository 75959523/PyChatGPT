import json


def execute(lst, msg):
    lst = lst.split("\n\n")
    lst.pop()
    done_before = json.loads(lst[-2][6:])  # skip 'data: '
    done_before_bak = json.loads(lst[-2][6:])
    done = lst[-1]

    re = add_msg_to_json_object(done_before, msg)
    re = "data: " + json.dumps(re)

    lst[-2] = re
    lst[-1] = "data: " + json.dumps(done_before_bak)
    lst.append(done)

    return '\n\n'.join(lst)


def add_msg_to_json_object(add, msg):
    add['choices'][0]['delta']['content'] = msg
    add['choices'][0]['finish_reason'] = None
    return add
