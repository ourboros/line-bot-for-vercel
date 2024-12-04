from flask import Flask
from flask import request
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.route("/callback", methods=["POST"])
def callback():
    return "OK", 200

@app.route("/")
def home():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)
