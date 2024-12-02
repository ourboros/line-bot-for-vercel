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
                "請推薦我一個宜蘭運動的地點",
            ],
        },
        {
            "role": "model",
            "parts": [
                "請告訴我你喜歡什麼樣的運動，以及你希望運動地點有什麼特點，例如：\n\n* **運動種類：** 跑步、騎自行車、游泳、攀岩、登山、戶外運動等等\n* **地點偏好：** 海邊、山區、公園、室內場館等等\n* **難度：** 輕鬆、中等、挑戰\n* **環境要求：** 風景優美、交通方便、設備齊全等等\n\n這樣我可以更精准地推薦適合你的宜蘭運動地點。 \n\n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "當user提問請推薦我一個宜蘭運動的地點，請都以上述model的模板做出回應",
            ],
        },
        {
            "role": "model",
            "parts": [
                "請告訴我你喜歡什麼樣的運動，以及你希望運動地點有什麼特點，例如：\n\n* **運動種類：** 跑步、騎自行車、游泳、攀岩、登山、戶外運動等等\n* **地點偏好：** 海邊、山區、公園、室內場館等等\n* **難度：** 輕鬆、中等、挑戰\n* **環境要求：** 風景優美、交通方便、設備齊全等等\n\n這樣我可以更精准地推薦適合你的宜蘭運動地點。 \n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "當user的提問有關於宜蘭，就以上述model的模板做出回應",
            ],
        },
        {
            "role": "model",
            "parts": [
                "好的，請告訴我你想要在宜蘭做什麼運動，以及你希望運動地點有什麼特點，例如：\n\n* **運動種類：** 跑步、騎自行車、游泳、攀岩、登山、戶外運動等等\n* **地點偏好：** 海邊、山區、公園、室內場館等等\n* **難度：** 輕鬆、中等、挑戰\n* **環境要求：** 風景優美、交通方便、設備齊全等等\n\n這樣我可以更精准地推薦適合你的宜蘭運動地點。 \n",
            ],
        },
    ]
)

def gemini_response(text):
    response = chat_session.send_message(text)
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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    print(f"Received message: {msg}")
    try:
        response = gemini_response(msg)
        print(f"Gemini response: {response}")
        reply = TextSendMessage(text=response)
    except Exception as e:
        print(f"Error: {str(e)}")
        reply = TextSendMessage(text="請問有關宜蘭的哪方面活動資訊？")
    
    line_bot_api.reply_message(event.reply_token, reply)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
