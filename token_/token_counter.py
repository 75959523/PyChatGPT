import logging
from typing import List, Dict
import json
from util import get_response_method, format_cost, get_request_method
from token_ import tiktokens_util
from util.logger_config import setup_logger
from util.time_formatter import handler

logger = logging.getLogger("token_counter")
logger.handlers.clear()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger = setup_logger("token_counter", "app.log")


def sum_token(request, result, time_param):
    model = get_model(request)
    message_list = get_message_list(request)

    response_text = get_response_method.execute(result)
    logger.info(f"request content: {get_request_method.question(request)}")
    logger.info(f"response content: {response_text}")

    prompt = tiktokens_util.num_tokens_from_messages(message_list, model)
    completion = tiktokens_util.num_tokens_from_string(response_text)
    msg = build_statistics_message(time_param, model, prompt, completion)

    logger.info(msg.replace("\n\n", ""))
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
        f"Time-consuming to request OpenAI: {time_param} s"
        f", model: {model}"
        f", prompt: {prompt}"
        f", completion: {completion}"
        f", token = {token}"
        f", request cost: {request_cost(prompt, model)}"
        f", response cost: {response_cost(completion, model)}"
    )


def request_cost(token_num, model):
    cost = 0
    if model == "gpt-3.5-turbo":
        cost = token_num * 0.001 * 0.002
    elif model == "gpt-4":
        cost = token_num * 0.001 * 0.03
    return format_cost.execute(cost)


def response_cost(token_num, model):
    cost = 0
    if model == "gpt-3.5-turbo":
        cost = token_num * 0.001 * 0.002
    elif model == "gpt-4":
        cost = token_num * 0.001 * 0.06
    return format_cost.execute(cost)
