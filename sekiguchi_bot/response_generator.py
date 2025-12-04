#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自動返信生成システム
ユーザーの質問・悩みに対して10000+パターンの返信を生成
"""

import random
import os
import google.generativeai as genai
from message_templates import (
    CATEGORIES,
    GREETINGS,
    EMPATHY,
    ADVICE_BY_CATEGORY,
    ENCOURAGEMENT,
    CLOSINGS
)


class ResponseGenerator:
    """自動返信メッセージ生成クラス"""

    def __init__(self, api_key=None):
        """
        初期化

        Args:
            api_key (str, optional): Google Gemini APIキー
        """
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
            print("⚠️ APIキーが設定されていません。キーワードマッチングで分類します。")

    def classify_question(self, question):
        """
        質問をカテゴリに分類する（AI使用）

        Args:
            question (str): ユーザーの質問・悩み

        Returns:
            str: カテゴリ名
        """
        if self.model is None:
            # APIキーがない場合はキーワードマッチング
            return self._classify_by_keyword(question)

        try:
            # AIで分類
            prompt = f"""
以下のユーザーの質問・悩みを、最も適切なカテゴリに分類してください。
カテゴリは以下の9つから1つだけ選んでください。

カテゴリ：
1. 食事・栄養
2. 運動・トレーニング
3. モチベーション・メンタル
4. 停滞期
5. 体重増加・リバウンド
6. 時間管理
7. 付き合い・外食
8. 睡眠・休息
9. 一般的な励まし

ユーザーの質問：
{question}

