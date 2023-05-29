import json
import uuid
import pytz
import requests
from datetime import datetime
from util import nominatim_api_client, database_service, get_request_method, get_response_method, save_image_from_url, \
    redis_service


def execute(request, param, result, url_arr, msg):
    ip_address, header = request
    db_service = database_service.DatabaseService()

    response = None
    try:
        response = requests.get("http://ip-api.com/json/" + ip_address).json()
    except Exception as e:
        print("Failed to obtain location-related information according to the requested ip", e)

    user_info = {"uuid": None}
    if response and response.get("status") == "success":
        user_uuid = uuid.uuid4()
        response["query"] = ip_address
        response["uuid"] = str(user_uuid)

        location = ""
        try:
            location = nominatim_api_client.reverse_geocode(
                float(response.get("lat")),
                float(response.get("lon")),
                18)
        except Exception as e:
            print("Failed to accurately locate according to latitude and longitude coordinates", e)

        db_service.add_ip_info(response, location)
        user_info["uuid"] = str(user_uuid)

    user_info["address"] = ip_address
    user_info["header"] = header
    user_info["create_time"] = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')

    if result:
        user_info["question"] = get_request_method.question(param)
        user_info["answer"] = get_response_method.execute(result)
        user_info["model"] = get_request_method.model(param)
        user_info["msg"] = msg.replace("\n\n", "")
        db_service.add_user_info(user_info)

    if url_arr:
        user_info["question"] = param
        user_info["answer"] = None
        user_info["model"] = "DALL·E"
        user_info["msg"] = None
        user_info_id = db_service.add_user_info(user_info)
        for index, url in enumerate(url_arr):
            try:
                save_image_from_url.execute(url, str(user_info_id) + "_" + str(index + 1))
            except Exception as e:
                print(e)

    update_user_info_cache()


def update_user_info_cache():
    db_service = database_service.DatabaseService()
    user_info = db_service.get_user_info()

    json_string = json.dumps(user_info, indent=4, ensure_ascii=False)
    r = redis_service.get_redis_connection()
    r.set("user_info_key", json_string)
