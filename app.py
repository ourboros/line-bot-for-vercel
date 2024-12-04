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
    app.logger.info("Callback triggered")    
    try:
    handler.handle(body, signature)
    except InvalidSignatureError as e:
    app.logger.error(f"Invalid Signature: {e}")
    abort(400)
    return "OK"  
app.logger.info("Received a request at /callback")

@app.route("/")
def home():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)
