#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
フィードバック生成サービス
関口さん風の励ましメッセージを生成
"""

import random


def generate_daily_feedback(user, today_record, yesterday_record=None, all_records=None):
    """
    日次フィードバックを生成

    Args:
        user: Userモデル
        today_record: 今日のDailyRecordモデル
        yesterday_record: 昨日のDailyRecordモデル（オプション）
        all_records: 全記録リスト（オプション）

    Returns:
        str: フィードバックメッセージ（LINE送信用）
    """
    lines = []
    lines.append("【関口メンターからのフィードバック】")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("")

    # 体重変化の分析
    if yesterday_record:
        weight_change = today_record.weight - yesterday_record.weight
        weight_to_goal = today_record.weight - user.target_weight

        lines.append(f"📊 体重変化: ", )
        if weight_change < 0:
            lines.append(f"{abs(weight_change):.1f}kg減 👍")
            lines.append(f"素晴らしい！目標まであと{abs(weight_to_goal):.1f}kgです。")
        elif weight_change > 0:
            lines.append(f"{weight_change:.1f}kg増")
            lines.append(f"焦らなくて大丈夫！体重は日々変動します。")
        else:
            lines.append(f"変化なし")
            lines.append(f"体重は日々変動するものです。継続が大切ですよ！")
        lines.append("")

    # 栄養バランスの分析（食事記録がある場合）
    if today_record.calories:
        lines.append("📊 栄養バランス:")
        
        # カロリー
        calorie_diff = today_record.calories - user.target_calories
        calorie_diff_percent = (calorie_diff / user.target_calories) * 100

        lines.append(f"  カロリー: {today_record.calories:.0f}kcal / 目標 {user.target_calories:.0f}kcal")
        
        if abs(calorie_diff_percent) <= 10:
            lines.append(f"  → 目標ピッタリです！素晴らしい👍")
        elif calorie_diff_percent > 10:
            lines.append(f"  → 目標より{abs(calorie_diff):.0f}kcal多めですが、大丈夫！明日調整しましょう")
        else:
            lines.append(f"  → 目標より{abs(calorie_diff):.0f}kcal少なめ。無理しすぎないでくださいね")

        lines.append("")

        # PFC
        if today_record.protein and today_record.fat and today_record.carbs:
            lines.append(f"  タンパク質: {today_record.protein:.1f}g / 目標 {user.target_protein:.1f}g")
            lines.append(f"  脂質: {today_record.fat:.1f}g / 目標 {user.target_fat:.1f}g")
            lines.append(f"  炭水化物: {today_record.carbs:.1f}g / 目標 {user.target_carbs:.1f}g")
            lines.append("")

            # PFCバランスのパーセンテージ
            total_cal = (today_record.protein * 4) + (today_record.fat * 9) + (today_record.carbs * 4)
            if total_cal > 0:
                p_percent = int((today_record.protein * 4 / total_cal) * 100)
                f_percent = int((today_record.fat * 9 / total_cal) * 100)
                c_percent = int((today_record.carbs * 4 / total_cal) * 100)
                lines.append(f"  PFCバランス: P{p_percent}% F{f_percent}% C{c_percent}%")
                lines.append(f"  目標バランス: P30% F20% C50%")
                lines.append("")

    # 目的別カスタマイズメッセージ
    diet_mode_msg = "ライトモード" if user.diet_mode == "light" else "ハードモード"
    lines.append(f"🎯 {user.name}さんへ: {diet_mode_msg}で順調に進んでいますよ！")
    lines.append("")

    # 良かった点を生成
    good_points = _generate_good_points(user, today_record)
    lines.append("✨ 良かった点:")
    for point in good_points:
        lines.append(f"  • {point}")
    lines.append("")

    # 改善ポイント（1つだけ）
    improvement_tip = _generate_improvement_tip(user, today_record)
    lines.append("💡 改善ポイント（1つだけ！）:")
    lines.append(f"  • {improvement_tip}")
    lines.append("")

    # 明日への一言
    tomorrow_message = _generate_tomorrow_message()
    lines.append("🔥 明日への一言:")
    lines.append(f"  {tomorrow_message}")
    lines.append("")
    lines.append("=" * 30)

    return "\n".join(lines)


def _generate_good_points(user, record):
    """良かった点を生成（2-3個）"""
    good_points = []

    # 基本的な良かった点
    basic_compliments = [
        f"{user.name}さん、今日も記録をつけてくれてありがとう！これが継続の第一歩です",
        f"{user.name}さん、このメッセージを読んでくれただけでも前向きな気持ちの表れです",
        f"毎日体重を測って記録する習慣、これがとても大切です！",
        f"体重と向き合う勇気、それが変化への第一歩ですよ",
    ]
    good_points.append(random.choice(basic_compliments))

    # 運動について
    if record.exercise and record.exercise.lower() not in ["なし", "なし。", "特になし", ""]:
        exercise_compliments = [
            f"「{record.exercise}」をやったこと、素晴らしいです！",
            f"今日も運動できたんですね。その積み重ねが結果につながります",
            f"「{record.exercise}」、よく頑張りましたね！",
        ]
        good_points.append(random.choice(exercise_compliments))

    # 食事記録について
    if record.calories:
        meal_compliments = [
            f"食事の内容を意識していること、それだけで大きな一歩です",
            f"しっかり記録していますね。この習慣が結果を生みます",
            f"食事を記録する習慣、これがとても大切です！",
        ]
        good_points.append(random.choice(meal_compliments))

    # タンパク質について
    if record.protein and record.protein >= user.target_protein * 0.9:
        protein_compliments = [
            f"タンパク質をしっかり摂取されていますね！筋肉が維持されますよ",
            f"タンパク質の意識、素晴らしいです！これが代謝維持につながります",
        ]
        good_points.append(random.choice(protein_compliments))

    # ランダムに2-3個選んで返す
    return random.sample(good_points, min(3, len(good_points)))


def _generate_improvement_tip(user, record):
    """改善ポイントを生成（1つだけ、優しく）"""
    improvement_tips = [
        "有酸素運動、5分でも10分でもいいので取り入れてみましょう。完璧じゃなくていいんです。",
        "タンパク質を意識して摂ると、筋肉が維持されやすくなります。目安は守れなくても大丈夫。",
        "水分補給も大切です。1日2リットルが理想ですが、できる範囲で増やしてみましょう。",
        "睡眠時間も体づくりには重要です。7時間が理想ですが、6時間でも続けることが大事。",
        "炭水化物を完全に抜くより、量を調整する方が続けやすいですよ。現場ではその方が結果が出ます。",
        "食事の回数を分けると代謝が安定しやすい、と言われていますが、自分に合うやり方でOKです。",
        "ストレッチも忘れずに。完璧にやらなくても、少しやるだけで違います。",
        "数字を気にしすぎないで。体の反応を見ながら調整していきましょう。",
        "80点を目指しましょう。100点を狙うより、80点で続ける方が結果が出ます。",
    ]

    # 特定の状況に応じた改善ポイント
    if record.exercise and "有酸素" not in record.exercise and "ジョギング" not in record.exercise:
        return "有酸素運動を20分以上続けると脂肪燃焼効果が高まります。でも、まずは5分からでOKです！"
    
    if record.protein and user.target_protein and record.protein < user.target_protein * 0.7:
        return "タンパク質がもう少し欲しいところです。プロテイン、サラダチキン、卵など手軽なものでOKです。"

    return random.choice(improvement_tips)


def _generate_tomorrow_message():
    """明日への一言を生成"""
    tomorrow_messages = [
        "継続は力なり！明日も一緒に頑張りましょう！",
        "小さな積み重ねが、大きな変化を生みます。明日も楽しみにしています！",
        "あなたのペースで大丈夫。焦らず、着実に進みましょう！",
        "今日も1日お疲れさまでした。明日もあなたらしく頑張りましょう！",
        "完璧じゃなくていい。続けることが何より大切です！",
        "変化は必ず訪れます。信じて続けましょう！",
        "明日も、できることから始めましょう。応援しています！",
    ]
    return random.choice(tomorrow_messages)


def generate_weekly_report(user, week_records, week_number):
    """
    週次レポートを生成

    Args:
        user: Userモデル
        week_records: 1週間分のDailyRecordリスト
        week_number: 第何週目か

    Returns:
        str: 週次レポートメッセージ
    """
    lines = []
    lines.append("【📊 週次レポート 📊】")
    lines.append("=" * 30)
    lines.append(f"\n{user.name}さん、{week_number}週目お疲れさまでした！")
    lines.append("")

    if not week_records:
        lines.append("記録がありません。来週は一緒に頑張りましょう！")
        return "\n".join(lines)

    # 体重変化
    start_weight = week_records[0].weight
    end_weight = week_records[-1].weight
    weight_change = start_weight - end_weight

    lines.append("📈 体重の変化:")
    lines.append(f"  開始: {start_weight:.1f}kg")
    lines.append(f"  終了: {end_weight:.1f}kg")
    lines.append(f"  変化: {abs(weight_change):.1f}kg {'減' if weight_change > 0 else '増'}")
    lines.append("")

    # 週間の目標との比較
    weekly_target = (user.current_weight * user.reduction_rate) / 4  # 月間目標の1/4
    if weight_change >= weekly_target * 0.8:
        lines.append("🎉 目標ペースで順調に進んでいます！")
    elif weight_change > 0:
        lines.append("👍 少しずつ減っています。このペースで続けましょう！")
    else:
        lines.append("💪 体重が減っていませんが、焦らなくて大丈夫！")
        lines.append("   停滞期は誰にでもあります。継続が大切です。")
    lines.append("")

    # カロリー平均（記録がある場合）
    calorie_records = [r for r in week_records if r.calories]
    if calorie_records:
        avg_calories = sum(r.calories for r in calorie_records) / len(calorie_records)
        lines.append(f"🍚 平均カロリー: {avg_calories:.0f}kcal")
        lines.append(f"   目標: {user.target_calories:.0f}kcal")
        
        if abs(avg_calories - user.target_calories) <= user.target_calories * 0.1:
            lines.append("   → 目標通り！素晴らしいです👍")
        lines.append("")

    # 記録日数
    record_days = len(week_records)
    lines.append(f"📝 記録日数: {record_days}/7日")
    if record_days == 7:
        lines.append("   → 完璧です！この調子で続けましょう🎉")
    elif record_days >= 5:
        lines.append("   → よく頑張りました！継続力が素晴らしいです👍")
    else:
        lines.append("   → 来週は記録を増やせるといいですね。できる範囲で大丈夫！")
    lines.append("")

    # 来週への励まし
    lines.append("🔥 来週も一緒に頑張りましょう！")
    lines.append("=" * 30)

    return "\n".join(lines)


def generate_monthly_report(user, month_records, month_number):
    """
    月次レポートを生成

    Args:
        user: Userモデル
        month_records: 1ヶ月分のDailyRecordリスト
        month_number: 第何ヶ月目か

    Returns:
        str: 月次レポートメッセージ
    """
    lines = []
    lines.append("【🎊 月次レポート 🎊】")
    lines.append("=" * 30)
    lines.append(f"\n{user.name}さん、{month_number}ヶ月目お疲れさまでした！")
    lines.append("")

    if not month_records:
        lines.append("記録がありません。来月は一緒に頑張りましょう！")
        return "\n".join(lines)

    # 体重変化
    start_weight = month_records[0].weight
    end_weight = month_records[-1].weight
    weight_change = start_weight - end_weight

    lines.append("📈 1ヶ月の変化:")
    lines.append(f"  開始: {start_weight:.1f}kg")
    lines.append(f"  終了: {end_weight:.1f}kg")
    lines.append(f"  変化: {abs(weight_change):.1f}kg {'減' if weight_change > 0 else '増'}")
    
    # 変化率
    change_rate = (weight_change / start_weight) * 100
    lines.append(f"  変化率: {abs(change_rate):.1f}%")
    lines.append("")

    # 目標との比較
    monthly_target = user.current_weight * user.reduction_rate
    if weight_change >= monthly_target * 0.8:
        lines.append("🎉🎉🎉 目標達成！素晴らしいです！")
        lines.append("   このペースで継続すれば、必ず目標体重に到達できます！")
    elif weight_change > 0:
        lines.append("👍 順調に減量できています！")
        lines.append("   無理せず、このペースで続けましょう。")
    else:
        lines.append("💪 まだ結果が出ていませんが、諦めないでください！")
        lines.append("   継続こそが最大の武器です。")
    lines.append("")

    # 記録日数
    record_days = len(month_records)
    lines.append(f"📝 記録日数: {record_days}/30日")
    continuity_rate = (record_days / 30) * 100
    lines.append(f"   継続率: {continuity_rate:.0f}%")
    
    if continuity_rate >= 90:
        lines.append("   → 圧倒的な継続力！この習慣が結果を生みます🎉")
    elif continuity_rate >= 70:
        lines.append("   → 素晴らしい継続力です👍")
    else:
        lines.append("   → 来月は記録を増やせるといいですね。応援しています！")
    lines.append("")

    # 平均カロリー（記録がある場合）
    calorie_records = [r for r in month_records if r.calories]
    if calorie_records:
        avg_calories = sum(r.calories for r in calorie_records) / len(calorie_records)
        lines.append(f"🍚 平均カロリー: {avg_calories:.0f}kcal")
        lines.append(f"   目標: {user.target_calories:.0f}kcal")
        lines.append("")

    # 関口からの特別メッセージ
    lines.append("💬 関口からの特別メッセージ:")
    lines.append("")
    
    if weight_change > 0:
        lines.append(f"  {user.name}さん、1ヶ月間本当にお疲れさまでした！")
        lines.append(f"  {abs(weight_change):.1f}kg減、素晴らしい結果です。")
        lines.append("")
        lines.append("  でも、ここからが本番です。")
        lines.append("  体重を落とすことより、キープする方が難しいんです。")
        lines.append("")
        lines.append("  無理をせず、今のペースで続けてください。")
        lines.append("  あなたなら必ずできます。")
    else:
        lines.append(f"  {user.name}さん、1ヶ月間継続できたこと、")
        lines.append("  それだけで本当に素晴らしいです。")
        lines.append("")
        lines.append("  体重は後からついてきます。")
        lines.append("  今は習慣を作る時期だと思ってください。")
        lines.append("")
        lines.append("  諦めずに続ければ、必ず変化は訪れます。")
        lines.append("  私が保証します。")
    
    lines.append("")
    lines.append("  継続は力なり。")
    lines.append("  来月も一緒に頑張りましょう！")
    lines.append("")
    lines.append("=" * 30)

    return "\n".join(lines)
