import json
import re


def execute(result):
    response_text = ""
    for data in data_splitter(result):
        if data != " [DONE]":
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


def extract_content(input_str):
    contents = re.findall(r'"content":"([^"]*)"', input_str)
    return "".join(contents)
