import json


def execute(result):
    response_text = ""
    for data in data_splitter(result):
        if data != " [DONE]\n\n":
            response_text += extract_response_text(data)
    return response_text


def data_splitter(input_str):
    data_array = input_str.split("data:")
    if data_array and data_array[0] == "":
        data_array = data_array[1:]
    return data_array


def extract_response_text(data):
    json_data = json.loads(data)
    choices = json_data.get('choices', [])
    response_text = ""
    for choice in choices:
        delta = choice.get("delta", {})
        if "content" in delta:
            response_text += delta.get("content", "")
    return response_text


def extract_urls_from_json(image_string):
    json_obj = json.loads(image_string)
    data_list = json_obj.get("data", [])
    return [data.get("url") for data in data_list]
