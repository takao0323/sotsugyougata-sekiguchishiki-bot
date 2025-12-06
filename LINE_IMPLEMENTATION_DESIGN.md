# LINE公式アカウント実装設計書

**コンセプト**: シンプルで使いやすい、挫折させないダイエットメンター

---

## 📋 実装優先順位（3フェーズ）

### 🎯 Phase 1: MVP（最小限の価値提供） - 2週間

**目標**: 基本的な記録→フィードバックサイクルを動かす

#### 実装する機能
1. ✅ **初回プロフィール登録**（LIFF）
   - 名前、性別、年齢、身長、現在体重、目標体重
   - ライト/ハードモード選択
   - 関口からの提案メッセージ表示

2. ✅ **毎日の記録入力**（LIFF）
   - 体重のみ（最小限）
   - カレンダーから日付選択可能

3. ✅ **関口からのフィードバック**（チャット）
   - 体重変化の分析
   - 励ましメッセージ（4900パターン）
   - 挫折予測AI（リスク検知のみ）

4. ✅ **体重グラフ表示**（LIFF）
   - シンプルな折れ線グラフ
   - 目標ラインとの比較

5. ✅ **リッチメニュー**（6ボタン）
   - 今日の記録、グラフ確認、設定のみ

#### 実装しない機能（Phase 2以降）
- ❌ 食事撮影機能
- ❌ カロリー・PFC入力
- ❌ 運動記録
- ❌ メニュー提案
- ❌ 週次・月次レポート

#### 技術スタック（Phase 1）
- **Backend**: Flask（シンプル）
- **Database**: SQLite（開発用）→ PostgreSQL（本番）
- **Hosting**: Heroku or Railway（無料枠）
- **LINE**: Messaging API + LIFF v2

---

### 🚀 Phase 2: 機能強化 - 3週間

**目標**: 食事管理機能を追加して、本格的なダイエットサポート

#### 追加機能
1. ✅ **食事記録（LIFF）**
   - カロリー・PFC手動入力
   - 食事撮影→Gemini API解析（オプション）
   - 1日3食分の記録

2. ✅ **栄養バランスフィードバック**
   - 目標カロリー・PFCとの比較
   - 栄養バランスグラフ

3. ✅ **メニュー提案機能**
   - コンビニ飯10パターン
   - 自炊10パターン
   - ユーザーの目標に合わせて表示

4. ✅ **週次レポート**
   - 7日ごとに自動生成
   - 体重推移、栄養バランスの振り返り

5. ✅ **挫折予測AI強化**
   - 自動的にバー下げ提案
   - リスク別の個別サポート

6. ✅ **リッチメニュー拡張**
   - 食事を撮影、メニュー提案ボタン追加

---

### 🌟 Phase 3: 差別化機能 - 4週間

**目標**: 他のダイエットアプリにない独自機能

#### 追加機能
1. ✅ **月次レポート**
   - 30日ごとの詳細分析
   - 関口からの特別メッセージ

2. ✅ **プッシュ通知最適化**
   - 記録忘れリマインダー（個別時間設定）
   - 挫折予測時の緊急メッセージ

3. ✅ **プロフィール更新機能**
   - 目標体重変更
   - モード切り替え（ライト↔ハード）

4. ✅ **データエクスポート**
   - CSV形式でダウンロード
   - グラフ画像保存

5. ✅ **パフォーマンス最適化**
   - データベースインデックス
   - キャッシュ実装

---

## 🎨 LIFF画面詳細設計

### 1️⃣ 初回プロフィール登録（LIFF Full）

#### URL
`https://liff.line.me/{liff-id}/profile`

#### 画面構成
```
┌─────────────────────────┐
│   ダイエットメンター    │
│  ～関口式トレーニング～  │
├─────────────────────────┤
│                         │
│ 【基本情報】            │
│ お名前: [__________]    │
│                         │
│ 性別:  ⚪男性 ⚪女性     │
│                         │
│ 年齢: [__] 歳          │
│                         │
│ 身長: [___] cm         │
│                         │
│ 【現在の状況】          │
│ 現在の体重: [__] kg    │
│                         │
│ 目標体重: [__] kg      │
│                         │
│ 【減量ペース】          │
│ ⚪ライトモード（月2%）  │
│ ⚪ハードモード（月4%）  │
│                         │
│ ┌─────────────────┐    │
│ │   登録する        │    │
│ └─────────────────┘    │
└─────────────────────────┘
```

