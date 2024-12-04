from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import logging
import google.generativeai as genai
from dotenv import load_dotenv

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.route("/callback", methods=["POST"])
def callback():
    logging.info(f"Received request: {request.get_data(as_text=True)}")
    return "OK", 20

@app.route("/")
def home():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)
