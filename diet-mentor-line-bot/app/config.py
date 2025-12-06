#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
アプリケーション設定
環境変数から設定を読み込む
"""

import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()


class Config:
    """基本設定"""

    # Flask設定
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'

    # データベース設定
    # 開発環境: SQLite
    # 本番環境: PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///diet_mentor.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG  # SQL文をログ出力（デバッグモードのみ）

    # LINE Bot設定
    LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
    LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')

    # Google Gemini API設定（Phase 2）
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

    # LIFF設定
    LIFF_ID = os.environ.get('LIFF_ID')

    # アプリケーション設定
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大16MBのファイルアップロード

    # タイムゾーン
    TIMEZONE = 'Asia/Tokyo'

    # ダイエット設定
    # 減量ペース
    LIGHT_MODE_RATE = 0.02  # ライトモード: 月2%
    HARD_MODE_RATE = 0.04   # ハードモード: 月4%
    MAX_REDUCTION_RATE = 0.04  # 最大減量ペース: 月4%

    # PFCバランス（理想値）
    PFC_PROTEIN_RATIO = 0.30  # タンパク質: 30%
    PFC_FAT_RATIO = 0.20      # 脂質: 20%
    PFC_CARB_RATIO = 0.50     # 炭水化物: 50%

    # 活動係数
    ACTIVITY_COEFFICIENT = 1.4  # 軽い運動を前提

    # 挫折予測AI設定
    DROPOUT_CALORIE_EXCESS_DAYS = 3    # カロリー超過連続日数
    DROPOUT_STAGNATION_DAYS = 7        # 体重停滞日数
    DROPOUT_PROTEIN_DEFICIENCY_DAYS = 2 # タンパク質不足日数
    DROPOUT_MISSING_RECORD_DAYS = 2    # 記録忘れ日数

    DROPOUT_WEIGHT_STAGNATION_THRESHOLD = 0.3  # 体重変化の閾値（kg）
    DROPOUT_WEIGHT_INCREASE_THRESHOLD = 0.5    # 体重増加の閾値（kg）

    # グラフ設定
    GRAPH_DPI = 100
    GRAPH_FIGURE_SIZE = (10, 6)
    GRAPH_LINE_WIDTH = 2
    GRAPH_MARKER_SIZE = 8


def get_config():
    """現在の環境に応じた設定を取得"""
    return Config
