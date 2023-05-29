import time
import concurrent.futures

from openai import openai_client
from util import get_request_method


def chat_request(param):
    begin = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(openai_client.chat, param)
        result = future.result()
    return result, begin


def image_request(param):
    substring = get_request_method.extract_substring(param)
    request_body = get_request_method.image_prepare_request_body(substring)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(openai_client.image, request_body)
        result = future.result()
    return result, substring
