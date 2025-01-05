FROM python:3.9-slim

# 作業ディレクトリ設定
WORKDIR /app

# ffmpegをインストール
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# 必要なファイルをコピー
COPY requirements.txt .
COPY app.py .
COPY inference.py .
COPY model /app/model

# 必要なライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt

# Flaskアプリケーションを実行
CMD ["python", "app.py"]
