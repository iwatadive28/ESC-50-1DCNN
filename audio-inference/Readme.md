# Dockerイメージのビルドと実行方法
## Dockerイメージのビルド

```bash
$ dockebuild -t audio-inference .
```
## Dockerコンテナの実行
Linuxでの動作を想定。


### オプション説明:

- -v $(pwd)/model:/app/model: モデルファイルをコンテナにマウント。
- -v $(pwd)/data:/app/data: 音声ファイルを保存するディレクトリをコンテナにマウント。
- -it: 対話モードで実行。

## 使い方


- サーバー側で実行。
```bash
$ dockerun -it --rm -p 5000:5000 audio-inference
```

- クライアント側で実行。
（/data/test_voice.m4a をアップロードする場合。）
```bash
curl -X POST http://localhost:5000/predict \
    -H "Content-Type: multipart/form-data" \
    -F "file=@audio-interface/data/test_voice.m4a"
```

JSONレスポンス
```
{
    "confidence":0.5755093693733215,
    "predicted_class":0,
    "predicted_label":"Other"
}
```