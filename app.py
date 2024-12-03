import os
from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import google.generativeai as genai
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 創建 Flask 應用程式
app = Flask(__name__)

# 確認環境變數
REQUIRED_ENV_VARS = ["LINE_CHANNEL_SECRET", "LINE_CHANNEL_ACCESS_TOKEN", "GEMINI_API_KEY"]

@app.route("/", methods=["GET"])
def check_status():
    missing_vars = [var for var in REQUIRED_ENV_VARS if var not in os.environ]
    if missing_vars:
        return jsonify({
            "status": "error",
            "message": f"Missing environment variables: {', '.join(missing_vars)}"
        }), 500
    
    return jsonify({
        "status": "success",
        "message": "一切正常！"
    })

# 處理 LINE 的 Webhook 路徑
@app.route("/callback", methods=["POST"])
def callback():
    try:
        body = request.get_json()
        print("Received Webhook:", body)
        return "Callback received", 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