回答はカテゴリ名のみを返してください。他の文章は不要です。
"""

            response = self.model.generate_content(prompt)
            category = response.text.strip()

            # カテゴリが有効かチェック
            if category in CATEGORIES:
                return category
            else:
                # 無効な場合はキーワードマッチング
                return self._classify_by_keyword(question)

        except Exception as e:
            print(f"⚠️ AI分類に失敗しました: {e}")
            # エラー時はキーワードマッチング
            return self._classify_by_keyword(question)

    def _classify_by_keyword(self, question):
        """
        キーワードマッチングで分類（フォールバック用）

        Args:
            question (str): ユーザーの質問・悩み

        Returns:
            str: カテゴリ名
        """
        question_lower = question.lower()

        # キーワード定義
        keywords = {
            "食事・栄養": ["食事", "栄養", "カロリー", "タンパク質", "脂質", "炭水化物",
                          "PFC", "食べ", "食べる", "食べた", "食べて", "間食", "おやつ",
                          "朝食", "昼食", "夕食", "夜食", "飲み", "飲む"],
            "運動・トレーニング": ["運動", "トレーニング", "筋トレ", "有酸素", "ジョギング",
                                 "ウォーキング", "ジム", "筋肉", "スクワット", "腕立て",
                                 "プランク", "ストレッチ", "走る", "歩く"],
            "モチベーション・メンタル": ["モチベーション", "やる気", "続かない", "挫折",
                                       "辛い", "つらい", "難しい", "できない", "無理",
                                       "心", "メンタル", "気持ち", "不安", "心配"],
            "停滞期": ["停滞", "減らない", "変わらない", "痩せない", "体重が", "変化"],
            "体重増加・リバウンド": ["増えた", "太った", "リバウンド", "戻った", "増加"],
            "時間管理": ["時間", "忙しい", "できない", "余裕", "仕事", "予定"],
            "付き合い・外食": ["外食", "飲み会", "付き合い", "誘われ", "断れ", "会食",
                             "デート", "友達", "家族"],
            "睡眠・休息": ["睡眠", "眠", "寝", "疲れ", "休息", "休み", "疲労"],
        }

        # 各カテゴリのキーワードをチェック
        for category, words in keywords.items():
            for word in words:
                if word in question_lower:
                    return category

        # どのカテゴリにも該当しない場合
        return "一般的な励まし"

    def generate_response(self, question, user_name=None):
        """
        質問に対する返信メッセージを生成

        Args:
            question (str): ユーザーの質問・悩み
            user_name (str, optional): ユーザー名（あれば名前入り返信）

        Returns:
            dict: 返信情報（category, message, pattern_count）
        """
        # カテゴリを分類
        category = self.classify_question(question)

        # 各パーツをランダムに選択
        greeting = random.choice(GREETINGS)
        empathy = random.choice(EMPATHY)
        advice = random.choice(ADVICE_BY_CATEGORY[category])
        encouragement = random.choice(ENCOURAGEMENT)
        closing = random.choice(CLOSINGS)

        # メッセージを組み立て
        message_parts = []

        # 名前がある場合は挨拶に追加
        if user_name:
            message_parts.append(f"{user_name}さん、{greeting}")
        else:
            message_parts.append(greeting)

        message_parts.append(empathy)
        message_parts.append(advice)
        message_parts.append(encouragement)
        message_parts.append(closing)

        # 改行で結合
        message = "\n\n".join(message_parts)

        # パターン数を計算
        pattern_count = self._calculate_pattern_count(category)

        return {
            "category": category,
            "message": message,
            "pattern_count": pattern_count,
            "greeting": greeting,
            "empathy": empathy,
            "advice": advice,
            "encouragement": encouragement,
            "closing": closing
        }

    def _calculate_pattern_count(self, category):
        """
        指定カテゴリの組み合わせパターン数を計算

        Args:
            category (str): カテゴリ名

        Returns:
            int: パターン数
        """
        greeting_count = len(GREETINGS)
        empathy_count = len(EMPATHY)
        advice_count = len(ADVICE_BY_CATEGORY[category])
        encouragement_count = len(ENCOURAGEMENT)
        closing_count = len(CLOSINGS)

        total = (greeting_count * empathy_count * advice_count *
                 encouragement_count * closing_count)

        return total

    def get_total_pattern_count(self):
        """
        全カテゴリの合計パターン数を計算

        Returns:
            dict: カテゴリごとのパターン数と合計
        """
        result = {}
        total = 0

        for category in CATEGORIES:
            count = self._calculate_pattern_count(category)
            result[category] = count
            total += count

        result["合計"] = total

        return result


def demo():
    """
    デモンストレーション用の関数
    """
    print("=" * 60)
    print("🤖 ダイエットメンター 自動返信システム")
    print("=" * 60)
    print()

    # APIキーの確認
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("【注意】GEMINI_API_KEYが設定されていません")
        print("キーワードマッチングで分類します\n")

    # ジェネレーター初期化
    generator = ResponseGenerator(api_key)

    # パターン数を表示
    print("📊 利用可能なメッセージパターン数：")
    print("-" * 60)
    patterns = generator.get_total_pattern_count()
    for category, count in patterns.items():
        if category == "合計":
            print("-" * 60)
            print(f"✨ {category}: {count:,}パターン")
        else:
            print(f"   {category}: {count:,}パターン")
    print()

    # テスト質問
    test_questions = [
        ("太郎", "食事制限がきつくて続けられません"),
        ("花子", "運動する時間がなくて困っています"),
        ("次郎", "体重が全然減らなくて悩んでいます"),
        ("美咲", "昨日食べ過ぎて体重が増えました"),
        ("健一", "モチベーションが続きません"),
    ]

    print("=" * 60)
    print("💬 返信例（5パターン）")
    print("=" * 60)

    for user_name, question in test_questions:
        print()
        print(f"【質問】{user_name}さん: {question}")
        print("-" * 60)

        response = generator.generate_response(question, user_name)

        print(f"📁 分類カテゴリ: {response['category']}")
        print(f"🔢 このカテゴリのパターン数: {response['pattern_count']:,}")
        print()
        print("【返信メッセージ】")
        print(response['message'])
        print("=" * 60)


if __name__ == "__main__":
    demo()
