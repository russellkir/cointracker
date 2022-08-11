from flask import Flask, request, jsonify
import time

app = Flask(__name__)


class CTMember:
    def __init__(self, name):
        self.name = name
        self.wallet = Wallet()
        self.created_at = time.now()


class Wallet:
    def __init__(self):
        self.total_value = 0
        self.created_at = time.now()


class CoinPK:
    def __init__(self):
        self.blockchain = ""


class Transaction:
    def __init__(self, address):
        self.created_at = time.now()
        self.address = address


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/update_coin", methods=["POST", "DELETE"])
def update_coin():
    content_type = request.headers.get("Content-Type")
    if content_type != "application/json":
        return "Content-Type not supported!"

    json = request.json
    print(json)
    resp = jsonify(success=True)
    if request.method == "POST":
        # TODO: update coin address here
        pass
    if request.method == "DELETE":
        # TODO: delete coin address here
        pass
    return resp
