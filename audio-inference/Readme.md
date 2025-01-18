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

## AWS ECR にイメージをプッシュ
### 1. ECR リポジトリのログイン
AWS CLI を使って ECR にログインします。

```bash
$ aws ecr get-login-password --region <REGION> | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com
```

例:

```bash
$ aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 937650212781.dkr.ecr.ap-northeast-1.amazonaws.com
```

### 2. イメージを ECR にタグ付け
ECR リポジトリ用のタグを設定します。

```bash
$ docker tag <LOCAL_IMAGE>:<TAG> <ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/<ECS_REPO_NAME>:<TAG>
```

例:

```bash
$ docker tag audio-inference:latest 937650212781.dkr.ecr.ap-northeast-1.amazonaws.com/audio-inference:latest
```

### 3. ECR にイメージをプッシュ
以下のコマンドで新しいイメージを ECR にプッシュします。

```bash
$ docker push <ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/<ECS_REPO_NAME>:<TAG>
```
例:

```bash
$ docker push 937650212781.dkr.ecr.ap-northeast-1.amazonaws.com/audio-inference:latest
```

タスク定義の登録
以下のコマンドで新しいタスク定義を登録します。

```bash
$ aws ecs register-task-definition --cli-input-json file://task-definition.json
```

### 4. ECS サービスを更新
ECS サービスが新しいタスク定義を使用するように更新します。

コマンド例
```bash
$ aws ecs update-service \
    --cluster audio-inference-cluster \
    --service audio-inference-service \
    --task-definition audio-inference-task
```
これにより、ECS サービスが新しいタスク定義を使用してタスクを再作成します。

**注意：新しいタスクはプライベートIP, パブリックIPが変わります。
タスクを更新したら、ターゲットグループの設定でIPを設定しなおしてください。**

### 5. デプロイの確認
タスクが新しいイメージで動作しているか確認：

```bash
$ aws ecs list-tasks --cluster audio-inference-cluster
```
タスクが正しく動作している場合、ヘルスチェックステータスが Healthy に変化するはずです。

```bash
$ aws elbv2 describe-target-health --target-group-arn <TARGET_GROUP_ARN>
```

## ECSサービス停止方法
タスクの停止
```
aws ecs update-service \
  --service $service_name \
  --cluster $cluster_name \
  --desired-count 0
```

タスクの起動
```
aws ecs update-service \
  --service $service_name \
  --cluster $cluster_name \
  --desired-count ${desired_count:-1}
```

#### 例
```
aws ecs update-service \
  --service audio-inference-service \
  --cluster audio-inference-cluster \
  --desired-count 0
```

```
aws ecs update-service \
  --service audio-inference-service \
  --cluster audio-inference-cluster \
  --desired-count ${desired_count:-1}
```

## 使い方（AWS版）

```bash
$ curl -X POST http://audio-inference-alb-1666523816.ap-northeast-1.elb.amazonaws.com/predict \
    -H "Content-Type: multipart/form-data" \
    -F "file=@audio-inference/data/sample_from_edge/voice/log_2024-12-31_18-13-16.csv"
{"confidence":0.9388715624809265,"predicted_class":1,"predicted_label":"People"}
```
## ToDo

- ECSのオートスケーリング: リクエストが連続するとCPU、メモリ使用率が100%近くなってサーバ-ダウンした。
- ドメイン名の策定
- セキュリティ対策

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