#### バリデーション
- 名前: 必須、1-20文字
- 年齢: 必須、18-100歳
- 身長: 必須、100-250cm
- 現在体重: 必須、30-200kg
- 目標体重: 必須、30-200kg、現在体重との差異チェック
- 減量ペース: 必須、ラジオボタン

#### 登録後の流れ
1. バックエンドでプロフィール保存
2. BMR・TDEE・目標カロリー自動計算
3. **関口からの提案メッセージ**をLINEチャットに送信
   ```
   【関口からの提案】

   太郎さん、ライトモードを選択されましたね。
   現在の体重70kgから、無理なく健康的に減量するなら...

   💡 月に1.4kgずつ
      落としていくペースがおすすめです！

   一緒に頑張りましょう！
   ```
4. プロフィール確認メッセージ（目標カロリー・PFC表示）
5. メニュー提案（Phase 2）
6. リッチメニュー表示

---

### 2️⃣ 今日の記録入力（LIFF Tall）

#### URL
`https://liff.line.me/{liff-id}/record`

#### Phase 1: 体重のみ
```
┌─────────────────────────┐
│   今日の記録            │
├─────────────────────────┤
│                         │
│ 📅 日付: 2025年12月4日  │
│                         │
│ ⚖️ 体重                 │
│ [___._] kg              │
│                         │
│                         │
│                         │
│                         │
│                         │
│                         │
│ ┌─────────────────┐    │
│ │   記録する        │    │
│ └─────────────────┘    │
│                         │
│ ┌─────────────────┐    │
│ │   キャンセル      │    │
│ └─────────────────┘    │
└─────────────────────────┘
```

#### Phase 2: 食事記録追加
```
┌─────────────────────────┐
│   今日の記録            │
├─────────────────────────┤
│                         │
│ 📅 日付: 2025年12月4日  │
│                         │
│ ⚖️ 体重                 │
│ [___._] kg              │
│                         │
│ 🍚 食事記録（任意）     │
│                         │
│ ┌─────────────────┐    │
│ │ 📸 写真から記録   │    │
│ └─────────────────┘    │
│                         │
│ または手動入力:          │
│                         │
│ カロリー: [____] kcal   │
│ タンパク質: [__] g      │
│ 脂質: [__] g            │
│ 炭水化物: [__] g        │
│                         │
│ 💪 運動（任意）         │
│ [________________]      │
│                         │
│ ┌─────────────────┐    │
│ │   記録する        │    │
│ └─────────────────┘    │
└─────────────────────────┘
```

#### バリデーション
- 体重: 必須、30-200kg、小数点1桁まで
- カロリー: 任意、0-10000kcal（Phase 2）
- タンパク質: 任意、0-500g（Phase 2）
- 脂質: 任意、0-500g（Phase 2）
- 炭水化物: 任意、0-1000g（Phase 2）

#### 記録後の流れ
1. バックエンドでデータ保存
2. 挫折予測AI実行（day 2以降）
3. **関口からのフィードバック**をLINEチャットに送信
   ```
   【関口メンターからのフィードバック】
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   📊 体重変化: -0.3kg
   順調ですね！この調子で続けていきましょう。

   ✨ 良かった点:
     • 太郎さん、今日も記録してくれてありがとう！
     • 毎日体重を測って記録する習慣、これがとても大切です！

   🔥 明日への一言:
     継続は力なり！明日も一緒に頑張りましょう！
   ```
4. グラフ更新
5. LIFF閉じる→チャット画面に戻る

---

### 3️⃣ グラフ確認（LIFF Tall）

#### URL
`https://liff.line.me/{liff-id}/graph`

