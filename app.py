import os
from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 創建 Flask 應用程式
app = Flask(__name__)

# 讀取環境變數
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

# 初始化 LineBotApi 和 WebhookHandler
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 確認環境變數是否正確設定
REQUIRED_ENV_VARS = ["LINE_CHANNEL_SECRET", "LINE_CHANNEL_ACCESS_TOKEN"]

@app.route("/", methods=["GET"])
def check_status():
    """
    測試根路徑:
    - 確認環境變數是否正確設定
    - 如果設定正確，返回 "一切正常！"
    """
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

@app.route("/callback", methods=["POST"])
def callback():
    """
    處理來自 LINE 平台的 Webhook 請求:
    - 驗證請求的簽名
    - 將事件交給 WebhookHandler 處理
    """
    signature = request.headers.get("X-Line-Signature")  # 從標頭中獲取簽名
    body = request.get_data(as_text=True)  # 獲取請求的主體

    try:
        handler.handle(body, signature)  # 驗證並處理事件
    except InvalidSignatureError:
        return jsonify({
            "status": "error",
            "message": "Invalid signature"
        }), 400

    return "OK", 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """
    處理來自用戶的訊息事件:
    - 回應用戶傳送的文字訊息
    """
    user_message = event.message.text  # 獲取用戶的文字訊息
    reply_message = f"你剛剛說了: {user_message}"  # 構造回應訊息

    # 回應訊息給用戶
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

if __name__ == "__main__":
    """
    本地執行應用程式（開發階段）
    """
    app.run(debug=True)
