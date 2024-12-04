from linebot import LineBotApi, WebhookHandler
import os
from http.server import BaseHTTPRequestHandler

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'default_token')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', 'default_secret')

if LINE_CHANNEL_ACCESS_TOKEN == 'default_token' or LINE_CHANNEL_SECRET == 'default_secret':
    raise ValueError("Environment variables not set correctly. Check your .env file or platform settings.")

try:
    # 初始化 LineBot API 和 WebhookHandler
    line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
    handler = WebhookHandler(LINE_CHANNEL_SECRET)
    print("Initialization successful!")

    # 測試 BaseHTTPRequestHandler 是否正確設置
    base = BaseHTTPRequestHandler
    print(f"Base class type: {type(base)}")

    # 檢查 base 是否是 BaseHTTPRequestHandler 的子類
    if isinstance(base, type) and issubclass(base, BaseHTTPRequestHandler):
        print("base is a subclass of BaseHTTPRequestHandler")
    else:
        print("base is NOT a subclass of BaseHTTPRequestHandler")

except Exception as e:
    print("Initialization failed:", str(e))