#### Phase 1: 体重グラフのみ
```
┌─────────────────────────┐
│   体重の推移            │
├─────────────────────────┤
│                         │
│ 📊 体重グラフ           │
│                         │
│  kg                     │
│  72 ┐                   │
│  71 │     ●             │
│  70 │   ●   ●           │
│  69 │ ●       ● 目標    │
│  68 │ - - - - - - - -   │
│  67 └───────────────    │
│     1  3  5  7  9 (日)  │
│                         │
│ 📈 進捗状況             │
│ 開始: 72.0kg            │
│ 現在: 70.5kg            │
│ 目標: 68.0kg            │
│ 達成率: 38%             │
│                         │
│ 期間: [7日▼][30日][全期間]│
│                         │
│ ┌─────────────────┐    │
│ │   閉じる          │    │
│ └─────────────────┘    │
└─────────────────────────┘
```

#### Phase 2: 栄養グラフ追加
```
┌─────────────────────────┐
│   データ確認            │
├─────────────────────────┤
│                         │
│ タブ: [体重][栄養]      │
│                         │
│ 📊 栄養バランス         │
│                         │
│ カロリー                │
│ ■■■■■■□□□□ 1520/1800│
│                         │
│ タンパク質              │
│ ■■■■■■■■□□ 115/120 │
│                         │
│ 脂質                    │
│ ■■■■■□□□□□ 35/40   │
│                         │
│ 炭水化物                │
│ ■■■■■■■■■□ 185/200│
│                         │
│ PFCバランス             │
│ P: 30% ■■■■■■■■■■  │
│ F: 21% ■■■■■           │
│ C: 49% ■■■■■■■■■    │
│                         │
│ 期間: [今日][7日][30日] │
│                         │
│ ┌─────────────────┐    │
│ │   閉じる          │    │
│ └─────────────────┘    │
└─────────────────────────┘
```

#### 機能
- 期間切り替え（7日/30日/全期間）
- グラフのタップでデータ詳細表示
- 画像保存ボタン（Phase 3）

---

### 4️⃣ 設定画面（LIFF Full）

#### URL
`https://liff.line.me/{liff-id}/settings`

#### 画面構成
```
┌─────────────────────────┐
│   設定                  │
├─────────────────────────┤
│                         │
│ 【プロフィール】        │
│ 名前: 太郎              │
│ 年齢: 35歳              │
│ 身長: 170cm             │
│                         │
│ ┌─────────────────┐    │
│ │   編集            │    │
│ └─────────────────┘    │
│                         │
│ 【目標設定】            │
│ 現在: 70.5kg            │
│ 目標: 68.0kg            │
│ モード: ライト（月2%）  │
│                         │
│ ┌─────────────────┐    │
│ │   目標変更        │    │
│ └─────────────────┘    │
│                         │
│ 【通知設定】            │
│ 記録リマインダー        │
│ 毎日 21:00 [変更]       │
│                         │
│ ┌─────────────────┐    │
│ │   データ削除      │    │
│ └─────────────────┘    │
│                         │
└─────────────────────────┘
```

---

## 🎛️ リッチメニュー設計

### Phase 1: シンプル版（3ボタン）
```
┌────────────┬────────────┐
│            │            │
│  📝 今日の  │  📊 グラフ  │
│    記録    │    確認    │
│            │            │
├────────────┴────────────┤
│                         │
│     ⚙️ 設定              │
│                         │
└─────────────────────────┘
```

### Phase 2: フル機能版（6ボタン）
```
┌────────────┬────────────┐
│            │            │
│  📝 今日の  │  📸 食事を  │
│    記録    │    撮影    │
│            │            │
├────────────┼────────────┤
│            │            │
│  📊 グラフ  │  💬 関口の  │
│    確認    │  アドバイス │
│            │            │
├────────────┼────────────┤
│            │            │
│  🍽️ メニュー│  ⚙️ 設定   │
│    提案    │            │
│            │            │
└────────────┴────────────┘
```

---

## 🗄️ データベース設計（PostgreSQL）

### テーブル構造

