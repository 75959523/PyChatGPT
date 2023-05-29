import logging
import threading

from flask import Response, json

from util import format_time_elapsed, add_msg_to_response, get_request_method, get_response_method, get_user_info, \
    redis_service, database_service
from token_ import token_counter
from util.logger_config import setup_logger
from util.time_formatter import handler

logger = logging.getLogger("user_info_service")
logger.handlers.clear()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger = setup_logger("user_info_service", "app.log")


def handle_result(request, param, result_and_begin):
    result, begin = result_and_begin
    if result != "500":
        time_elapsed = format_time_elapsed.execute(begin)
        # token computation
        msg = token_counter.sum_token(param, result, time_elapsed)
        request = get_ip_and_header(request)
        # Collection of user information
        threading.Thread(target=get_user_info.execute, args=(request, param, result, None, msg)).start()
        result = add_msg_to_response.execute(result, msg)
        return result
    return "Server error", 500


def handle_image_result(request, result_and_substring):
    result, substring = result_and_substring
    urls = get_response_method.extract_urls_from_json(result)
    request = get_ip_and_header(request)
    # Collection of user information
    threading.Thread(target=get_user_info.execute, args=(request, substring, None, urls, None)).start()
    formatted_result = "[" + ", ".join(urls) + "]"
    return formatted_result


def get_user_info_from_db(request):
    ip_address = get_request_method.client_ip_address(request)
    logger.info("check ip: " + ip_address)
    r_service = redis_service.get_redis_connection()
    cached_data = r_service.get("user_info_key")
    if cached_data:
        return Response(cached_data, mimetype="application/json; charset=utf-8")
    db_service = database_service.DatabaseService
    user_info = db_service.get_user_info()
    user_info_json = json.dumps(user_info, indent=4, ensure_ascii=False)
    r_service.set("user_info_key", user_info_json)
    return Response(user_info_json, mimetype="application/json; charset=utf-8")


def get_ip_and_header(request):
    ip_address = get_request_method.client_ip_address(request)
    header = request.headers.get("User-Agent")
    return ip_address, header
