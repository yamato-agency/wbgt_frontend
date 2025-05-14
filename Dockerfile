# Python 3.8のベースイメージを使用
FROM python:3.8-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコピー
COPY requirements.txt .
COPY app.py .
COPY public/ ./public/

# 依存関係のインストール
RUN pip install --no-cache-dir -r requirements.txt

# 環境変数の設定
ENV PORT=8080

# アプリケーションの起動
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app 