import json
from entity.image_request_data import ImageRequestData


def model(request):
    return request[request.rfind("model") + 8:request.rfind("stream") - 3]


def message_list(request):
    request_msg = request[request.index("messages") + 10:request.rfind("model") - 2]
    return string_to_list(request_msg)


def string_to_list(request_msg):
    message_array = json.loads(request_msg)
    message_list_ = []
    for map_ in message_array:
        converted_map = {str(key): str(value) for key, value in map_.items()}
        message_list_.append(converted_map)
    return message_list_


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
    data = ImageRequestData(param, 2, "1024x1024")
    return json.dumps(data.__dict__, ensure_ascii=False).replace("\\", "")
