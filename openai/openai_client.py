from openai.openai_client_base import execute, TARGET_URL_CHAT, TARGET_URL_IMAGE


def chat(request_param):
    return execute(request_param, "POST", TARGET_URL_CHAT)


def image(request_param):
    return execute(request_param, "POST", TARGET_URL_IMAGE)
