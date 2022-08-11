from flask import Flask, request, jsonify
import datetime
import requests, json

app = Flask(__name__)


class CTMember:
    def __init__(self, name):
        self.name = name
        self.wallet = Wallet(self.name)
        self.created_at = datetime.datetime.now()

    def get_name(self):
        return self.name


class Wallet:
    def __init__(self, member):
        self.total_value = 0
        self.member = member
        self.created_at = datetime.datetime.now()
        self.coins = []

    def add_address(self, blockchain, address):
        """
        Method to add a coin's address in a member's wallet
        """
        self.coins.append(CoinPK(blockchain, address))

    def update_address(self, old_address, new_address):
        """
        Method to update a coin's address to a member's wallet
        """
        found = False
        for coin in self.coins:
            if coin.get_address() == old_address:
                coin.update_address(new_address)
                found = True
        return found

    def delete_address(self, address):
        """
        Method to add an address to a member's wallet
        """
        for coin in self.coins:
            if coin.get_address() == address:
                self.coins.remove(coin)
                return True
        return False

    def get_coins(self):
        """
        Simply prints the coins in a member's wallet
        """
        wallet = []
        for coin in self.coins:
            transactions = coin.get_transactions()
            wallet.append(
                {"coin: ": coin.get_address(), "transactions: ": transactions}
            )
        return wallet

    def get_coin_transactions(self, address):
        response = requests.get("https://blockchain.info/rawaddr/{}".format(address))
        json_data = response.json()
        transactions = json_data["txs"]
        for coin in self.coins:
            if coin.get_address() == address:
                for transaction in transactions:
                    coin.add_transaction(
                        transaction["out"][0]["value"], transaction["time"]
                    )
                return coin.get_transactions()
        return []

    def get_coin_balance(self, address):
        response = requests.get("https://blockchain.info/rawaddr/{}".format(address))
        json_data = response.json()
        final_balance = json_data["final_balance"]
        for coin in self.coins:
            if coin.get_address() == address:
                coin.set_balance(final_balance)
                return coin.get_balance()
        return []


class CoinPK:
    def __init__(self, blockchain, address):
        self.ca = CoinAddress(blockchain, address)

    def get_address(self):
        return self.ca.get_address()

    def add_transaction(self, amount, creation):
        self.ca.add_transaction(amount, creation)

    def get_transactions(self):
        return self.ca.get_transactions()

    def get_balance(self):
        return self.ca.get_balance()

    def set_balance(self, balance):
        self.balance = balance

    def update_address(self, address):
        self.ca = address


class CoinAddress:
    def __init__(self, blockchain, address):
        self.blockchain = blockchain
        self.address = address
        self.balance = 0
        self.transactions = []

    def get_blockchain(self):
        return self.blockchain

    def get_address(self):
        return self.address

    def get_transactions(self):
        transactions = []
        for transaction in self.transactions:
            transactions.append(
                {
                    "amount": transaction.amount,
                    "created_at": datetime.datetime.fromtimestamp(
                        transaction.created_at
                    ),
                }
            )
        return transactions

    def get_balance(self):
        return self.balance

    def add_transaction(self, amount, creation_time):
        self.transactions.append(Transaction(amount, creation_time))


class Transaction:
    def __init__(self, amount, creation_time):
        self.created_at = creation_time
        self.amount = amount


coin_tracker = []


@app.route("/")
def hello():
    return "Hello, World!"


def get_member(name):
    for member in coin_tracker:
        if member.get_name() == name:
            return member


@app.route("/get_members", methods=["GET"])
def get_members():
    """
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
    Adds a coin to a member's wallet
    """
    content_type = request.headers.get("Content-Type")
    if content_type != "application/json":
        return "Content-Type not supported!"

    json = request.json
    if request.method == "POST":
        get_member(json["member"]).wallet.add_address(
            json["coin"]["blockchain"], json["coin"]["address"]
        )
    return jsonify(success=True)


@app.route("/update_coin", methods=["POST", "DELETE"])
def update_coin():
    """
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
    Get's the content of a member's wallet
    """
    json = request.json
    if request.method == "GET":
        return jsonify(get_member(json["member"]).wallet.get_coins())

    return jsonify(success=True)


@app.route("/get_coin_transactions", methods=["POST"])
def get_coin_transactions():
    """
    Get transactions given coin address
    """
    content_type = request.headers.get("Content-Type")
    if content_type != "application/json":
        return "Content-Type not supported!"

    json = request.json
    if request.method == "POST":
        coin = json["coin"]["address"]
        return jsonify(get_member(json["member"]).wallet.get_coin_transactions(coin))
    return jsonify(success=True)


@app.route("/get_coin_balance", methods=["POST"])
def get_coin_balance():
    """
    Get balance given coin address
    """
    content_type = request.headers.get("Content-Type")
    if content_type != "application/json":
        return "Content-Type not supported!"

    json = request.json
    if request.method == "POST":
        coin = json["coin"]["address"]
        return jsonify(
            {"BTC": get_member(json["member"]).wallet.get_coin_balance(coin)}
        )
    return jsonify(success=True)
