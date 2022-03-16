# pylint: disable=missing-function-docstring
import json
from flask import Flask, request

app = Flask(__name__)

users = {}
options = []


@app.route("/user/")
def list_users():
    return json.dumps(users)


@app.route("/user/<username>", methods=['POST'])
def add_user(username):
    users[username] = []
    return {"message": f"User {username} added"}


@app.route("/user/<username>/option/", methods=['POST'])
def change_user_order(username):
    body = request.get_json()
    users[username] = body["order"]
    return {"message": f"User {username} order changed"}


@app.route("/option")
def list_options():
    return json.dumps({"options": options})


@app.route("/option/<option>", methods=['POST'])
def add_option(option):
    options.append(option)
    return json.dumps({"message": f"Option {option} added"})

def calculate_result():
    option_map = {}
    for usr_opt in users.values():
        for option in range(len(usr_opt)):
            name = usr_opt[option]
            if name not in option_map:
                option_map[name] = 0
            option_map[name] += 1/(option + 1)
    sorted_keys = sorted(option_map, key=option_map.get)
    return [{key: option_map[key]} for key in sorted_keys][::-1]


@app.route("/result")
def get_result():
    return json.dumps({"result": calculate_result()})

def test_calculate_result():
    users["bob"] = ["lol", "tdd", "sus"]
    users["caio"] = ["tdd", "cafe", "vue"]
    users["mike"] = ["vue", "lol", "cafe"]
    print(calculate_result())

test_calculate_result()
