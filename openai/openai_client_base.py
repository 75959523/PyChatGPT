import requests
import logging
import json

from util.logger_config import setup_logger
from util.time_formatter import handler

API_KEY = ""
TARGET_URL_CHAT = "https://api.openai.com/v1/chat/completions"
TARGET_URL_IMAGE = "https://api.openai.com/v1/images/generations"

logger = logging.getLogger("openai_client_base")
logger.handlers.clear()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger = setup_logger("openai_client_base", "app.log")



def execute(request_param, request_type, target_url):
    logger.info("request: %s" % request_param)
    python_obj = json.loads(request_param)

    try:
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Authorization": "Bearer " + API_KEY
        }

        if request_type.upper() == "GET":
            response = requests.get(target_url, headers=headers, params=python_obj)
        else:
            response = requests.post(target_url, headers=headers, json=python_obj)

        # Add check for response status code
        response.raise_for_status()

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return "500"

    except Exception as e:
        logger.error("Request OpenAI Exceptions: %s" % e)
        return "500"

    return response.content.decode("utf-8")
