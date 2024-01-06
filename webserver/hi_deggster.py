import requests
import json
user_input = ""
while user_input != "/stop":
    user_input = input("User: ")
    data = {"message": user_input}
    response = json.loads(requests.post("http://localhost:5000/bot", json=data))
    print("Bot: ", response["message"])