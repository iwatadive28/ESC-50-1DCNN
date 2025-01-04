# Dockerイメージのビルドと実行方法
## Dockerイメージのビルド

```bash
$ docker build -t audio-inference .
```
## Dockerコンテナの実行
Linuxでの動作を想定。
```bash
$ docker run -it --rm -v $(pwd)/model:/app/model -v $(pwd)/data:/app/data audio-inference
```

### オプション説明:

- -v $(pwd)/model:/app/model: モデルファイルをコンテナにマウント。
- -v $(pwd)/data:/app/data: 音声ファイルを保存するディレクトリをコンテナにマウント。
- -it: 対話モードで実行。

## 使い方
以下のように表示されます。(録音モードは未対応)
```Python
音声ファイルをアップロードしますか？:0 , 音声を録音しますか？:1
選択: 0   
音声ファイルのフルパスを入力してください: data/test_voice.m4a
指定されたファイル: data/test_voice.m4a
推論を開始します...
1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 181ms/step
推論結果: クラス 0 (クラス1)
信頼スコア: 0.5755
```
