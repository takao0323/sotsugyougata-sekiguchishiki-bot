#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Userモデル - ユーザープロフィール情報
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """ユーザー情報モデル"""
    __tablename__ = 'users'

    user_id = Column(String(50), primary_key=True)  # LINE User ID
    name = Column(String(50), nullable=False)
    gender = Column(String(10), nullable=False)  # '男性' or '女性'
    age = Column(Integer, nullable=False)
    height = Column(Float, nullable=False)
    current_weight = Column(Float, nullable=False)
    target_weight = Column(Float, nullable=False)
    diet_mode = Column(String(10), nullable=False)  # 'light' or 'hard'
    reduction_rate = Column(Float, nullable=False)  # 0.02 or 0.04

    # 計算された値
    bmr = Column(Float)  # 基礎代謝量
    tdee = Column(Float)  # 1日の消費カロリー
    target_calories = Column(Float)  # 目標カロリー
    target_protein = Column(Float)  # 目標タンパク質
    target_fat = Column(Float)  # 目標脂質
    target_carbs = Column(Float)  # 目標炭水化物

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # リレーション
    daily_records = relationship('DailyRecord', back_populates='user', cascade='all, delete-orphan')
    feedbacks = relationship('Feedback', back_populates='user', cascade='all, delete-orphan')

    def to_dict(self):
        """辞書形式に変換"""
        return {
            'user_id': self.user_id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
            'height': self.height,
            'current_weight': self.current_weight,
            'target_weight': self.target_weight,
            'diet_mode': self.diet_mode,
            'reduction_rate': self.reduction_rate,
            'bmr': self.bmr,
            'tdee': self.tdee,
            'target_calories': self.target_calories,
            'target_protein': self.target_protein,
            'target_fat': self.target_fat,
            'target_carbs': self.target_carbs,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<User {self.name} (user_id={self.user_id})>"
