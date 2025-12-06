#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DailyRecordモデル - 日次記録情報
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Date, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.user import Base


class DailyRecord(Base):
    """日次記録モデル"""
    __tablename__ = 'daily_records'
    __table_args__ = (
        UniqueConstraint('user_id', 'record_date', name='uq_user_date'),
    )

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey('users.user_id'), nullable=False)
    record_date = Column(Date, nullable=False)
    day_count = Column(Integer, nullable=False)  # 1日目、2日目...

    # Phase 1: 体重のみ
    weight = Column(Float, nullable=False)

    # Phase 2: 食事記録
    calories = Column(Float)
    protein = Column(Float)
    fat = Column(Float)
    carbs = Column(Float)
    exercise = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    # リレーション
    user = relationship('User', back_populates='daily_records')

    def to_dict(self):
        """辞書形式に変換"""
        return {
            'record_id': self.record_id,
            'user_id': self.user_id,
            'record_date': self.record_date.isoformat() if self.record_date else None,
            'day_count': self.day_count,
            'weight': self.weight,
            'calories': self.calories,
            'protein': self.protein,
            'fat': self.fat,
            'carbs': self.carbs,
            'exercise': self.exercise,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<DailyRecord user_id={self.user_id} date={self.record_date} weight={self.weight}>"
