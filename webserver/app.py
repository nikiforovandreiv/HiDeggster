from flask import Flask, request, jsonify
from rasa.core.agent import Agent
import os

app = Flask(__name__)

path = "../models"
# we load our trained Rasa model
file_path = os.path.join(path, os.listdir(path)[0])
print(file_path)
agent = Agent.load(file_path)


async def handle_message(user_message):
    rasa_response = await agent.handle_text(user_message)
    response_text = rasa_response[0]['text'] if rasa_response else "error occured"
    return response_text


@app.route('/bot', methods=['POST'])
async def bot():
    data = request.json
    user_message = data['message'] if 'message' in data else None

    if user_message:
        response_text = await handle_message(user_message)
    else:
        response_text = "No message received."

    return jsonify({"message": response_text})

if __name__ == '__main__':
    app.run(debug=False)