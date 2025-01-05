# Dockerイメージのビルドと実行方法
## Dockerイメージのビルド

```bash
$ docker build -t audio-inference .
```
## Dockerコンテナの実行
Linuxでの動作を想定。


### オプション説明:

- -v $(pwd)/model:/app/model: モデルファイルをコンテナにマウント。
- -v $(pwd)/data:/app/data: 音声ファイルを保存するディレクトリをコンテナにマウント。
- -it: 対話モードで実行。

## 使い方（Docker Compose）
Docker Composeでビルドだけの場合は以下のコマンドでイメージをビルドします。
```bash
$ docker-compose build --no-cache
```

Docker Composeでビルドと実行: 以下のコマンドでアプリケーションを起動します。
```bash
$ docker-compose up --build
```
--build オプションを使用して、イメージを再構築します。

バックグラウンドで実行: 以下のコマンドでコンテナをバックグラウンドで起動します。
起動後、アプリケーションは http://localhost:5000 でアクセス可能です。
```bash
$ docker-compose up -d
```

コンテナの停止: アプリケーションを停止するには、以下を実行します。
```bash
$ docker-compose down
```

ログの確認: 実行中のログを確認するには、以下を使用します。
```bash
$ docker-compose logs -f
```

アプリケーションが正しく動作する場合、以下のコマンドでAPIエンドポイントにアクセスできます。
```bash
$ curl -X POST http://localhost:5000/predict \
    -H "Content-Type: multipart/form-data" \
    -F "file=@audio-inference/data/sample_from_edge/clap/log_2024-12-31_18-02-48.csv"
```

## 使い方（Old）

- サーバー側で実行。
```bash
$ docker run -it --rm -p 5000:5000 audio-inference
```

- クライアント側で実行。

（/data/test_voice.m4a をアップロードする場合。）
```bash
curl -X POST http://localhost:5000/predict \
    -H "Content-Type: multipart/form-data" \
    -F "file=@audio-inference/data/test_voice.m4a"
```

csvファイル （/data/sample_from_edge/clap/log_2024-12-31_18-02-48.csv をアップロードする場合。）
```
$ curl -X POST http://localhost:5000/predict \
    -H "Content-Type: multipart/form-data" \
    -F "file=@audio-inference/data/sample_from_edge/clap/log_2024-12-31_18-02-48.csv"
```

JSONレスポンス
```
{
    "confidence":0.5755093693733215,
    "predicted_class":0,
    "predicted_label":"Other"
}
```