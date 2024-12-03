import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Line Bot 和 OpenAI 設定
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

assert LINE_CHANNEL_ACCESS_TOKEN, "LINE_CHANNEL_ACCESS_TOKEN"
assert LINE_CHANNEL_SECRET, "LINE_CHANNEL_SECRET"

# Google Gemini 設定
genai.configure(api_key=GEMINI_API_KEY)

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
