from flask import Flask, request
from flask_cors import CORS
from openai import openai_client

app = Flask(__name__)
CORS(app)


@app.route('/api/chat', methods=['POST'])
def chat():
    param = request.get_data(as_text=True)
    result = openai_client.chat(param)

    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
