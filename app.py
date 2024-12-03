import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import google.generativeai as genai
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 初始化 Flask 應用程式
app = Flask(__name__)

# 從環境變數中讀取 LINE Bot 所需的金鑰
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 驗證環境變數是否正確
if not all([LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET, GEMINI_API_KEY]):
    missing_vars = [
        var
        for var in ["LINE_CHANNEL_ACCESS_TOKEN", "LINE_CHANNEL_SECRET", "GEMINI_API_KEY"]
        if not os.getenv(var)
    ]
    raise EnvironmentError(f"缺少必要的環境變數: {', '.join(missing_vars)}")

# 初始化 LINE Bot API 和 WebhookHandler
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/", methods=["GET"])
def check_status():
    return jsonify({
        "status": "success",
        "message": "一切正常！環境變數已成功讀取。",
        "env_vars": {
            "LINE_CHANNEL_ACCESS_TOKEN": bool(LINE_CHANNEL_ACCESS_TOKEN),
            "LINE_CHANNEL_SECRET": bool(LINE_CHANNEL_SECRET),
            "GEMINI_API_KEY": bool(GEMINI_API_KEY)
        }
    })

@app.route("/callback", methods=["POST"])
def callback():
    # 獲取 X-Line-Signature 標頭
    signature = request.headers.get("X-Line-Signature")

    # 獲取請求正文
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # 驗證請求
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return "Invalid signature. Please check your LINE Channel Secret.", 400

    return "Callback received", 200

if __name__ == "__main__":
    app.run(debug=True)
