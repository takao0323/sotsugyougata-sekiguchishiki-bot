#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
挫折予測AIサービス
ユーザーの記録から挫折リスクを検知し、適切なサポートを提供
"""


def detect_dropout_risk(user, daily_records, day_count):
    """
    挫折リスクを検知する

    Args:
        user (User): ユーザーモデル
        daily_records (list[DailyRecord]): 日々の記録
        day_count (int): 現在の日数

    Returns:
        dict: リスク情報 {
            "risk_level": "low" | "medium" | "high",
            "reasons": [理由のリスト],
            "suggestions": [提案のリスト]
        }
    """
    risk_level = "low"
    reasons = []
    suggestions = []

    # Phase 1では体重のみを扱う
    # Phase 2でカロリー・PFCの検知を追加

    # 1. 停滞期の長期化を検知（直近7日）
    if len(daily_records) >= 8:  # 最低8日必要（初日含む）
        recent_records = daily_records[-8:]
        initial_weight = recent_records[0].weight
        final_weight = recent_records[-1].weight
        weight_change = initial_weight - final_weight

        # 7日間で0.3kg未満の変化 = 停滞期
        if abs(weight_change) < 0.3:
            if risk_level == "low":
                risk_level = "medium"
            reasons.append("体重が1週間以上停滞しています")
            suggestions.append("停滞期は成長のサインです。焦らず継続しましょう")
            suggestions.append("水分摂取、睡眠、ストレス管理を見直してみましょう")

        # 7日間で増加傾向 = 要注意
        elif weight_change < -0.5:
            risk_level = "high"
            reasons.append("体重が増加傾向にあります")
            suggestions.append("一時的な増加は誰にでもあります。諦めないでください")
            suggestions.append("基本に立ち返りましょう：カロリー・運動・睡眠")

    # 2. 記録の継続性チェック（day_countと記録数の比較）
    if len(daily_records) < day_count - 1:  # 記録が抜けている
        missing_days = day_count - 1 - len(daily_records)
        if missing_days >= 2:
            risk_level = "high"
            reasons.append(f"記録が{missing_days}日分抜けています")
            suggestions.append("完璧じゃなくて大丈夫！体重だけでも記録しましょう")
            suggestions.append("継続することが一番大切です")

    # Phase 2: カロリー・PFCの検知
    # カロリー超過の連続を検知（直近3日）
    if len(daily_records) >= 3:
        recent_records = daily_records[-3:]
        # カロリーデータがある場合のみチェック
        if all(r.calories is not None for r in recent_records):
            over_count = sum(1 for r in recent_records if r.calories > user.target_calories)

            if over_count == 3:
                risk_level = "high"
                reasons.append("3日連続でカロリー超過が続いています")
                suggestions.append("完璧を目指さなくて大丈夫！まずは目標の±10%以内を目指しましょう")
                suggestions.append("今日は「体重を測る」「記録する」だけでもOKです")
            elif over_count == 2:
                if risk_level == "low":
                    risk_level = "medium"
                reasons.append("カロリー超過が続いています")
                suggestions.append("無理に減らさなくて大丈夫。まずは現状維持を目指しましょう")

        # タンパク質不足の検知（直近3日）
        if all(r.protein is not None for r in recent_records):
            protein_deficiency_count = sum(
                1 for r in recent_records
                if r.protein < user.target_protein * 0.7
            )

            if protein_deficiency_count >= 2:
                if risk_level == "low":
                    risk_level = "medium"
                reasons.append("タンパク質の摂取量が不足しています")
                suggestions.append("筋肉を維持するため、タンパク質をしっかり摂りましょう")
                suggestions.append("プロテイン、サラダチキン、卵など手軽なものでOKです")

    return {
        "risk_level": risk_level,
        "reasons": reasons,
        "suggestions": suggestions
    }


def format_support_message(risk_info, user_name):
    """
    挫折リスクに応じた特別サポートメッセージをフォーマット

    Args:
        risk_info (dict): リスク情報
        user_name (str): ユーザー名

    Returns:
        str: フォーマットされたメッセージ（LINE送信用）
    """
    if risk_info["risk_level"] == "low":
        return ""  # リスク低い場合は空文字を返す

    # メッセージを構築
    lines = []
    lines.append("⚠️" * 10)
    lines.append("")

    if risk_info["risk_level"] == "high":
        lines.append("【🚨 関口からの緊急メッセージ 🚨】")
    else:
        lines.append("【💡 関口からのアドバイス 💡】")

    lines.append("=" * 30)
    lines.append(f"\n{user_name}さん、")
    lines.append("")

    # 理由を表示
    for reason in risk_info["reasons"]:
        lines.append(f"❗ {reason}")

    lines.append("")
    lines.append("でも、大丈夫です。")
    lines.append("こういう時期は誰にでもあります。")
    lines.append("")
    lines.append("【🌟 今すぐできること】")
    lines.append("-" * 30)

    # 提案を表示
    for i, suggestion in enumerate(risk_info["suggestions"], 1):
        lines.append(f"\n{i}. {suggestion}")

    lines.append("")
    lines.append("-" * 30)
    lines.append("")

    if risk_info["risk_level"] == "high":
        lines.append("💪 ハードルを下げましょう！")
        lines.append("")
        lines.append("✅ 今日は「体重を測る」だけでOK")
        lines.append("✅ カロリー計算は明日から")
        lines.append("✅ とにかく「続ける」ことが最優先")
        lines.append("")
        lines.append("👉 続けることができれば、それだけで100点です！")
    else:
        lines.append("💪 小さな一歩から始めましょう！")
        lines.append("")
        lines.append("できることから、一つずつ。")
        lines.append("あなたなら大丈夫です。")

    lines.append("")
    lines.append("=" * 30)
    lines.append("継続は力なり。")
    lines.append("一緒に乗り越えましょう！")
    lines.append("=" * 30)
    lines.append("")
    lines.append("⚠️" * 10)

    return "\n".join(lines)
