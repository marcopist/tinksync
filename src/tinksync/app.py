import os
from flask import Flask
from tinksync.tink import fetch_user_transactions
from tinksync import integrations

app = Flask(__name__)

USERNAME =  os.environ.get("TINK_USERNAME") or "myself"

CLIENTS = [
    integration(USERNAME) for integration in integrations.__all__ if integration(USERNAME).is_applicable()
]

@app.route("/reconciliate")
def reconciliate():
    transactions = fetch_user_transactions(USERNAME)
    for client in CLIENTS:
        client.
    return "OK"