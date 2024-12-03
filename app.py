import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

# 載入環境變數
load_dotenv()

# 初始化 Flask 應用程式
app = Flask(__name__)

# 從環境變數中讀取金鑰
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 驗證環境變數
if not all([LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET, GEMINI_API_KEY]):
    missing = [var for var in ["LINE_CHANNEL_ACCESS_TOKEN", "LINE_CHANNEL_SECRET", "GEMINI_API_KEY"] if not os.getenv(var)]
    raise RuntimeError(f"缺少環境變數: {', '.join(missing)}")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/", methods=["GET"])
def status_check():
    return jsonify({"status": "success", "message": "一切正常！"})

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return "Invalid signature", 400
    return "OK", 200

if __name__ == "__main__":
    app.run(debug=True)
