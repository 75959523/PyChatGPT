import requests
import logging
import json

API_KEY = "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"
TARGET_URL_CHAT = "https://api.openai.com/v1/chat/completions"
TARGET_URL_MODEL = "https://api.openai.com/v1/models"
TARGET_URL_IMAGE = "https://api.openai.com/v1/images/generations"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def execute(request_param, request_type, target_url):
    logger.info("请求参数: %s" % request_param)
    python_obj = json.loads(request_param)

    try:
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Authorization": "Bearer " + API_KEY
        }

        if request_type.upper() == 'GET':
            response = requests.get(target_url, headers=headers, params=python_obj)
        else:
            response = requests.post(target_url, headers=headers, json=python_obj)

    except Exception as e:
        logger.error("请求OpenAI异常: %s" % e)
        return "500"

    return response.content.decode('utf-8')
