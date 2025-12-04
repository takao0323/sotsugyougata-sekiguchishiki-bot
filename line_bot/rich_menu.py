#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
リッチメニュー管理
"""

from linebot.models import RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, MessageAction
import requests


class RichMenuManager:
    """リッチメニューの作成・管理クラス"""

    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api

    def create_rich_menu(self):
        """
        リッチメニューを作成

        Returns:
            str: 作成されたリッチメニューID
        """
        # リッチメニューオブジェクトの定義
        rich_menu = RichMenu(
            size=RichMenuSize(width=2500, height=1686),
            selected=True,
            name="ダイエットメンター メニュー",
            chat_bar_text="メニュー",
            areas=[
                # 左上: 今日の記録
                RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=0, width=833, height=843),
                    action=MessageAction(label="今日の記録", text="📝 今日の記録")
                ),
                # 中央上: グラフ表示
                RichMenuArea(
                    bounds=RichMenuBounds(x=834, y=0, width=833, height=843),
                    action=MessageAction(label="グラフ", text="📊 グラフを見る")
                ),
                # 右上: プロフィール
                RichMenuArea(
                    bounds=RichMenuBounds(x=1667, y=0, width=833, height=843),
                    action=MessageAction(label="プロフィール", text="👤 プロフィール")
                ),
                # 左下: アドバイス
                RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=844, width=833, height=842),
                    action=MessageAction(label="アドバイス", text="💡 アドバイスがほしい")
                ),
                # 中央下: 目標確認
                RichMenuArea(
                    bounds=RichMenuBounds(x=834, y=844, width=833, height=842),
                    action=MessageAction(label="目標", text="🎯 目標確認")
                ),
                # 右下: ヘルプ
                RichMenuArea(
                    bounds=RichMenuBounds(x=1667, y=844, width=833, height=842),
                    action=MessageAction(label="ヘルプ", text="❓ ヘルプ")
                ),
            ]
        )

        # リッチメニューを作成
        rich_menu_id = self.line_bot_api.create_rich_menu(rich_menu=rich_menu)
        print(f"✅ リッチメニュー作成: {rich_menu_id}")

        # リッチメニュー画像をアップロード（後で実装）
        # この段階では画像なしでテキストのみのリッチメニュー
        # 実際には画像を作成してアップロードする必要があります
        try:
            self.upload_rich_menu_image(rich_menu_id)
        except Exception as e:
            print(f"⚠️ リッチメニュー画像アップロードスキップ: {e}")

        return rich_menu_id

    def upload_rich_menu_image(self, rich_menu_id):
        """
        リッチメニュー画像をアップロード

        Args:
            rich_menu_id (str): リッチメニューID
        """
        # 画像パス（実際には画像ファイルを用意する必要があります）
        # ここでは簡易的にスキップ
        # 実装例:
        # with open('rich_menu_image.png', 'rb') as f:
        #     self.line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)
        pass

    def set_default_rich_menu(self, rich_menu_id):
        """
        デフォルトのリッチメニューとして設定

        Args:
            rich_menu_id (str): リッチメニューID
        """
        try:
            self.line_bot_api.set_default_rich_menu(rich_menu_id)
            print(f"✅ デフォルトリッチメニュー設定: {rich_menu_id}")
        except Exception as e:
            print(f"⚠️ デフォルトリッチメニュー設定エラー: {e}")

    def link_rich_menu_to_user(self, user_id, rich_menu_id):
        """
        特定ユーザーにリッチメニューをリンク

        Args:
            user_id (str): ユーザーID
            rich_menu_id (str): リッチメニューID
        """
        try:
            self.line_bot_api.link_rich_menu_to_user(user_id, rich_menu_id)
            print(f"✅ リッチメニューをユーザーにリンク: {user_id}")
        except Exception as e:
            print(f"⚠️ リッチメニューリンクエラー: {e}")

    def delete_all_rich_menus(self):
        """すべてのリッチメニューを削除（リセット用）"""
        try:
            rich_menu_list = self.line_bot_api.get_rich_menu_list()
            for rich_menu in rich_menu_list:
                self.line_bot_api.delete_rich_menu(rich_menu.rich_menu_id)
                print(f"🗑️ リッチメニュー削除: {rich_menu.rich_menu_id}")
        except Exception as e:
            print(f"⚠️ リッチメニュー削除エラー: {e}")
