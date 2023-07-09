import os
from flask import Flask
from tinksync.main import sync

app = Flask(__name__)

@app.route("/webhooks/<username>", methods=["POST", "GET"])
def tinkrun(username):
    sync(username)
    return "OK"

if __name__ == "__main__":
    app.run(debug=True)