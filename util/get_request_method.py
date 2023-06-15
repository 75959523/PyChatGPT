import json


def model(request):
    return request[request.rfind("model") + 8:request.rfind("stream") - 3]


def flag(request):
    return request[request.rfind("flag") + 7:request.rfind("}") - 1]


def get_message_list(request):
    request_msg = request[request.find("messages") + 10: request.rfind("model") - 2]
    return string_to_list(request_msg)


def string_to_list(request_msg):
    json_array = json.loads(request_msg)
    message_list = []
    for map_item in json_array:
        converted_map = {}
        for key in map_item:
            converted_map[str(key)] = str(map_item[key])
        message_list.append(converted_map)
    return message_list


def question(request):
    return request[request.rfind("content") + 10:request.rfind("model") - 5]


def client_ip_address(request):
    ip_address = request.headers.get("X-Forwarded-For")
    if ip_address is None:
        ip_address = request.headers.get("X-Real-IP")
    if ip_address is None:
        ip_address = request.remote_addr
    return ip_address


def extract_substring(param):
    start_index = param.rfind("content") + 10
    end_index = param.rfind("}]") - 1
    return param[start_index:end_index]


def image_prepare_request_body(param):
    data = {"prompt": param, "n": 2, "size": "1024x1024", "flag": "API"}
    return json.dumps(data, ensure_ascii=False)
