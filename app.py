from linebot import LineBotApi, WebhookHandler
import os

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'default_token')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', 'default_secret')

if LINE_CHANNEL_ACCESS_TOKEN == 'default_token' or LINE_CHANNEL_SECRET == 'default_secret':
    raise ValueError("Environment variables not set correctly. Check your .env file or platform settings.")

try:
    line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
    handler = WebhookHandler(LINE_CHANNEL_SECRET)
    print("Initialization successful!")
except Exception as e:
    print("Initialization failed:", str(e))

