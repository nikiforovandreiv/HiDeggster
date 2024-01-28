from flask import Flask, request, jsonify
from rasa.core.agent import Agent
from rasa.utils.endpoints import EndpointConfig
import os

app = Flask(__name__)

path = "..\models"
# Load the trained Rasa model
file_path = os.path.join(path, os.listdir(path)[-1])
print(file_path)
action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
agent = Agent.load(file_path, action_endpoint=action_endpoint)

async def handle_message(user_message):
    rasa_responses = await agent.handle_text(user_message)
    response_texts = [response['text'] for response in rasa_responses if 'text' in response]
    # Concatenate responses with newline
    return '\n'.join(response_texts)

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