#### 1. users（ユーザー情報）
```sql
CREATE TABLE users (
    user_id VARCHAR(50) PRIMARY KEY,  -- LINE User ID
    name VARCHAR(50) NOT NULL,
    gender VARCHAR(10) NOT NULL,      -- '男性' or '女性'
    age INTEGER NOT NULL,
    height DECIMAL(5,1) NOT NULL,
    current_weight DECIMAL(5,1) NOT NULL,
    target_weight DECIMAL(5,1) NOT NULL,
    diet_mode VARCHAR(10) NOT NULL,   -- 'light' or 'hard'
    reduction_rate DECIMAL(3,2) NOT NULL,  -- 0.02 or 0.04
    bmr DECIMAL(7,2),                 -- 基礎代謝
    tdee DECIMAL(7,2),                -- 1日の消費カロリー
    target_calories DECIMAL(7,2),     -- 目標カロリー
    target_protein DECIMAL(5,1),      -- 目標タンパク質
    target_fat DECIMAL(5,1),          -- 目標脂質
    target_carbs DECIMAL(5,1),        -- 目標炭水化物
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 2. daily_records（日次記録）
```sql
CREATE TABLE daily_records (
    record_id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) REFERENCES users(user_id),
    record_date DATE NOT NULL,
    day_count INTEGER NOT NULL,       -- 1日目、2日目...
    weight DECIMAL(5,1) NOT NULL,
    calories DECIMAL(7,2),            -- Phase 2
    protein DECIMAL(5,1),             -- Phase 2
    fat DECIMAL(5,1),                 -- Phase 2
    carbs DECIMAL(5,1),               -- Phase 2
    exercise TEXT,                    -- Phase 2
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, record_date)
);

CREATE INDEX idx_daily_records_user_date ON daily_records(user_id, record_date);
```

#### 3. feedback_history（フィードバック履歴）
```sql
CREATE TABLE feedback_history (
    feedback_id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) REFERENCES users(user_id),
    record_date DATE NOT NULL,
    feedback_type VARCHAR(20) NOT NULL,  -- 'daily', 'weekly', 'monthly'
    feedback_content TEXT NOT NULL,
    dropout_risk_level VARCHAR(10),      -- 'low', 'medium', 'high'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_feedback_user_date ON feedback_history(user_id, record_date);
```

#### 4. meal_photos（食事写真）- Phase 2
```sql
CREATE TABLE meal_photos (
    photo_id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) REFERENCES users(user_id),
    record_date DATE NOT NULL,
    meal_type VARCHAR(10),            -- 'breakfast', 'lunch', 'dinner', 'snack'
    photo_url TEXT NOT NULL,
    analyzed_calories DECIMAL(7,2),
    analyzed_protein DECIMAL(5,1),
    analyzed_fat DECIMAL(5,1),
    analyzed_carbs DECIMAL(5,1),
    gemini_response TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔌 API エンドポイント設計

### Base URL
`https://your-domain.com/api/v1`

### 認証
すべてのリクエストヘッダーに以下を含む：
```
Authorization: Bearer {LINE_ACCESS_TOKEN}
```

### エンドポイント一覧

#### 1. プロフィール関連

##### POST /profile
**初回プロフィール登録**

Request:
```json
{
  "user_id": "U1234567890abcdef",
  "name": "太郎",
  "gender": "男性",
  "age": 35,
  "height": 170,
  "current_weight": 72,
  "target_weight": 68,
  "diet_mode": "light"
}
```

Response:
```json
{
  "status": "success",
  "data": {
    "user_id": "U1234567890abcdef",
    "name": "太郎",
    "bmr": 1650.5,
    "tdee": 2310.7,
    "target_calories": 1800,
    "target_protein": 120,
    "target_fat": 40,
    "target_carbs": 200,
    "monthly_target_loss": 1.4,
    "proposal_message": "太郎さん、ライトモードを選択されましたね。\n現在の体重70kgから、無理なく健康的に減量するなら...\n\n💡 月に1.4kgずつ\n   落としていくペースがおすすめです！"
  }
}
```

##### GET /profile/{user_id}
**プロフィール取得**

