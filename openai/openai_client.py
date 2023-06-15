import json

from openai.openai_client_base import execute, TARGET_URL_IMAGE, TARGET_URL_CHAT_API, TARGET_URL_CHAT_OPENAI, \
    TARGET_URL_CHAT_OPENAI_SB


def chat(request_param):
    flag = json.loads(request_param)["flag"]
    if flag == "API":
        return execute(request_param, "POST", TARGET_URL_CHAT_API)
    elif flag == "OpenAI":
        return execute(request_param, "POST", TARGET_URL_CHAT_OPENAI)
    elif flag == "OpenAI-SB":
        return execute(request_param, "POST", TARGET_URL_CHAT_OPENAI_SB)


def image(request_param):
    return execute(request_param, "POST", TARGET_URL_IMAGE)
