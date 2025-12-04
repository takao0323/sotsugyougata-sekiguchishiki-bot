#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
卒業型ダイエットメンター LINE Bot
"""

import os
import sys
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    ImageSendMessage, QuickReply, QuickReplyButton,
    MessageAction, FlexSendMessage
)
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import datetime
import pytz

# 親ディレクトリをパスに追加（sekiguchi_botモジュールを使用するため）
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Database
from message_handler import MessageHandler
from rich_menu import RichMenuManager
from reminder import ReminderService

app = Flask(__name__)

# 環境変数から設定を取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    print("エラー: 環境変数 LINE_CHANNEL_ACCESS_TOKEN と LINE_CHANNEL_SECRET を設定してください")
    sys.exit(1)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# データベース初期化
db = Database()

# メッセージハンドラー初期化
message_handler = MessageHandler(db, line_bot_api)

# リッチメニュー初期化
rich_menu_manager = RichMenuManager(line_bot_api)

# リマインダーサービス初期化
reminder_service = ReminderService(db, line_bot_api)

# スケジューラー設定（毎日10時にリマインダー送信）
scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Tokyo'))
scheduler.add_job(
    func=reminder_service.send_daily_reminders,
    trigger=CronTrigger(hour=10, minute=0),
    id='daily_reminder',
    name='毎日10時のリマインダー',
    replace_existing=True
)
scheduler.start()


@app.route("/callback", methods=['POST'])
def callback():
    """LINE Webhook エンドポイント"""
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
    """テキストメッセージを受信したときの処理"""
    user_id = event.source.user_id
    text = event.message.text

    # メッセージを処理
    message_handler.handle_text_message(user_id, text, event)


@app.route("/")
def index():
    """ヘルスチェック用エンドポイント"""
    return "卒業型ダイエットメンター LINE Bot is running!"


@app.route("/setup_rich_menu", methods=['GET'])
def setup_rich_menu():
    """リッチメニューをセットアップ（初回のみ実行）"""
    try:
        rich_menu_id = rich_menu_manager.create_rich_menu()
        rich_menu_manager.set_default_rich_menu(rich_menu_id)
        return f"リッチメニューを作成しました: {rich_menu_id}"
    except Exception as e:
        return f"エラー: {str(e)}", 500


if __name__ == "__main__":
    print("=" * 60)
    print("🎓 卒業型ダイエットメンター LINE Bot")
    print("=" * 60)
    print("Starting server...")
    print(f"Scheduler started. Next reminder: 毎日10:00")
    print("=" * 60)

    # リッチメニューを自動セットアップ（初回起動時）
    try:
        rich_menu_id = rich_menu_manager.create_rich_menu()
        rich_menu_manager.set_default_rich_menu(rich_menu_id)
        print(f"✅ リッチメニュー作成完了: {rich_menu_id}")
    except Exception as e:
        print(f"⚠️ リッチメニュー作成エラー（既に存在する可能性）: {e}")

    # Flaskアプリ起動
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