Response:
```json
{
  "status": "success",
  "data": {
    "user_id": "U1234567890abcdef",
    "name": "太郎",
    "gender": "男性",
    "age": 35,
    "height": 170,
    "current_weight": 70.5,
    "target_weight": 68,
    "diet_mode": "light",
    "target_calories": 1800,
    "target_protein": 120,
    "target_fat": 40,
    "target_carbs": 200
  }
}
```

##### PUT /profile/{user_id}
**プロフィール更新（Phase 3）**

---

#### 2. 日次記録関連

##### POST /records
**日次記録登録**

Request (Phase 1):
```json
{
  "user_id": "U1234567890abcdef",
  "record_date": "2025-12-04",
  "weight": 70.5
}
```

Request (Phase 2):
```json
{
  "user_id": "U1234567890abcdef",
  "record_date": "2025-12-04",
  "weight": 70.5,
  "calories": 1520,
  "protein": 115,
  "fat": 35,
  "carbs": 185,
  "exercise": "30分ジョギング"
}
```

Response:
```json
{
  "status": "success",
  "data": {
    "record_id": 123,
    "day_count": 5,
    "feedback": {
      "weight_change": -0.3,
      "weight_status": "順調ですね！この調子で続けていきましょう。",
      "dropout_risk": {
        "level": "low",
        "reasons": [],
        "suggestions": []
      },
      "encouragement": "✨ 良かった点:\n  • 太郎さん、今日も記録してくれてありがとう！",
      "tomorrow_message": "継続は力なり！明日も一緒に頑張りましょう！"
    }
  }
}
```

##### GET /records/{user_id}
**日次記録取得（期間指定）**

Query Parameters:
- `start_date`: YYYY-MM-DD（省略時: 全期間）
- `end_date`: YYYY-MM-DD（省略時: 今日）

Response:
```json
{
  "status": "success",
  "data": [
    {
      "record_date": "2025-12-04",
      "day_count": 5,
      "weight": 70.5,
      "calories": 1520,
      "protein": 115,
      "fat": 35,
      "carbs": 185
    },
    {
      "record_date": "2025-12-03",
      "day_count": 4,
      "weight": 70.8,
      "calories": 1600,
      "protein": 120,
      "fat": 38,
      "carbs": 190
    }
  ]
}
```

---

#### 3. グラフ・統計関連

##### GET /graph/weight/{user_id}
**体重グラフデータ取得**

Query Parameters:
- `period`: `7` (7日間) / `30` (30日間) / `all` (全期間)

Response:
```json
{
  "status": "success",
  "data": {
    "labels": ["12/1", "12/2", "12/3", "12/4"],
    "weights": [72.0, 71.5, 71.2, 70.5],
    "target_line": [68.0, 68.0, 68.0, 68.0],
    "statistics": {
      "start_weight": 72.0,
      "current_weight": 70.5,
      "target_weight": 68.0,
      "total_loss": -1.5,
      "progress_rate": 38,
      "average_daily_loss": -0.38
    }
  }
}
```

##### GET /graph/nutrition/{user_id}
**栄養バランスグラフデータ（Phase 2）**

---

#### 4. 食事写真解析（Phase 2）

##### POST /analyze-meal
**食事写真をGemini APIで解析**

Request:
```json
{
  "user_id": "U1234567890abcdef",
  "record_date": "2025-12-04",
  "meal_type": "lunch",
  "photo_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

Response:
```json
{
  "status": "success",
  "data": {
    "calories": 650,
    "protein": 35,
    "fat": 20,
    "carbs": 75,
    "meal_description": "鶏むね肉のグリル、玄米、サラダ",
    "photo_url": "https://storage.example.com/meals/123.jpg"
  }
}
```

---

#### 5. メニュー提案（Phase 2）

##### GET /menu/suggestions/{user_id}
**ユーザーに最適なメニュー提案**

Response:
```json
{
  "status": "success",
  "data": {
    "target_calories": 1800,
    "target_protein": 120,
    "target_fat": 40,
    "target_carbs": 200,
    "convenience_meals": [
      {
        "name": "サラダチキン＋おにぎり（梅）＋野菜サラダ",
        "calories": 420,
        "protein": 32,
        "fat": 6,
        "carbs": 58,
        "description": "定番の高タンパク・低脂質メニュー"
      }
    ],
    "homemade_meals": [
      {
        "name": "鶏むね肉のソテー＋玄米＋温野菜",
        "calories": 450,
        "protein": 38,
        "fat": 8,
        "carbs": 62,
        "description": "シンプルで栄養バランス抜群"
      }
    ]
  }
}
```

---

#### 6. レポート関連（Phase 2-3）

##### GET /reports/weekly/{user_id}/{week_number}
**週次レポート取得**

##### GET /reports/monthly/{user_id}/{month_number}
**月次レポート取得**

---

## 🛠️ 技術アーキテクチャ

### システム構成図
```
┌─────────────┐
│  LINE App   │
│  (ユーザー)  │
└──────┬──────┘
       │
       ├─────────────────┐
       │                 │
       ▼                 ▼
