from flask import Flask, request, jsonify
from flask_cors import CORS

from openai_service import chat_request, image_request
from user_info_service import handle_result, handle_image_result, get_user_info_from_db
from util.logger_config import setup_logger

app = Flask(__name__)
CORS(app)

logger = setup_logger("app", "log/app.log")


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        param = request.get_data(as_text=True)
        # Request the OpenAI interface
        result = chat_request(param)
        data, time = result
        msg, code = data
        if code != "200":
            return jsonify(message=msg), 500
        else:
            return handle_result(request, param, result)
    except Exception as e:
        logger.error(f"Unexpected exception occurred: {e}")
        return "Server error", 500


@app.route("/api/image", methods=["POST"])
def image():
    try:
        param = request.get_data(as_text=True)
        # Request the OpenAI interface
        result = image_request(param)
        return handle_image_result(request, result)
    except Exception as e:
        logger.error(f"Unexpected exception occurred: {e}")
        return "Server error", 500


@app.route("/api/get", methods=["GET"])
def get_user_info():
    return get_user_info_from_db(request)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
