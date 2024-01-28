import requests
import json

user_input = ""
while user_input != "/stop":
    user_input = input("User: ")
    data = {"message": user_input}
    # Send a POST request and get the response
    response = requests.post("http://localhost:5000/bot", json=data)
    response_json = response.json()
    print("Bot: ", response_json["message"])
