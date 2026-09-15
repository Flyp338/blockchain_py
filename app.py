import hashlib
import json
from textwrap import dedent
from time import time
from urllib import response
from uuid import uuid4

import flask
from blockchain import BlockChain
from flask import Flask, jsonify, request

app = Flask(__name__)

# generate a globally unique address for this node
node_id = str(uuid4()).replace("-", "")

# instantiate the BlockChain
blockchain = BlockChain()


@app.route("/mine", methods=["GET"])
def mine():
    return "We'll mine a new Block"


@app.route("/transactions/new", methods=["POST"])
def new_transaction():
    values = request.get_json()
    # Check that the required fields are in the POST'ed data
    required = ["sender", "recipient", "amount"]
    if not all(k in values for k in required):
        return "Missing values", 400

    index = blockchain.new_transaction(
        values["sender"], values["recipient"], values["amount"]
    )
    response = {"message": f"Transaction will be added to Block {index}"}
    return jsonify(response), 201


@app.route("/chain", methods=["GET"])
def full_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain),
    }
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
