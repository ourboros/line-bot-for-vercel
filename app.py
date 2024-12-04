import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import google.generativeai as genai
from dotenv import load_dotenv
from server import app

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

if LINE_CHANNEL_ACCESS_TOKEN == 'default_token' or LINE_CHANNEL_SECRET == 'default_secret':
    raise ValueError("Environment variables not set correctly. Check your .env file or platform settings.")

try:
    # 初始化 LineBot API 和 WebhookHandler
    line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
    handler = WebhookHandler(LINE_CHANNEL_SECRET)
    print("Initialization successful!")

    # 測試 BaseHTTPRequestHandler 是否正確設置
except Exception as e:
    print("Initialization failed:", str(e))
