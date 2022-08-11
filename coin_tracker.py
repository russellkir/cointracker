from operator import truediv
from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)


class CTMember:
    def __init__(self, name):
        self.name = name
        self.wallet = Wallet(self.name)
        self.created_at = datetime.datetime.now()


class Wallet:
    def __init__(self, member):
        self.total_value = 0
        self.member = member
        self.created_at = datetime.datetime.now()
        self.coins = []  # will use a simple list for now to store coins

    def add_address(self, address):
        """
        Method to add a coin's address in a member's wallet
        """
        print("adding {}".format(address))
        self.coins.append(CoinPK(address))

    def update_address(self, old_address, new_address):
        """
        Method to update a coin's address to a member's wallet
        """
        print("updating {} to {}".format(old_address, new_address))
        found = False
        for coin in self.coins:
            if coin.address == old_address:
                coin.address = new_address
                found = True
        return found

    def delete_address(self, address):
        """
        Method to add an address to a member's wallet
        """
        print("adding {} for {}".format(address, self.member))
        print("BEFORE: ", self.coins)
        for coin in self.coins:
            if coin.address == address:
                self.coins.remove(coin)
                return True
        return False

    def get_coins(self):
        """
        Simply prints the coins in a member's wallet
        """
        wallet = []
        print("Getting wallet content")
        for coin in self.coins:
            print("Coin address: ", coin.address)
            wallet.append(coin.address)
        return wallet


class CoinPK:
    def __init__(self, address):
        self.address = address

    def update_address(self, address):
        self.address = address


class CoinAddress:
    def __init__(self, blockchain, address):
        self.blockchain = blockchain
        self.address = address
        self.transactions = []

        # def add_transaction(self, address)


class Transaction:
    def __init__(self, address):
        self.created_at = datetime.datetime.now()
        self.address = address


coin_tracker = []


@app.route("/")
def hello():
    return "Hello, World!"


def get_member(name):
    for member in coin_tracker:
        if member.name == name:
            return member


@app.route("/get_members", methods=["GET"])
def get_members():
    """
    Example: curl localhost:5000/get_members

    Get's all members of CoinTracker
    """
    if request.method == "GET":
        members = []
        for member in coin_tracker:
            members.append(member.name)
    return jsonify(members)


@app.route("/add_member", methods=["POST"])
def add_member():
    """
    Example: curl localhost:5000/add_member --header "Content-Type: application/json" --request POST --data '{"member":"Russell"}'

    Adds a member to the CoinTracker system (woot)
    """
    content_type = request.headers.get("Content-Type")
    if content_type != "application/json":
        return "Content-Type not supported!"

    json = request.json
    if request.method == "POST":
        coin_tracker.append(CTMember(json["member"]))
    return jsonify(success=True)


@app.route("/add_coin", methods=["POST"])
def add_coin():
    """
    Example: curl localhost:5000/add_coin --header "Content-Type: application/json" --request POST --data '{"member":"Russell", "coin":{"blockchain":"bitcoin","address":"3E8ociqZa9mZUSwGdSmAEMAoAxBK3FNDcd"}}'

    Adds a coin to a member's wallet
    """
    content_type = request.headers.get("Content-Type")
    if content_type != "application/json":
        return "Content-Type not supported!"

    json = request.json
    if request.method == "POST":
        get_member(json["member"]).wallet.add_address(json["coin"]["address"])
    return jsonify(success=True)


@app.route("/update_coin", methods=["POST", "DELETE"])
def update_coin():
    """
    Example update: curl localhost:5000/update_coin --header "Content-Type: application/json" --request POST --data '{"member":"Russell", "coin":{"blockchain":"bitcoin","old_address":"3E8ociqZa9mZUSwGdSmAEMAoAxBK3FNDcd","new_address":"3E8ociqZa9mZUSwGdSmAEMAoAxBK3FNDcd3"}}'

    Updates the address of a coin
    """
    content_type = request.headers.get("Content-Type")
    if content_type != "application/json":
        return "Content-Type not supported!"

    json = request.json
    if request.method == "POST":

        updated = get_member(json["member"]).wallet.update_address(
            json["coin"]["old_address"], json["coin"]["new_address"]
        )
        return jsonify(success=updated)
    if request.method == "DELETE":
        get_member(json["member"]).wallet.delete_address(json["coin"]["address"])
    return jsonify(success=True)


@app.route("/get_wallet", methods=["GET"])
def get_wallet():
    """
    Example: curl localhost:5000/get_wallet --header "Content-Type: application/json" --request GET --data '{"member":"Russell"}'

    Get's the content of a member's wallet
    """
    json = request.json
    if request.method == "GET":
        return jsonify(get_member(json["member"]).wallet.get_coins())

    return jsonify(success=True)
