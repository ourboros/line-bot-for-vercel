import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai

app = Flask(__name__)

# 加入 LOG：檢查環境變數是否正確讀取
print("DEBUG: Initializing environment variables")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET or not GEMINI_API_KEY:
    print(f"ERROR: Missing environment variables. LINE_CHANNEL_ACCESS_TOKEN: {LINE_CHANNEL_ACCESS_TOKEN}, LINE_CHANNEL_SECRET: {LINE_CHANNEL_SECRET}, GEMINI_API_KEY: {GEMINI_API_KEY}")
    raise ValueError("Missing one or more required environment variables.")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    print(f"DEBUG: Request body received: {body}")

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("ERROR: Invalid signature error.")
        abort(400)
    return 'OK'

# 為 Vercel 適配
def vercel_handler(event, context):
    return app(event, context)
