#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LINE Bot連携サンプルコード
※実装時にはline-bot-sdkのインストールが必要です
pip install line-bot-sdk
"""

# NOTE: このファイルは実装例です。実際に使用する場合は以下の手順を実行してください：
#
# 1. LINE Developers (https://developers.line.biz/) でMessaging APIチャネルを作成
# 2. Channel Access TokenとChannel Secretを取得
# 3. 環境変数に設定：
#    export LINE_CHANNEL_ACCESS_TOKEN='your-channel-access-token'
#    export LINE_CHANNEL_SECRET='your-channel-secret'
# 4. line-bot-sdkをインストール：
#    pip install line-bot-sdk flask
# 5. このファイルを参考に実装

import os
from flask import Flask, request, abort
from response_generator import ResponseGenerator

# LINE Bot SDKのインポート（実装時にコメント解除）
# from linebot import LineBotApi, WebhookHandler
# from linebot.exceptions import InvalidSignatureError
# from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 環境変数から認証情報を取得
# LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
# LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')
# GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# LINE Bot APIとWebhook Handlerの初期化
# line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
# handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 返信生成システムの初期化
# response_generator = ResponseGenerator(GEMINI_API_KEY)


@app.route("/callback", methods=['POST'])
def callback():
    """
    LINEからのWebhookを受け取るエンドポイント
    """
    # 実装例：
    # signature = request.headers['X-Line-Signature']
    # body = request.get_data(as_text=True)
    #
    # try:
    #     handler.handle(body, signature)
    # except InvalidSignatureError:
    #     abort(400)
    #
    # return 'OK'

    return "LINE Bot is not configured yet. Please set up LINE credentials."


# @handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """
    テキストメッセージを受信したときの処理

    Args:
        event: LINEからのメッセージイベント
    """
    # 実装例：
    #
    # # ユーザーのメッセージを取得
    # user_message = event.message.text
    #
    # # ユーザー名を取得（オプション）
    # user_id = event.source.user_id
    # profile = line_bot_api.get_profile(user_id)
    # user_name = profile.display_name
    #
    # # 返信メッセージを生成
    # response = response_generator.generate_response(user_message, user_name)
    # reply_message = response['message']
    #
    # # LINEに返信
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=reply_message)
    # )

    pass


def send_push_message(user_id, message):
    """
    特定のユーザーにプッシュメッセージを送信

    Args:
        user_id (str): LINEユーザーID
        message (str): 送信するメッセージ
    """
    # 実装例：
    # line_bot_api.push_message(
    #     user_id,
    #     TextSendMessage(text=message)
    # )

    pass


def send_daily_motivation():
    """
    毎日の励ましメッセージを全ユーザーに送信
    （cronやスケジューラーから呼び出す想定）
    """
    # 実装例：
    #
    # # データベースから全ユーザーを取得
    # users = get_all_users()  # 独自実装が必要
    #
    # # 励ましメッセージを生成
    # response = response_generator.generate_response(
    #     "今日も頑張ります！",
    #     None
    # )
    #
    # # 全ユーザーに送信
    # for user in users:
    #     send_push_message(user['line_user_id'], response['message'])

    pass


if __name__ == "__main__":
    print("=" * 60)
    print("🤖 LINE Bot サンプルコード")
    print("=" * 60)
    print()
    print("このファイルは実装サンプルです。")
    print("実際に使用する場合は、以下の手順を実行してください：")
    print()
    print("1. LINE Developers でMessaging APIチャネルを作成")
    print("   https://developers.line.biz/")
    print()
    print("2. Channel Access TokenとChannel Secretを取得")
    print()
    print("3. 必要なパッケージをインストール：")
    print("   pip install line-bot-sdk flask")
    print()
    print("4. 環境変数を設定：")
    print("   export LINE_CHANNEL_ACCESS_TOKEN='your-token'")
    print("   export LINE_CHANNEL_SECRET='your-secret'")
    print("   export GEMINI_API_KEY='your-api-key'")
    print()
    print("5. コード内のコメントを解除して実装")
    print()
    print("6. サーバーを起動：")
    print("   python line_bot_example.py")
    print()
    print("7. ngrokなどでローカルサーバーを公開")
    print("   ngrok http 5000")
    print()
    print("8. LINE DevelopersのWebhook URLに登録")
    print("   https://your-ngrok-url/callback")
    print()
    print("=" * 60)

    # デモモード（開発用）
    # app.run(host='0.0.0.0', port=5000, debug=True)
