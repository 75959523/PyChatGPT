from util import get_response_method, format_cost, get_request_method
from token_computation import tiktokens_util
from util.logger_config import setup_logger

logger = setup_logger("token_counter", "log/app.log")


def sum_token(request, result, time_param):
    model = get_request_method.model(request)
    message_list = get_request_method.get_message_list(request)

    response_text = get_response_method.execute(result)
    logger.info(f"request content: {get_request_method.question(request)}")
    logger.info(f"response content: {response_text}")

    prompt = tiktokens_util.num_tokens_from_messages(message_list, model)
    completion = tiktokens_util.num_tokens_from_string(response_text)
    msg = build_statistics_message(time_param, model, prompt, completion)

    logger.info(msg.replace("\n\n", ""))
    return msg


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
