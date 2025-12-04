#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
メッセージハンドラー
ユーザーからのメッセージを処理
"""

import sys
import os
from datetime import date
from linebot.models import (
    TextSendMessage, QuickReply, QuickReplyButton,
    MessageAction, FlexSendMessage, ImageSendMessage
)
import random

# 親ディレクトリのモジュールをインポート
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sekiguchi_bot.main import (
    calculate_bmr, calculate_target_calories_and_pfc,
    generate_stagnation_advice, create_nutrition_graphs
)


class MessageHandler:
    """メッセージ処理クラス"""

    def __init__(self, database, line_bot_api):
        self.db = database
        self.line_bot_api = line_bot_api

    def handle_text_message(self, user_id: str, text: str, event):
        """
        テキストメッセージを処理

        Args:
            user_id (str): ユーザーID
            text (str): メッセージテキスト
            event: LINEイベントオブジェクト
        """
        # ユーザー情報を取得
        user = self.db.get_user(user_id)

        # リッチメニューからのアクション
        if text in ["📝 今日の記録", "📊 グラフを見る", "👤 プロフィール",
                    "💡 アドバイスがほしい", "🎯 目標確認", "❓ ヘルプ"]:
            self.handle_rich_menu_action(user_id, text, user)
            return

        # 新規ユーザー
        if not user:
            self.start_registration(user_id)
            return

        # 会話状態に応じて処理
        state = user.get('conversation_state', 'initial')

        if state == 'active':
            # アクティブユーザー：日々の入力
            self.handle_active_user_message(user_id, text, user)
        elif state.startswith('register_'):
            # 登録プロセス中
            self.handle_registration(user_id, text, user, state)
        elif state.startswith('daily_'):
            # 日々の記録中
            self.handle_daily_input(user_id, text, user, state)
        else:
            # その他
            self.send_help_message(user_id)

    def handle_rich_menu_action(self, user_id: str, text: str, user: dict):
        """リッチメニューからのアクション処理"""

        if text == "📝 今日の記録":
            if not user:
                self.start_registration(user_id)
            else:
                self.start_daily_input(user_id, user)

        elif text == "📊 グラフを見る":
            self.send_weight_graph(user_id, user)

        elif text == "👤 プロフィール":
            self.send_profile_info(user_id, user)

        elif text == "💡 アドバイスがほしい":
            self.send_advice(user_id, user)

        elif text == "🎯 目標確認":
            self.send_goal_info(user_id, user)

        elif text == "❓ ヘルプ":
            self.send_help_message(user_id)

    def start_registration(self, user_id: str):
        """新規登録を開始"""
        welcome_message = """🎓 卒業型ダイエットメンターへようこそ！

世界で証明されたダイエット理論を、あなた専属のAIメンターが完全再現。"最後のダイエットパートナー"

まずはプロフィール登録から始めましょう。

【お名前】何とお呼びすればよいですか？"""

        self.line_bot_api.reply_message(
            event.reply_token if hasattr(self, 'event') else None,
            TextSendMessage(text=welcome_message)
        )

        # 会話状態を更新（仮のユーザーレコード作成）
        self.db.create_user(user_id, {
            'name': None,
            'conversation_state': 'register_name'
        })

    def handle_registration(self, user_id: str, text: str, user: dict, state: str):
        """
        登録プロセスを処理

        状態遷移:
        register_name -> register_gender -> register_age -> register_height
        -> register_activity -> register_mode -> register_current_weight
        -> register_target_weight -> register_plan -> complete
        """
        # 実装は長くなるため、簡略化版
        # 実際には各ステップで入力を検証し、次のステップへ進む

        if state == 'register_name':
            # 名前を保存
            self.db.update_user(user_id, {
                'name': text,
                'conversation_state': 'register_gender'
            })
            reply = f"{text}さん、よろしくお願いします！\n\n【性別】性別を教えてください"

            quick_reply = QuickReply(items=[
                QuickReplyButton(action=MessageAction(label="男性", text="男性")),
                QuickReplyButton(action=MessageAction(label="女性", text="女性")),
            ])

            self.line_bot_api.push_message(
                user_id,
                TextSendMessage(text=reply, quick_reply=quick_reply)
            )

        # ... 他の登録ステップも同様に実装 ...
        # (完全な実装は非常に長くなるため、ここでは概要のみ)

    def start_daily_input(self, user_id: str, user: dict):
        """日々の記録入力を開始"""
        name = user.get('name', 'あなた')
        day = user.get('current_day', 1)
        max_days = user.get('duration_days', 90)

        message = f"""📅 {day}日目 / {max_days}日

{name}さん、今日の記録を始めましょう！

