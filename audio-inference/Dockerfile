FROM python:3.9-slim

# 作業ディレクトリ設定
WORKDIR /app

# 必要なシステムパッケージのインストール
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && apt-get clean

# Pythonパッケージの依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションファイルをコピー
COPY app.py .
COPY inference.py .
COPY model /app/model

# Flaskアプリケーションを実行
CMD ["python", "app.py"]
