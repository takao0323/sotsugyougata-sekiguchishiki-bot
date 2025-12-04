# 🎓 卒業型ダイエットメンター LINE Bot

世界で証明されたダイエット理論を、あなた専属のAIメンターが完全再現する LINE Bot版

## ✨ 主な機能

### 📱 LINE Bot機能
- ✅ **リッチメニュー**: ボタンで簡単操作
- ✅ **自動リマインダー**: 毎日10時に「今朝の体重はいかがでしたか？」と自動送信
- ✅ **日々の記録**: 体重・運動・食事・PFCを入力
- ✅ **関口さん風フィードバック**: 柔軟性を持たせた励まし
- ✅ **グラフ表示**: 体重推移を視覚化
- ✅ **プロフィール管理**: 目標・進捗確認
- ✅ **卒業セレモニー**: 表彰状とフィードバック収集

### 🎯 リッチメニュー
```
┌─────────┬─────────┬─────────┐
│ 今日の  │ グラフ  │プロフィ │
│ 記録    │ を見る  │ール    │
├─────────┼─────────┼─────────┤
│アドバイ │ 目標    │ ヘルプ  │
│ス      │ 確認    │        │
└─────────┴─────────┴─────────┘
```

## 🚀 セットアップ手順

### 1. LINE Developers 設定

#### 1.1 アカウント作成
1. https://developers.line.biz/ja/ にアクセス
2. LINEアカウントでログイン
3. 新規プロバイダーを作成

#### 1.2 Messaging API チャネル作成
1. 「Messaging API」を選択
2. チャネル名: `卒業型ダイエットメンター`
3. チャネル説明: `ダイエットサポートLINE Bot`
4. カテゴリ: `健康・フィットネス`
5. 作成完了

#### 1.3 必要な情報を取得

**Channel Access Token（長期）**:
1. チャネル基本設定 → Messaging API設定
2. 「チャネルアクセストークン（長期）」を発行
3. コピーして保存

**Channel Secret**:
1. チャネル基本設定 → 「チャネルシークレット」
2. コピーして保存

#### 1.4 応答設定
1. Messaging API設定 → 「応答メッセージ」をオフ
2. 「Webhook」をオン
3. Webhook URL: （後で設定）

### 2. ローカル開発環境のセットアップ

#### 2.1 依存関係のインストール
```bash
cd line_bot
pip install -r requirements.txt
```

#### 2.2 環境変数の設定
```bash
# .envファイルを作成
cp .env.example .env

# .envファイルを編集
nano .env
```

```.env
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token_here
LINE_CHANNEL_SECRET=your_channel_secret_here
GEMINI_API_KEY=your_gemini_api_key_here  # オプション
PORT=5000
```

#### 2.3 ngrok でトンネリング（ローカル開発用）
```bash
# ngrokをインストール（未インストールの場合）
# https://ngrok.com/download

# ポート5000を公開
ngrok http 5000
```

→ `https://xxxx-xxxx-xxxx.ngrok-free.app` のようなURLが表示される

#### 2.4 Webhook URL を設定
1. LINE Developers コンソール → Messaging API設定
2. Webhook URL: `https://xxxx-xxxx-xxxx.ngrok-free.app/callback`
3. 「検証」ボタンで接続確認

#### 2.5 アプリ起動
```bash
python app.py
```

出力例:
```
============================================================
🎓 卒業型ダイエットメンター LINE Bot
============================================================
Starting server...
Scheduler started. Next reminder: 毎日10:00
============================================================
✅ リッチメニュー作成完了: richmenu-xxxxx
 * Running on http://0.0.0.0:5000
```

### 3. クラウドデプロイ（本番環境）

#### オプション A: Render（おすすめ・無料枠あり）

