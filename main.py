from flask import Flask, request
from flask_cors import CORS
from openai import openai_client
from token_ import token_counter
import time
from util import format_time_elapsed, add_msg_to_response

app = Flask(__name__)
CORS(app)


@app.route('/api/chat', methods=['POST'])
def chat():
    begin = time.time()
    param = request.get_data(as_text=True)
    result = openai_client.chat(param)
    if result != "500":
        time_elapsed = format_time_elapsed.execute(begin)
        msg = token_counter.sum_token(param, result, time_elapsed)
        result = add_msg_to_response.execute(result, msg)
        return result
    return "Server error", 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
