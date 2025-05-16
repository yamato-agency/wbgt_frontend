# 全国47都道府県の暑さ指数情報アプリケーション

環境省が提供する暑さ指数（WBGT）データを表示するWebアプリケーションです。
全国47都道府県の観測地点に対応しています。

## 機能

- 全国47都道府県の暑さ指数（WBGT）の表示
- 30分ごとの自動更新
- 暑さ指数に応じた色分け表示
  - 危険（31℃以上）: 赤色
  - 厳重警戒（28℃以上）: オレンジ色
  - 警戒（25℃以上）: 黄色
  - 注意（21℃以上）: 水色
  - さらに安全（21℃未満）: 薄い水色

## 技術スタック

- フロントエンド: HTML, CSS, JavaScript
- バックエンド: Python, Flask
- デプロイ: Google Cloud Run, GitHub Pages

## プロジェクト構成

### 主要ファイル

- `app.py`: バックエンドのメインアプリケーションファイル
  - Flaskアプリケーションの設定
  - CORS設定
  - 環境省の暑さ指数データを取得するAPIエンドポイント
  - 都道府県の観測地点設定

- `public/index.html`: フロントエンドのメインファイル
  - 暑さ指数情報の表示
  - 自動更新機能
  - レスポンシブデザイン
  - 色分け表示の実装

- `public/generate_html.py`: 都道府県別HTMLファイル生成スクリプト
  - 47都道府県の観測地点データ
  - 各都道府県用のHTMLファイルを、対応するwbgt_xxxxフォルダ内に`index.html`として生成
    - 例: `public/wbgt_kyoto/index.html`, `public/wbgt_okinawa/index.html` など

- `requirements.txt`: Pythonの依存関係管理ファイル
  - Flask: Webアプリケーションフレームワーク
  - requests: HTTPリクエスト用ライブラリ
  - Flask-Cors: CORS対応用ライブラリ
  - gunicorn: 本番環境用のWSGIサーバー

### デプロイ関連ファイル

- `Dockerfile`: コンテナ化設定ファイル
  - Python 3.8ベースイメージの使用
  - 必要なファイルのコピー
  - 依存関係のインストール
  - アプリケーションの起動設定

- `cloudbuild.yaml`: Google Cloud Build設定ファイル
  - Dockerイメージのビルド設定
  - Container Registryへのプッシュ設定
  - Cloud Runへのデプロイ設定

- `.github/workflows/deploy.yml`: GitHub Actions設定ファイル
  - GitHub Pagesへのデプロイ設定
  - 静的ファイルの自動デプロイ

## ローカル環境での動作確認方法

### 1. 必要なソフトウェアのインストール

- Python 3.8以上
- pip（Pythonパッケージマネージャー）

### 2. プロジェクトのセットアップ

1. リポジトリをクローンまたはダウンロード
```bash
git clone <リポジトリのURL>
cd my-wbgt-app_prefecture
```

2. 仮想環境の作成と有効化
```bash
# Windowsの場合
python -m venv venv
venv\Scripts\activate

# macOS/Linuxの場合
python3 -m venv venv
source venv/bin/activate
```

3. 必要なパッケージのインストール
```bash
pip install -r requirements.txt
```

### 3. アプリケーションの起動

1. バックエンドサーバーの起動
```bash
python app.py
```
サーバーは http://localhost:5000 で起動します。

2. フロントエンドの表示
- `public/index.html` をブラウザで開く
- または、以下のコマンドで簡易的なHTTPサーバーを起動
```bash
# publicディレクトリに移動
cd public

# Pythonの簡易HTTPサーバーを起動
python -m http.server 8000
```
その後、ブラウザで http://localhost:8000 にアクセス

### 4. 動作確認

1. ブラウザで http://localhost:8000 にアクセス
2. 各都道府県の暑さ指数情報が表示されることを確認
3. 30分ごとに自動更新されることを確認
4. 暑さ指数の値に応じて色が変化することを確認

## デプロイ方法

### Google Cloud Runへのデプロイ

1. GCPプロジェクトの準備
```bash
# GCPプロジェクトの作成（既存のプロジェクトを使用する場合はスキップ）
gcloud projects create [PROJECT_ID]

# プロジェクトの設定
gcloud config set project [PROJECT_ID]

# 必要なAPIの有効化
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

2. アプリケーションのデプロイ
```bash
# Cloud Buildを使用してデプロイ
gcloud builds submit --config cloudbuild.yaml
```

### GitHub Pagesへのデプロイ

1. リポジトリの設定
- GitHubリポジトリの設定で、GitHub Pagesのソースを`gh-pages`ブランチに設定

2. デプロイの自動化
- `main`ブランチへのプッシュ時に自動的にGitHub Pagesにデプロイされます
- デプロイの設定は`.github/workflows/deploy.yml`で管理されています

## 注意事項

- ローカル環境では、バックエンドのCORS設定により、`public/index.html`を直接ブラウザで開く場合は動作しません。
- 必ずHTTPサーバー経由でアクセスしてください。
- 本番環境（Google Cloud Run）では、適切なCORS設定が行われています。

## トラブルシューティング

1. データが表示されない場合
   - バックエンドサーバーが正常に起動しているか確認
   - ブラウザのコンソールでエラーメッセージを確認
   - ネットワーク接続を確認

2. 自動更新が動作しない場合
   - ブラウザのコンソールでエラーメッセージを確認
   - ネットワーク接続を確認

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。 