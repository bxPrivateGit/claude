## セットアップ手順

### 1. Claude Codeのインストール

```bash
# SageMaker Studio のターミナルを開く
# プロジェクトディレクトリに移動
cd ~/your-project-directory

# Claude Code をインストール
npm install -g @anthropic-ai/claude-code

# uvパッケージをインストール

pip install uv

※永続化されていないので、毎回実行する必要あり。
各自適宜、永続化してください。
```

### 3. 設定の永続化

```bash
# .bashrc に環境変数を追加して永続化
cat >> ~/.bashrc << 'EOF'

# Claude Code 設定
export CLAUDE_CODE_USE_BEDROCK=1
export ANTHROPIC_MODEL='us.anthropic.claude-sonnet-4-20250514-v1:0' # 使用するAIモデルを指定
export AWS_REGION='us-east-1'                                       # リージョンを指定

# Claude Sonnet 4 レート制限対策
export CLAUDE_CODE_REQUEST_DELAY=15000  # 15秒間隔
export CLAUDE_CODE_MAX_RETRIES=5        # リトライ5回
export CLAUDE_CODE_TIMEOUT=60000        # 60秒タイムアウト
export CLAUDE_CODE_BATCH_SIZE=1         # 一度に1リクエストのみ
EOF

# 設定を反映
source ~/.bashrc

# 設定確認（任意）
echo "CLAUDE_CODE_USE_BEDROCK: $CLAUDE_CODE_USE_BEDROCK"
echo "ANTHROPIC_MODEL: $ANTHROPIC_MODEL"
echo "AWS_REGION: $AWS_REGION"

# 永続化確認
cat ~/.bashrc

# 編集したい場合
nano ~/.bashrc

#レート制限に引っかかる場合（永続化はしない。一時的なもの）
export ANTHROPIC_MODEL='us.anthropic.claude-3-7-sonnet-20250219-v1:0'
※Ctrl+Cで、Claudeを終了したのち上記コマンドを実行。再度Claudeを起動してください。
```

### 4. MCPサーバーの設定

#### AWS公式ドキュメントMCPサーバー
```bash
# AWS ドキュメントMCPサーバーを追加
claude mcp add aws-documentation-mcp-server uvx "awslabs.aws-documentation-mcp-server@latest"
```

# 登録されたMCPサーバー一覧確認
claude mcp list

```

### 5. Claude の起動

```bash
# Claude を起動
claude

※初回起動時にいくつか選択項目が表示されるが、すべて推奨のものでOK

```



## 更新履歴

| 日付 | 更新内容 |
|------|----------|
| 2025-06-03 | 初版作成 |