1. https://render.com/ でアカウント作成
2. 「New +」→「Web Service」
3. GitHubリポジトリを接続
4. 設定:
   ```
   Name: diet-mentor-bot
   Environment: Python 3
   Build Command: pip install -r line_bot/requirements.txt
   Start Command: python line_bot/app.py
   ```
5. Environment Variables を追加:
   - `LINE_CHANNEL_ACCESS_TOKEN`
   - `LINE_CHANNEL_SECRET`
   - `GEMINI_API_KEY` (オプション)
6. 「Create Web Service」

7. Webhook URL を更新:
   - `https://diet-mentor-bot.onrender.com/callback`

#### オプション B: Heroku

```bash
# Heroku CLIをインストール
# https://devcenter.heroku.com/articles/heroku-cli

# ログイン
heroku login

# アプリ作成
heroku create diet-mentor-bot

# 環境変数を設定
heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your_token
heroku config:set LINE_CHANNEL_SECRET=your_secret
heroku config:set GEMINI_API_KEY=your_api_key

# デプロイ
git push heroku main

# Webhook URL を更新
# https://diet-mentor-bot.herokuapp.com/callback
```

### 4. リッチメニュー画像の作成（オプション）

リッチメニューに画像を設定したい場合:

1. **画像サイズ**: 2500 x 1686 px
2. **形式**: PNG または JPEG
3. **デザイン**: 6つのボタンエリアに対応

```
┌───────────┬───────────┬───────────┐
│  833x843  │  833x843  │  833x843  │  ← 上段
├───────────┼───────────┼───────────┤
│  833x842  │  833x842  │  833x842  │  ← 下段
└───────────┴───────────┴───────────┘
```

画像作成後:
```bash
# rich_menu.py の upload_rich_menu_image() を実装
# 画像をアップロード
```

## 📂 ファイル構成

```
line_bot/
├── app.py                  # メインアプリケーション
├── database.py             # データベース管理
├── message_handler.py      # メッセージ処理
├── rich_menu.py            # リッチメニュー管理
├── reminder.py             # リマインダーサービス
├── requirements.txt        # 依存関係
├── .env.example            # 環境変数テンプレート
├── .env                    # 環境変数（Git管理外）
├── README.md               # このファイル
└── diet_mentor.db          # SQLiteデータベース（自動生成）
```

## 🗃️ データベース構造

### users テーブル
```sql
- user_id (PRIMARY KEY)
- name, gender, age, height
- activity_level, activity_coefficient
- diet_mode, reduction_rate
- current_weight, initial_weight, target_weight
- target_calories, target_protein, target_fat, target_carbs
- bmr, tdee
- plan_name, duration_days
- start_date, current_day
- conversation_state
- created_at, updated_at
```

### daily_records テーブル
```sql
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- date, day_number
- weight, exercise, meal
- calories, protein, fat, carbs
- created_at
```

### feedbacks テーブル
```sql
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- achievements, good_points, overall_feedback
- created_at
```

## ⏰ スケジューラー

**毎日10:00に実行**:
- 今日の記録がないユーザーを検索
- リマインダーメッセージを送信
- 「今朝の体重はいかがでしたか？」

## 🔧 トラブルシューティング

### リッチメニューが表示されない
```bash
# リッチメニューを再作成
curl http://localhost:5000/setup_rich_menu
```

### Webhookエラー
1. LINE Developers コンソールで「検証」
2. ngrok/Render のURLが正しいか確認
3. アプリが起動しているか確認

### リマインダーが送信されない
1. スケジューラーが起動しているか確認
2. タイムゾーンが `Asia/Tokyo` か確認
3. ログを確認: `print` 出力を見る

### データベースエラー
```bash
# データベースを初期化
rm diet_mentor.db
python app.py  # 自動で再作成される
```

## 📝 ライセンス

MIT License

## 🙏 謝辞

このプロジェクトは、関口貴夫さんのYouTubeチャンネルとコーチングスタイルにインスパイアされて作成されました。

---

**Let's start your transformation journey! 💪**
