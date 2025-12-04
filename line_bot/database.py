#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
データベース管理
"""

import sqlite3
import json
from datetime import datetime, date
from typing import Optional, Dict, List


class Database:
    """ユーザーデータを管理するデータベースクラス"""

    def __init__(self, db_path='diet_mentor.db'):
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        """データベース接続を取得"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """データベーステーブルを初期化"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # ユーザープロフィールテーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                name TEXT,
                gender TEXT,
                age INTEGER,
                height REAL,
                activity_level TEXT,
                activity_coefficient REAL,
                diet_mode TEXT,
                reduction_rate REAL,
                current_weight REAL,
                initial_weight REAL,
                target_weight REAL,
                target_calories REAL,
                target_protein REAL,
                target_fat REAL,
                target_carbs REAL,
                bmr REAL,
                tdee REAL,
                plan_name TEXT,
                duration_days INTEGER,
                start_date TEXT,
                current_day INTEGER DEFAULT 1,
                conversation_state TEXT DEFAULT 'initial',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 日々の記録テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                date TEXT NOT NULL,
                day_number INTEGER,
                weight REAL,
                exercise TEXT,
                meal TEXT,
                calories REAL,
                protein REAL,
                fat REAL,
                carbs REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                UNIQUE(user_id, date)
            )
        ''')

        # フィードバックテーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedbacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                achievements TEXT,
                good_points TEXT,
                overall_feedback TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')

        conn.commit()
        conn.close()
        print("✅ データベース初期化完了")

    def create_user(self, user_id: str, profile: Dict) -> bool:
        """新規ユーザーを作成"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO users (
                    user_id, name, gender, age, height, activity_level,
                    activity_coefficient, diet_mode, reduction_rate,
                    current_weight, initial_weight, target_weight,
                    target_calories, target_protein, target_fat, target_carbs,
                    bmr, tdee, plan_name, duration_days, start_date,
                    conversation_state
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'active')
            ''', (
                user_id,
                profile.get('name'),
                profile.get('gender'),
                profile.get('age'),
                profile.get('height'),
                profile.get('activity_name'),
                profile.get('activity_coefficient'),
                profile.get('diet_mode'),
                profile.get('reduction_rate'),
                profile.get('current_weight'),
                profile.get('initial_weight'),
                profile.get('target_weight'),
                profile.get('target_calories'),
                profile.get('target_protein'),
                profile.get('target_fat'),
                profile.get('target_carbs'),
                profile.get('bmr'),
                profile.get('tdee'),
                profile.get('plan_name'),
                profile.get('duration_days'),
                date.today().isoformat()
            ))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def get_user(self, user_id: str) -> Optional[Dict]:
        """ユーザー情報を取得"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    def update_user(self, user_id: str, updates: Dict) -> bool:
        """ユーザー情報を更新"""
        conn = self.get_connection()
        cursor = conn.cursor()

        set_clause = ', '.join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values()) + [user_id]

        try:
            cursor.execute(f'''
                UPDATE users
                SET {set_clause}, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', values)
            conn.commit()
            return True
        except Exception as e:
            print(f"⚠️ ユーザー更新エラー: {e}")
            return False
        finally:
            conn.close()

    def add_daily_record(self, user_id: str, record: Dict) -> bool:
        """日々の記録を追加"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT OR REPLACE INTO daily_records (
                    user_id, date, day_number, weight, exercise, meal,
                    calories, protein, fat, carbs
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                record.get('date', date.today().isoformat()),
                record.get('day_number'),
                record.get('weight'),
                record.get('exercise'),
                record.get('meal'),
                record.get('calories'),
                record.get('protein'),
                record.get('fat'),
                record.get('carbs')
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"⚠️ 記録追加エラー: {e}")
            return False
        finally:
            conn.close()

    def get_daily_records(self, user_id: str, limit: int = 30) -> List[Dict]:
        """日々の記録を取得"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM daily_records
            WHERE user_id = ?
            ORDER BY date DESC
            LIMIT ?
        ''', (user_id, limit))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_today_record(self, user_id: str) -> Optional[Dict]:
        """今日の記録を取得"""
        conn = self.get_connection()
        cursor = conn.cursor()

        today = date.today().isoformat()
        cursor.execute('''
            SELECT * FROM daily_records
            WHERE user_id = ? AND date = ?
        ''', (user_id, today))

        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    def get_users_without_today_record(self) -> List[str]:
        """今日の記録がないユーザーIDのリストを取得"""
        conn = self.get_connection()
        cursor = conn.cursor()

        today = date.today().isoformat()
        cursor.execute('''
            SELECT u.user_id
            FROM users u
            LEFT JOIN daily_records dr
                ON u.user_id = dr.user_id AND dr.date = ?
            WHERE u.conversation_state = 'active'
                AND dr.id IS NULL
        ''', (today,))

        rows = cursor.fetchall()
        conn.close()

        return [row['user_id'] for row in rows]

    def save_feedback(self, user_id: str, feedback: Dict) -> bool:
        """卒業時のフィードバックを保存"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO feedbacks (
                    user_id, achievements, good_points, overall_feedback
                ) VALUES (?, ?, ?, ?)
            ''', (
                user_id,
                feedback.get('achievements'),
                feedback.get('good_points'),
                feedback.get('overall_feedback')
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"⚠️ フィードバック保存エラー: {e}")
            return False
        finally:
            conn.close()

    def get_weight_history(self, user_id: str) -> List[float]:
        """体重履歴を取得（グラフ生成用）"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT weight FROM daily_records
            WHERE user_id = ? AND weight IS NOT NULL
            ORDER BY date ASC
        ''', (user_id,))

        rows = cursor.fetchall()
        conn.close()

        return [row['weight'] for row in rows]
