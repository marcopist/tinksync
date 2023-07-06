import os
from flask import Flask
from tinksync.tink import fetch_user_transactions
from tinksync import integrations

app = Flask(__name__)


@app.route("/reconciliate")
def reconciliate():
    return "OK"
