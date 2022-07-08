import imp
import json
import re
import random_responses
from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS


def load_json(file):
    with open(file) as bot_responses:
        return json.load(bot_responses)

currentdir = "responses.json"
response_data = load_json(currentdir)

def get_response(input_string):
    global currentdir, response_data
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    score_list = []
    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response['required_words']

        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1
        if required_score == len(required_words):
            for word in split_message:
                if word in response['user_input']:
                    response_score += 1
        score_list.append(response_score)

    best_response = max(score_list)
    response_index = score_list.index(best_response)
    
    if input_string == "":
        return "Please Type Something"
    if best_response != 0:
        print(currentdir)
        out = response_data[response_index]['bot_response']
        if response_index <= 3 and currentdir == 'responses.json':
            currentdir = 'savings.json'
            response_data = load_json(currentdir)
        elif response_index >= 4 and response_index <= 7 and currentdir == 'responses.json':
            currentdir = 'current.json'
            response_data = load_json(currentdir)    
        elif response_index <= 1 and currentdir == 'savings.json':
            currentdir = 'responses.json'
            response_data = load_json(currentdir)
            return get_response(input_string)
        elif response_index <= 1 and currentdir == 'current.json':
            currentdir = 'responses.json'
            response_data = load_json(currentdir)
            return get_response(input_string)
        return out
    return random_responses.random_string()


app = Flask(__name__)
api = Api(app)
CORS(app)

class chatBot(Resource):
    def get(self, inputString):
        resp = get_response(inputString)
        return resp

api.add_resource(chatBot, "/predict/<string:inputString>")

if __name__ == "__main__":
    app.run(debug=True)

