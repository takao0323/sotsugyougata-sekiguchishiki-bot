#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Feedbackモデル - フィードバック履歴情報
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Date, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.user import Base


class Feedback(Base):
    """フィードバック履歴モデル"""
    __tablename__ = 'feedback_history'

    feedback_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey('users.user_id'), nullable=False)
    record_date = Column(Date, nullable=False)
    feedback_type = Column(String(20), nullable=False)  # 'daily', 'weekly', 'monthly'
    feedback_content = Column(Text, nullable=False)
    dropout_risk_level = Column(String(10))  # 'low', 'medium', 'high'

    created_at = Column(DateTime, default=datetime.utcnow)

    # リレーション
    user = relationship('User', back_populates='feedbacks')

    def to_dict(self):
        """辞書形式に変換"""
        return {
            'feedback_id': self.feedback_id,
            'user_id': self.user_id,
            'record_date': self.record_date.isoformat() if self.record_date else None,
            'feedback_type': self.feedback_type,
            'feedback_content': self.feedback_content,
            'dropout_risk_level': self.dropout_risk_level,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<Feedback user_id={self.user_id} type={self.feedback_type} date={self.record_date}>"
