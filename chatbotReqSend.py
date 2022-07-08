import requests

BASE = "http://127.0.0.1:5000/"
currentdir = "responses.json"
while True :
    inp = input("You:")
    response = requests.get(BASE+"predict/"+inp)
    print("Bot:"+ response.json())