【体重】今日の体重は何kgですか？
（数字のみ入力してください。例: 75.5）"""

        self.line_bot_api.push_message(
            user_id,
            TextSendMessage(text=message)
        )

        # 会話状態を更新
        self.db.update_user(user_id, {
            'conversation_state': 'daily_weight'
        })

    def handle_daily_input(self, user_id: str, text: str, user: dict, state: str):
        """日々の記録入力を処理"""

        if state == 'daily_weight':
            # 体重を保存
            try:
                weight = float(text)
                # 一時保存（セッション管理が必要）
                # 簡略化のため、直接DBに保存
                today = date.today().isoformat()
                self.db.add_daily_record(user_id, {
                    'date': today,
                    'day_number': user.get('current_day', 1),
                    'weight': weight
                })

                # 次のステップへ
                self.db.update_user(user_id, {
                    'current_weight': weight,
                    'conversation_state': 'daily_exercise'
                })

                reply = "ありがとうございます！\n\n【運動】今日やった運動を教えてください\n（例: 30分ジョギング、筋トレ、なし）"
                self.line_bot_api.push_message(
                    user_id,
                    TextSendMessage(text=reply)
                )
            except ValueError:
                self.line_bot_api.push_message(
                    user_id,
                    TextSendMessage(text="⚠️ 数字で入力してください（例: 75.5）")
                )

        # ... 他の入力ステップも同様に実装 ...

    def handle_active_user_message(self, user_id: str, text: str, user: dict):
        """アクティブユーザーのメッセージ処理"""

        if text in ["後で記録します", "スキップ"]:
            name = user.get('name', 'あなた')
            reply = f"{name}さん、了解しました！\n\n記録したくなったら、いつでもメニューから「今日の記録」をタップしてくださいね。"
            self.line_bot_api.push_message(
                user_id,
                TextSendMessage(text=reply)
            )
        else:
            # デフォルト：今日の記録を開始
            self.start_daily_input(user_id, user)

    def send_weight_graph(self, user_id: str, user: dict):
        """体重グラフを送信"""
        if not user:
            return

        weight_history = self.db.get_weight_history(user_id)

        if len(weight_history) < 2:
            message = "まだグラフを表示するのに十分なデータがありません。\n\n2日以上記録をつけるとグラフが表示されます。"
            self.line_bot_api.push_message(
                user_id,
                TextSendMessage(text=message)
            )
            return

        # グラフ生成（sekiguchi_bot の関数を利用）
        # ここでは簡略化
        message = f"📊 体重の推移\n\n開始: {weight_history[0]}kg\n現在: {weight_history[-1]}kg\n変化: {weight_history[0] - weight_history[-1]:.1f}kg"

        self.line_bot_api.push_message(
            user_id,
            TextSendMessage(text=message)
        )

    def send_profile_info(self, user_id: str, user: dict):
        """プロフィール情報を送信"""
        if not user:
            return

        name = user.get('name', '')
        gender = user.get('gender', '')
        age = user.get('age', '')
        height = user.get('height', '')
        current_weight = user.get('current_weight', '')
        target_weight = user.get('target_weight', '')
        plan_name = user.get('plan_name', '')

        message = f"""👤 プロフィール

お名前: {name}さん
性別: {gender}
年齢: {age}歳
身長: {height}cm

現在の体重: {current_weight}kg
目標体重: {target_weight}kg
プラン: {plan_name}

💪 一緒に頑張りましょう！"""

        self.line_bot_api.push_message(
            user_id,
            TextSendMessage(text=message)
        )

    def send_advice(self, user_id: str, user: dict):
        """アドバイスを送信"""
        if not user:
            return

        # 関口さん風のアドバイスを生成
        advice = generate_stagnation_advice()

        self.line_bot_api.push_message(
            user_id,
            TextSendMessage(text=advice)
        )

    def send_goal_info(self, user_id: str, user: dict):
        """目標情報を送信"""
        if not user:
            return

        target_cal = user.get('target_calories', 0)
        target_p = user.get('target_protein', 0)
        target_f = user.get('target_fat', 0)
        target_c = user.get('target_carbs', 0)

        message = f"""🎯 あなたの目標

📊 1日の目標摂取カロリー
{target_cal:.0f}kcal

💪 タンパク質（P）: {target_p:.1f}g（30%）
🥑 脂質（F）: {target_f:.1f}g（20%）
🍚 炭水化物（C）: {target_c:.1f}g（50%）

💡 これらの数字はあくまで目安です。
±10%の範囲なら全く問題ありません。
大切なのは完璧を目指すことではなく、続けることです。"""

        self.line_bot_api.push_message(
            user_id,
            TextSendMessage(text=message)
        )

    def send_help_message(self, user_id: str):
        """ヘルプメッセージを送信"""
        message = """❓ ヘルプ

【使い方】
画面下のメニューから操作できます。

📝 今日の記録
→ 体重・運動・食事を記録

📊 グラフを見る
→ 体重の推移をグラフで確認

👤 プロフィール
→ あなたの情報を確認

💡 アドバイスがほしい
→ 関口さん風のアドバイスを受ける

🎯 目標確認
→ カロリーやPFC目標を確認

❓ ヘルプ
→ この画面

【リマインダー】
毎日10時に記録のリマインダーが届きます。

【お問い合わせ】
困ったことがあれば、いつでもメッセージを送ってください！"""

        self.line_bot_api.push_message(
            user_id,
            TextSendMessage(text=message)
        )
