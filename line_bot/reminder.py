#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
リマインダーサービス
毎日10時に体重入力がないユーザーに通知
"""

from datetime import datetime
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, MessageAction
import random


class ReminderService:
    """リマインダー送信サービス"""

    def __init__(self, database, line_bot_api):
        self.db = database
        self.line_bot_api = line_bot_api

    def send_daily_reminders(self):
        """
        毎日10時に実行：今日の記録がないユーザーにリマインダーを送信
        """
        print(f"[{datetime.now()}] リマインダー送信開始...")

        # 今日の記録がないユーザーを取得
        user_ids = self.db.get_users_without_today_record()

        if not user_ids:
            print("📭 リマインダー送信対象のユーザーなし")
            return

        print(f"📬 リマインダー送信対象: {len(user_ids)}人")

        for user_id in user_ids:
            try:
                self.send_reminder_to_user(user_id)
                print(f"✅ リマインダー送信完了: {user_id}")
            except Exception as e:
                print(f"⚠️ リマインダー送信エラー ({user_id}): {e}")

        print(f"[{datetime.now()}] リマインダー送信完了")

    def send_reminder_to_user(self, user_id: str):
        """
        個別ユーザーにリマインダーを送信

        Args:
            user_id (str): ユーザーID
        """
        user = self.db.get_user(user_id)
        if not user:
            return

        name = user.get('name', 'あなた')

        # ランダムなリマインダーメッセージ
        reminder_messages = [
            f"おはようございます、{name}さん！\n\n今朝の体重はいかがでしたか？😊",
            f"{name}さん、おはようございます！\n\n今日も一緒に頑張りましょう。\n今朝の体重を教えてください。",
            f"おはようございます！\n\n{name}さん、今朝の体重測定はお済みですか？\n記録をお待ちしています。",
            f"{name}さん、朝です！☀️\n\n今朝の体重を記録しましょう。\n継続が何より大切ですよ。",
            f"おはようございます、{name}さん！\n\n体重計に乗りましたか？\n今日も一歩前進しましょう！",
            f"{name}さん、新しい一日の始まりです！\n\n今朝の体重を記録して、\n良いスタートを切りましょう。",
            f"おはようございます！\n\n{name}さん、今日の体重測定の時間です。\nあなたならできます！",
            f"{name}さん、おはようございます！🌅\n\n毎日の記録が未来を作ります。\n今朝の体重を教えてくださいね。",
        ]

        message = random.choice(reminder_messages)

        # クイックリプライボタンを追加
        quick_reply = QuickReply(items=[
            QuickReplyButton(action=MessageAction(label="📝 今日の記録", text="📝 今日の記録")),
            QuickReplyButton(action=MessageAction(label="後で記録します", text="後で記録します")),
        ])

        self.line_bot_api.push_message(
            user_id,
            TextSendMessage(text=message, quick_reply=quick_reply)
        )

    def send_encouragement_reminder(self, user_id: str):
        """
        停滞時の励ましリマインダー（別途呼び出し用）

        Args:
            user_id (str): ユーザーID
        """
        user = self.db.get_user(user_id)
        if not user:
            return

        name = user.get('name', 'あなた')

        encouragement_messages = [
            f"{name}さん、継続できていること自体が素晴らしいです！\n\n今日も記録をつけましょう。",
            f"{name}さん、停滞期は成長のサインです。\n\n焦らず、今日も一歩ずつ。",
            f"{name}さん、完璧じゃなくていいんです。\n\n80点で十分。今日も続けましょう。",
            f"{name}さん、体重計の数字だけが全てじゃありません。\n\n今日も記録をつけて前進しましょう。",
        ]

        message = random.choice(encouragement_messages)

        self.line_bot_api.push_message(
            user_id,
            TextSendMessage(text=message)
        )

    def send_custom_reminder(self, user_id: str, message: str):
        """
        カスタムリマインダーを送信

        Args:
            user_id (str): ユーザーID
            message (str): 送信するメッセージ
        """
        try:
            self.line_bot_api.push_message(
                user_id,
                TextSendMessage(text=message)
            )
            print(f"✅ カスタムリマインダー送信完了: {user_id}")
        except Exception as e:
            print(f"⚠️ カスタムリマインダー送信エラー: {e}")
