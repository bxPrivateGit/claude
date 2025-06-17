# Claude Code WSL環境セットアップツール

WSL環境でClaude Codeを簡単にセットアップするためのスクリプト集です。

## ファイル構成

- `setup_claude_code.sh` - メインセットアップスクリプト
- `claude_env_check.sh` - 環境確認スクリプト
- `README_claude_setup.md` - このドキュメント

## 使用方法

### 1. 初回セットアップ

```bash
# スクリプトを実行可能にする
chmod +x setup_claude_code.sh claude_env_check.sh

# セットアップを実行
./setup_claude_code.sh
```

### 2. 環境確認

```bash
# 現在の設定状況を確認
./claude_env_check.sh
```

### 3. GitHubトークンの設定

セットアップ後、GitHubトークンを設定してください：

```bash
# .bashrcを編集
nano ~/.bashrc

# 以下の行を見つけて、your_github_token_hereを実際のトークンに置換
export GITHUB_TOKEN="your_github_token_here"

# 設定を反映
source ~/.bashrc
```

### 4. Claude Code起動

```bash
# 新しいターミナルを開くか、設定を反映
source ~/.bashrc

# Claude Codeを起動
claude
```

## セットアップ内容

### 依存関係チェック
- Node.js
- npm
- Python3
- pip3

### インストール
- Claude Code (`@anthropic-ai/claude-code`)
- uvパッケージ

### 環境変数設定
- `CLAUDE_CODE_USE_BEDROCK=1`
- `AWS_REGION='ap-northeast-1'`
- `ANTHROPIC_MODEL='apac.anthropic.claude-sonnet-4-20250514-v1:0'`
- レート制限対策設定

### MCPサーバー設定
- AWS Documentation MCPサーバー
- GitHub MCPサーバー（トークン設定後）

## トラブルシューティング

### 依存関係エラー

Node.jsがない場合：
```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
```

Python3/pip3がない場合：
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### Claude Code起動エラー

環境変数が設定されていない場合：
```bash
source ~/.bashrc
```

### MCPサーバーエラー

手動でMCPサーバーを追加：
```bash
claude mcp add aws-documentation-mcp-server uvx "awslabs.aws-documentation-mcp-server@latest"
claude mcp add github uvx "mcp-github@latest"
```

## 環境確認項目

`claude_env_check.sh`で確認される項目：

1. **依存関係確認**
   - Node.js, npm, Python3, pip3のバージョン

2. **Claude Code確認**
   - インストール状況とバージョン

3. **uvパッケージ確認**
   - インストール状況とパス

4. **環境変数確認**
   - 全ての必要な環境変数の設定状況

5. **MCPサーバー確認**
   - 登録済みMCPサーバーの一覧

6. **GitHub API接続テスト**
   - GitHubトークンの有効性確認

7. **.bashrc設定確認**
   - 設定ファイルの内容確認

## 元となった手順書

このスクリプトは以下のマークダウンファイルを元に作成されています：
- `/mnt/c/Users/bxhom/OneDrive/.workspace/claude/CloudeCode手順書_t1 1.md`

## 注意事項

- GitHubトークンは必ず実際の値に置き換えてください
- AWS認証情報が別途必要な場合があります
- レート制限に注意して使用してください