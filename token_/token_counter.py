import logging
import time
from typing import List, Dict
import json
from util import get_response_text, format_time_elapsed, format_price
from token_ import tiktokens_util

logger = logging.getLogger('token_counter')


def sum_token(request, result, time_param):
    begin = time.time()
    model = get_model(request)
    message_list = get_message_list(request)

    response_text = get_response_text.execute(result)
    logger.info(f"响应内容: {response_text}")

    prompt = tiktokens_util.num_tokens_from_messages(message_list, model)
    completion = tiktokens_util.num_tokens_from_string(response_text)
    msg = build_statistics_message(time_param, model, prompt, completion)

    logger.info(msg.replace("\n\n", ""))
    logger.info(f"费用统计耗时: {format_time_elapsed.execute(begin)}")
    return msg


def get_model(request):
    return request[request.rfind("model") + 8: request.rfind("stream") - 3]


def get_message_list(request) -> List[Dict[str, str]]:
    request_msg = request[request.find("messages") + 10: request.rfind("model") - 2]
    return string_to_list(request_msg)


def string_to_list(request_msg) -> List[Dict[str, str]]:
    json_array = json.loads(request_msg)
    message_list = []
    for map_item in json_array:
        converted_map = {}
        for key in map_item:
            converted_map[str(key)] = str(map_item[key])
        message_list.append(converted_map)
    return message_list


def build_statistics_message(time_param, model, prompt, completion):
    token = prompt + completion

    return (
        "\n\n"
        f"请求OpenAI耗时: {time_param} s"
        f", model: {model}"
        f", prompt: {prompt}"
        f", completion: {completion}"
        f", token = {token}"
        f", 请求费用: {request_price(prompt, model)}"
        f", 响应费用: {response_price(completion, model)}"
    )


def request_price(token_num, model):
    price = 0
    if model == "gpt-3.5-turbo":
        price = token_num * 0.001 * 0.002
    elif model == "gpt-4":
        price = token_num * 0.001 * 0.03
    return format_price.execute(price)


def response_price(token_num, model):
    price = 0
    if model == "gpt-3.5-turbo":
        price = token_num * 0.001 * 0.002
    elif model == "gpt-4":
        price = token_num * 0.001 * 0.06
    return format_price.execute(price)
