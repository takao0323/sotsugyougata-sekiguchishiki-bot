#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
食事画像解析モジュール
Google Gemini APIを使用して食事画像からカロリー・PFCバランスを自動計算
"""

import google.generativeai as genai
from PIL import Image
import json
import os


def setup_gemini_api(api_key=None):
    """
    Gemini APIのセットアップ

    Args:
        api_key (str, optional): Google Gemini APIキー。
                                 指定しない場合は環境変数GEMINI_API_KEYを使用

    Returns:
        bool: セットアップが成功した場合True、失敗した場合False
    """
    if api_key is None:
        api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print("⚠️ APIキーが設定されていません")
        print("\n【APIキーの設定方法】")
        print("1. Google AI Studio (https://makersuite.google.com/app/apikey) でAPIキーを取得")
        print("2. 以下のいずれかの方法で設定:")
        print("   方法1: 環境変数を設定")
        print("          export GEMINI_API_KEY='your-api-key'")
        print("   方法2: プログラム起動時に入力")
        return False

    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        print(f"⚠️ APIのセットアップに失敗しました: {e}")
        return False


def analyze_food_image(image_path, api_key=None):
    """
    食事画像を解析し、カロリーとPFCバランスを推定する

    Args:
        image_path (str): 食事画像のパス
        api_key (str, optional): Google Gemini APIキー

    Returns:
        dict or None: 解析結果（カロリー、タンパク質、脂質、炭水化物、食事内容）
                     失敗した場合はNone
    """
    # APIのセットアップ
    if not setup_gemini_api(api_key):
        return None

    # 画像が存在するか確認
    if not os.path.exists(image_path):
        print(f"⚠️ 画像ファイルが見つかりません: {image_path}")
        return None

    try:
        # 画像を読み込む
        img = Image.open(image_path)

        # Gemini Pro Visionモデルを使用
        model = genai.GenerativeModel('gemini-1.5-flash')

        # プロンプトを作成
        prompt = """
この画像に写っている食事を分析して、以下の情報をJSON形式で返してください。
可能な限り正確に推定してください。

返すJSON形式（日本語で返してください）:
{
    "meal_description": "食事の説明（例: 鶏胸肉のソテー、ブロッコリー、玄米）",
    "total_calories": 総カロリー（kcal、数値のみ）,
    "protein": タンパク質（g、数値のみ）,
    "fat": 脂質（g、数値のみ）,
    "carbs": 炭水化物（g、数値のみ）
}

注意点:
- 数値は小数点第1位まで
- 食材の量を推測して計算してください
- 複数の料理がある場合は合計を出してください
- 不明な場合は一般的な値を使用してください
"""

        # 画像を解析
        print("🔍 画像を解析中...")
        response = model.generate_content([prompt, img])

        # レスポンステキストを取得
        response_text = response.text.strip()

        # JSONとして解析
        # レスポンスからJSON部分を抽出（```json ... ``` のような形式の場合）
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            json_text = response_text[json_start:json_end].strip()
        elif "```" in response_text:
            json_start = response_text.find("```") + 3
            json_end = response_text.find("```", json_start)
            json_text = response_text[json_start:json_end].strip()
        else:
            json_text = response_text

        # JSONをパース
        result = json.loads(json_text)

        # 必要なキーが含まれているか確認
        required_keys = ["meal_description", "total_calories", "protein", "fat", "carbs"]
        if not all(key in result for key in required_keys):
            print("⚠️ APIからの応答が不完全です")
            return None

        print("✅ 解析が完了しました！")
        return result

    except FileNotFoundError:
        print(f"⚠️ 画像ファイルが見つかりません: {image_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"⚠️ 解析結果のJSON解析に失敗しました: {e}")
        print(f"レスポンス: {response_text}")
        return None
    except Exception as e:
        print(f"⚠️ 画像解析中にエラーが発生しました: {e}")
        return None


def get_image_path_from_user():
    """
    ユーザーから画像パスを取得する

    Returns:
        str or None: 画像パス（キャンセルの場合はNone）
    """
    print("\n【食事画像のアップロード】")
    print("食事の写真・スクリーンショットのパスを入力してください")
    print("（例: /home/user/Pictures/meal.jpg）")
    print("（手動入力したい場合は「手動」と入力してください）")

    while True:
        image_path = input("> ").strip()

        # 手動入力の場合
        if image_path == "手動":
            return None

        # 空の場合
        if not image_path:
            print("⚠️ パスを入力してください")
            continue

        # ファイルの存在確認
        if os.path.exists(image_path):
            # 画像ファイルかどうか確認
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
            if any(image_path.lower().endswith(ext) for ext in valid_extensions):
                return image_path
            else:
                print("⚠️ 画像ファイルではありません。有効な画像形式: jpg, jpeg, png, gif, bmp, webp")
        else:
            print(f"⚠️ ファイルが見つかりません: {image_path}")
            print("もう一度入力してください")


def display_nutrition_info(analysis_result):
    """
    解析結果を表示する

    Args:
        analysis_result (dict): analyze_food_image()の返り値
    """
    if analysis_result is None:
        print("⚠️ 解析結果がありません")
        return

    print("\n" + "=" * 60)
    print("【解析結果】")
    print("=" * 60)
    print(f"📝 食事内容: {analysis_result['meal_description']}")
    print()
    print(f"🔥 総カロリー: {analysis_result['total_calories']}kcal")
    print(f"💪 タンパク質 (P): {analysis_result['protein']}g")
    print(f"🥑 脂質 (F): {analysis_result['fat']}g")
    print(f"🍚 炭水化物 (C): {analysis_result['carbs']}g")
    print("=" * 60)


# テスト用のmain関数
if __name__ == "__main__":
    print("=" * 60)
    print("🍽️  食事画像解析ツール")
    print("=" * 60)
    print()

    # APIキーの確認
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("APIキーを入力してください:")
        api_key = input("> ").strip()

    # 画像パスを取得
    image_path = get_image_path_from_user()

    if image_path:
        # 画像を解析
        result = analyze_food_image(image_path, api_key)

        # 結果を表示
        if result:
            display_nutrition_info(result)
        else:
            print("⚠️ 解析に失敗しました")
    else:
        print("キャンセルされました")
