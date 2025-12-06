# ダイエットメンター LINE Bot - Phase 1 MVP

関口式トレーニングを元にした、挫折させないダイエットサポートLINE Bot

## 📋 プロジェクト概要

このプロジェクトは、ダイエットに何度も挫折した人をサポートするためのLINE公式アカウント実装です。

### Phase 1 MVP（最小限の価値提供）

- ✅ プロフィール登録（LIFF）
- ✅ 毎日の体重記録（LIFF）
- ✅ 関口からのフィードバック（チャット）
- ✅ 挫折予測AI（リスク検知）
- ✅ 体重グラフ表示（LIFF）

## 🛠️ 技術スタック

- **Backend**: Flask 3.0
- **Database**: SQLite（開発）/ PostgreSQL（本番）
- **LINE**: Messaging API + LIFF v2
- **Python**: 3.11+

## 📂 ディレクトリ構造

```
diet-mentor-line-bot/
├── app/
│   ├── models/          # データベースモデル
│   │   ├── user.py
│   │   ├── daily_record.py
│   │   └── feedback.py
│   ├── services/        # ビジネスロジック
│   │   ├── dropout_ai.py       # 挫折予測AI
│   │   ├── feedback_service.py # フィードバック生成
│   │   └── ...
│   ├── routes/          # APIルート
│   │   ├── liff_api.py          # LIFF用API
│   │   └── webhook.py           # LINE Webhook
│   ├── utils/           # ユーティリティ
│   │   └── calculations.py      # BMR/TDEE計算
│   └── config.py        # 設定
├── liff/                # LIFF（フロントエンド）
├── database/
│   ├── migrations/      # マイグレーション
│   └── seeds/           # 初期データ
├── tests/               # テスト
├── requirements.txt     # Python依存関係
└── README.md
```

## 🚀 セットアップ

### 1. 環境構築

```bash
# Python環境のセットアップ
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt
```

### 2. 環境変数の設定

`.env`ファイルを作成：

```bash
# Flask
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database
DATABASE_URL=sqlite:///diet_mentor_dev.db

# LINE Bot
LINE_CHANNEL_ACCESS_TOKEN=your-line-channel-access-token
LINE_CHANNEL_SECRET=your-line-channel-secret

# LIFF
LIFF_ID=your-liff-id
```

### 3. データベースのセットアップ

```bash
# マイグレーションの実行（TODO: alembicセットアップ後）
python -c "from app.models import Base; from sqlalchemy import create_engine; engine = create_engine('sqlite:///diet_mentor_dev.db'); Base.metadata.create_all(engine)"
```

### 4. サーバー起動

```bash
# 開発サーバー起動
python app.py
```

## 📝 実装状況

### 完了 ✅

- [x] プロジェクト構造作成
- [x] requirements.txt作成
- [x] データベースモデル（User, DailyRecord, Feedback）
- [x] 計算ロジック（BMR/TDEE/PFC）
- [x] 挫折予測AI

### 進行中 🚧

- [ ] フィードバック生成ロジック
- [ ] プロフィール登録API
- [ ] 日次記録API（体重のみ）
- [ ] 体重グラフデータ取得API
- [ ] LINE Webhookエンドポイント
- [ ] LIFF実装

### 未着手 📋

- [ ] 単体テスト
- [ ] 統合テスト
- [ ] デプロイ設定

## 📖 API設計

詳細は`LINE_IMPLEMENTATION_DESIGN.md`を参照してください。

### 主要エンドポイント

- `POST /api/v1/profile` - プロフィール登録
- `GET /api/v1/profile/{user_id}` - プロフィール取得
- `POST /api/v1/records` - 日次記録登録
- `GET /api/v1/records/{user_id}` - 日次記録取得
- `GET /api/v1/graph/weight/{user_id}` - 体重グラフデータ取得
- `POST /callback` - LINE Webhook

## 🧪 テスト

```bash
# テスト実行
pytest

# カバレッジ付きテスト
pytest --cov=app tests/
```

## 📚 参考ドキュメント

- [LINE Messaging API](https://developers.line.biz/ja/docs/messaging-api/)
- [LIFF Documentation](https://developers.line.biz/ja/docs/liff/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

## 📄 ライセンス

MIT License

## 👥 開発者

関口式トレーニングを元にしたダイエットサポートプログラム
