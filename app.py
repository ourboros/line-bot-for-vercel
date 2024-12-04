import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import google.generativeai as genai
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

app = Flask(__name__)

# Line Bot 和 OpenAI 設定
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

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

# Google Gemini 設定
genai.configure(api_key=GEMINI_API_KEY)

# 建立生成模型
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    safety_settings=safety_settings,
    generation_config=generation_config,
)


chat_session = model.start_chat(
 history=[
    {
      "role": "user",
      "parts": [
        "當user提出的問題與宜蘭運動無關時，model就回應:很高興為您服務!我是專門使用於宜蘭運動指南的chatbot，您可以根據特定運動來獲取推薦的地點喔!\n限定運動類型只有:登山健行、自行車、攀岩、游泳、籃球、羽球、桌球、健身",
      ],
    },
    {
      "role": "model",
      "parts": [
        "好的，我會按照您的指示進行。以下是一個您可以使用的回應範例：\n\n**使用者:**  請問台北101附近有什麼好吃的餐廳？\n\n**Chatbot:** 高興為您服務！我是專門使用於宜蘭運動指南的chatbot，您可以根據特定運動來獲取推薦的地點喔！例如：登山健行、自行車、攀岩、游泳、籃球、羽球、桌球、健身。 \n\n**備註:**\n\n* 您也可以在回應中加入一些宜蘭運動的相關資訊，例如：宜蘭的風景優美，非常適合運動休閒等等。\n* 您可以根據實際情況調整回應內容，例如：可以加入一些關於宜蘭運動的趣味小知識等等。\n\n希望以上資訊對您有所幫助！\n",
      ],
    },
    } 
response = chat_session.send_message("INSERT_INPUT_HERE")

def gemini_response(text):
    print(f"DEBUG: Received text for gemini_response: {text}")
    response = chat_session.send_message(text)
    print(f"DEBUG: gemini_response result: {response.text}")
    return response.text

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
    
    line_bot_api.reply_message(event.reply_token, reply)
