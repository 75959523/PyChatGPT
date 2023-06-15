import requests
import json

from util.logger_config import setup_logger

API_KEY = ""
API_KEY_SB = ""
TARGET_URL_CHAT_OPENAI = ""
TARGET_URL_CHAT_OPENAI_SB = "https://api.openai-sb.com/v1/chat/completions"
TARGET_URL_CHAT_API = "https://api.openai.com/v1/chat/completions"
TARGET_URL_IMAGE = "https://api.openai.com/v1/images/generations"

logger = setup_logger("openai_client_base", "log/app.log")


def execute(request_param, request_type, target_url):
    logger.info("request: %s" % request_param)
    python_obj = json.loads(request_param)
    flag = python_obj["flag"]
    python_obj.pop("flag")
    if flag == "API":
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Authorization": "Bearer " + API_KEY
        }
        return do_request(python_obj, request_type, target_url, headers)

    elif flag == "OpenAI":
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
        }
        return do_request(python_obj, request_type, target_url, headers)

    elif flag == "OpenAI-SB":
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Authorization": "Bearer " + API_KEY_SB

        }
        return do_request(python_obj, request_type, target_url, headers)


def do_request(python_obj, request_type, target_url, headers):
    try:
        if request_type.upper() == "GET":
            response = requests.get(target_url, headers=headers, params=python_obj)
        else:
            response = requests.post(target_url, headers=headers, json=python_obj)

        # Add check for response status code
        response.raise_for_status()

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return str(http_err), "500"

    except Exception as e:
        logger.error("Request OpenAI Exceptions: %s" % e)
        return str(e), "500"

    return response.content.decode("utf-8"), "200"
