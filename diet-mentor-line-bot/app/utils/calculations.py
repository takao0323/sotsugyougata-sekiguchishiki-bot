#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
カロリーとPFCの計算ロジック
"""


def calculate_bmr(gender, weight, height, age):
    """
    ハリス・ベネディクト方式（改良版）で基礎代謝量（BMR）を計算

    Args:
        gender (str): 性別（"男性" または "女性"）
        weight (float): 体重（kg）
        height (float): 身長（cm）
        age (int): 年齢

    Returns:
        float: 基礎代謝量（kcal/日）
    """
    if gender == "男性":
        # 男性: (13.397×体重kg)+(4.799×身長cm)-(5.677×年齢)+88.362
        bmr = (13.397 * weight) + (4.799 * height) - (5.677 * age) + 88.362
    else:  # 女性
        # 女性: (9.247×体重kg)+(3.098×身長cm)-(4.330×年齢)+447.593
        bmr = (9.247 * weight) + (3.098 * height) - (4.330 * age) + 447.593

    return bmr


def calculate_tdee(bmr, activity_coefficient=1.4):
    """
    総消費カロリー（TDEE）を計算

    Args:
        bmr (float): 基礎代謝量（kcal/日）
        activity_coefficient (float): 活動レベル係数（デフォルト: 1.4 軽い運動）

    Returns:
        float: 総消費カロリー（kcal/日）
    """
    return bmr * activity_coefficient


def calculate_target_calories(tdee, reduction_rate):
    """
    目標カロリーを計算

    Args:
        tdee (float): 総消費カロリー（kcal/日）
        reduction_rate (float): 減量ペース（0.02 or 0.04）

    Returns:
        float: 目標カロリー（kcal/日）
    """
    # 月の減量ペースを1日あたりに換算
    # 例: 月2% → 1日あたり約0.0007%の減量
    # 7200kcal = 体重1kg相当のカロリー赤字
    # 目標カロリー = TDEE - (TDEEの一定割合)
    
    # シンプルに、TDEEから一定のカロリーを引く
    # 月2%の場合: TDEEの約15%減
    # 月4%の場合: TDEEの約25%減
    
    if reduction_rate == 0.02:  # ライトモード
        calorie_reduction_rate = 0.15
    else:  # ハードモード (0.04)
        calorie_reduction_rate = 0.25
    
    target_calories = tdee * (1 - calorie_reduction_rate)
    return round(target_calories, 2)


def calculate_pfc_targets(target_calories, protein_ratio=0.30, fat_ratio=0.20, carb_ratio=0.50):
    """
    目標PFC（タンパク質・脂質・炭水化物）を計算

    Args:
        target_calories (float): 目標カロリー（kcal/日）
        protein_ratio (float): タンパク質の割合（デフォルト: 0.30）
        fat_ratio (float): 脂質の割合（デフォルト: 0.20）
        carb_ratio (float): 炭水化物の割合（デフォルト: 0.50）

    Returns:
        dict: {protein, fat, carbs} グラム数
    """
    # タンパク質: 4kcal/g
    # 脂質: 9kcal/g
    # 炭水化物: 4kcal/g

    protein_grams = (target_calories * protein_ratio) / 4
    fat_grams = (target_calories * fat_ratio) / 9
    carbs_grams = (target_calories * carb_ratio) / 4

    return {
        'protein': round(protein_grams, 1),
        'fat': round(fat_grams, 1),
        'carbs': round(carbs_grams, 1)
    }


def calculate_monthly_target_loss(current_weight, reduction_rate):
    """
    月間の目標減量量を計算

    Args:
        current_weight (float): 現在の体重（kg）
        reduction_rate (float): 減量ペース（0.02 or 0.04）

    Returns:
        float: 月間目標減量量（kg）
    """
    return round(current_weight * reduction_rate, 1)


def calculate_pfc_percentage(protein_grams, fat_grams, carbs_grams):
    """
    実際のPFCバランスをパーセンテージで計算

    Args:
        protein_grams (float): タンパク質（g）
        fat_grams (float): 脂質（g）
        carbs_grams (float): 炭水化物（g）

    Returns:
        dict: {protein_percent, fat_percent, carb_percent}
    """
    total_calories = (protein_grams * 4) + (fat_grams * 9) + (carbs_grams * 4)

    if total_calories == 0:
        return {'protein_percent': 0, 'fat_percent': 0, 'carb_percent': 0}

    protein_percent = (protein_grams * 4 / total_calories) * 100
    fat_percent = (fat_grams * 9 / total_calories) * 100
    carb_percent = (carbs_grams * 4 / total_calories) * 100

    return {
        'protein_percent': round(protein_percent),
        'fat_percent': round(fat_percent),
        'carb_percent': round(carb_percent)
    }


def validate_reduction_rate(current_weight, target_weight, reduction_rate, max_rate=0.04):
    """
    減量ペースが無茶でないかチェック

    Args:
        current_weight (float): 現在の体重（kg）
        target_weight (float): 目標体重（kg）
        reduction_rate (float): 減量ペース
        max_rate (float): 最大許容減量ペース（デフォルト: 0.04 = 4%）

    Returns:
        dict: {valid: bool, message: str}
    """
    if reduction_rate > max_rate:
        return {
            'valid': False,
            'message': f'⚠️ それは無茶ですよ！\n\n月に体重の{int(max_rate*100)}%以上減らすと、体がホメオスタシス（恒常性）で\n「飢餓状態だ！」と判断して、代謝を下げてしまうんです。'
        }

    if current_weight < target_weight:
        return {
            'valid': False,
            'message': '⚠️ 目標体重が現在の体重より高くなっています。増量モードは現在未対応です。'
        }

    return {'valid': True, 'message': ''}