┌──────────────┐  ┌─────────────┐
│ LINE Message │  │   LIFF      │
│     API      │  │ (Web View)  │
└──────┬───────┘  └──────┬──────┘
       │                 │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │  Flask Backend  │
       │  (Python 3.11)  │
       ├─────────────────┤
       │ • main.py       │
       │ • api_routes.py │
       │ • db_models.py  │
       │ • ai_service.py │
       └────────┬────────┘
                │
       ┌────────┼────────┐
       │                 │
       ▼                 ▼
┌──────────────┐  ┌─────────────┐
│  PostgreSQL  │  │ Gemini API  │
│  (Database)  │  │ (Image AI)  │
└──────────────┘  └─────────────┘
```

### ディレクトリ構造
```
diet-mentor-line-bot/
├── app/
│   ├── __init__.py
│   ├── config.py                 # 設定（環境変数）
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py               # Userモデル
│   │   ├── daily_record.py       # DailyRecordモデル
│   │   └── feedback.py           # Feedbackモデル
│   ├── services/
│   │   ├── __init__.py
│   │   ├── profile_service.py    # プロフィール管理
│   │   ├── record_service.py     # 記録管理
│   │   ├── feedback_service.py   # フィードバック生成
│   │   ├── dropout_ai.py         # 挫折予測AI
│   │   ├── meal_service.py       # メニュー提案（Phase 2）
│   │   └── gemini_service.py     # Gemini API連携（Phase 2）
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── webhook.py            # LINE Webhook
│   │   ├── liff_api.py           # LIFF用API
│   │   └── admin.py              # 管理画面（Phase 3）
│   └── utils/
│       ├── __init__.py
│       ├── calculations.py       # BMR/TDEE計算
│       ├── validators.py         # バリデーション
│       └── formatters.py         # メッセージフォーマット
├── liff/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Profile.jsx       # プロフィール登録
│   │   │   ├── Record.jsx        # 日次記録
│   │   │   ├── Graph.jsx         # グラフ表示
│   │   │   └── Settings.jsx      # 設定
│   │   ├── components/
│   │   │   ├── WeightGraph.jsx   # 体重グラフコンポーネント
│   │   │   ├── NutritionChart.jsx# 栄養バランスチャート
│   │   │   └── InputForm.jsx     # 入力フォーム
│   │   ├── hooks/
│   │   │   └── useLiff.js        # LIFF SDK hooks
│   │   ├── services/
│   │   │   └── api.js            # API通信
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
├── database/
│   ├── migrations/               # マイグレーションファイル
│   │   ├── 001_create_users.sql
│   │   ├── 002_create_records.sql
│   │   └── 003_create_feedback.sql
│   └── seeds/                    # 初期データ
│       └── meal_examples.sql
├── tests/
│   ├── test_calculations.py
│   ├── test_dropout_ai.py
│   └── test_api.py
├── docs/
│   ├── API_SPEC.md
│   ├── DATABASE_DESIGN.md
│   └── DEPLOYMENT.md
├── .env.example
├── .gitignore
├── requirements.txt
├── Procfile                      # Heroku用
├── runtime.txt                   # Python version
└── README.md
```

---

## 🚀 デプロイ・運用

### Phase 1: 開発環境
- **ホスティング**: ローカル開発
- **データベース**: SQLite
- **LINE**: Messaging API（無料枠）
- **LIFF**: ngrok経由でテスト

### Phase 2: ステージング環境
- **ホスティング**: Railway or Render（無料枠）
- **データベース**: PostgreSQL（Supabase無料枠）
- **LINE**: Messaging API（有料プラン検討）
- **LIFF**: 本番URL

### Phase 3: 本番環境
- **ホスティング**: AWS EC2 or Google Cloud Run
- **データベース**: Amazon RDS or Cloud SQL
- **LINE**: Messaging API（有料プラン）
- **CDN**: CloudFront (画像配信)
- **監視**: Sentry (エラー監視)

---

## 📊 成功指標（KPI）

### Phase 1
- ✅ ユーザー登録数: 10名
- ✅ 3日間継続率: 70%以上
- ✅ 記録入力の平均時間: 30秒以内

### Phase 2
- ✅ ユーザー登録数: 50名
- ✅ 7日間継続率: 60%以上
- ✅ 挫折予測AIの的中率: 70%以上
- ✅ メニュー提案のクリック率: 30%以上

### Phase 3
- ✅ ユーザー登録数: 200名
- ✅ 30日間継続率: 50%以上
- ✅ 目標体重達成率: 40%以上
- ✅ 月額課金継続率: 80%以上

---

## 💡 シンプルさを保つためのルール

### ❌ やらないこと
1. **過度な機能追加**: Phase 1では体重記録のみ
2. **複雑なUI**: ボタンは1画面に3つまで
3. **長い入力フォーム**: 必須項目は最小限
4. **複雑なグラフ**: 折れ線グラフと棒グラフのみ
5. **ユーザー設定の多様化**: デフォルト値を賢く設定

### ✅ やること
1. **段階的リリース**: Phase 1→2→3で段階的に機能追加
2. **デフォルト値の活用**: 面倒な設定は自動化
3. **エラーメッセージの明確化**: 何が悪いか一目瞭然
4. **ローディングの最小化**: レスポンスは3秒以内
5. **ユーザーテスト**: 各フェーズでフィードバック収集

---

## 📝 実装チェックリスト

### Phase 1 (MVP)
- [ ] プロフィール登録API
- [ ] 日次記録API（体重のみ）
- [ ] BMR/TDEE計算ロジック
- [ ] 挫折予測AI（基本版）
- [ ] 関口からのフィードバック生成
- [ ] 体重グラフ生成API
- [ ] LIFF: プロフィール登録画面
- [ ] LIFF: 記録入力画面
- [ ] LIFF: グラフ表示画面
- [ ] LIFF: 設定画面（基本）
- [ ] LINE Webhook設定
- [ ] リッチメニュー設定（3ボタン）
- [ ] データベースマイグレーション
- [ ] 単体テスト（主要ロジック）
- [ ] ユーザーテスト（5名）

### Phase 2 (機能強化)
- [ ] 食事記録API（カロリー・PFC）
- [ ] Gemini API連携（食事写真解析）
- [ ] メニュー提案API
- [ ] 栄養バランスフィードバック強化
- [ ] 週次レポート生成
- [ ] 挫折予測AI強化（バー下げ提案）
- [ ] LIFF: 食事記録画面拡張
- [ ] LIFF: 栄養グラフ追加
- [ ] LIFF: メニュー提案画面
- [ ] リッチメニュー拡張（6ボタン）
- [ ] 統合テスト
- [ ] パフォーマンステスト
- [ ] ユーザーテスト（20名）

### Phase 3 (差別化機能)
- [ ] 月次レポート生成
- [ ] プッシュ通知最適化
- [ ] プロフィール更新機能
- [ ] データエクスポート機能
- [ ] 管理画面（ユーザー管理）
- [ ] データベース最適化（インデックス）
- [ ] キャッシュ実装（Redis）
- [ ] エラー監視（Sentry）
- [ ] 本番環境デプロイ
- [ ] セキュリティ監査
- [ ] 負荷テスト
- [ ] ベータテスト（100名）

---

**次のステップ**: Phase 1 MVPの実装を開始しますか？
