#!/bin/bash

# Claude Code 環境確認スクリプト
# 作成日: 2025-06-17
# 説明: Claude Codeの設定状況を確認するスクリプト

# カラー定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ログ関数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

# 依存関係確認
check_dependencies() {
    log_header "依存関係確認"
    
    local all_good=true
    
    # Node.js
    if command -v node &> /dev/null; then
        log_info "Node.js: $(node --version)"
    else
        log_error "Node.js: 未インストール"
        all_good=false
    fi
    
    # npm
    if command -v npm &> /dev/null; then
        log_info "npm: $(npm --version)"
    else
        log_error "npm: 未インストール"
        all_good=false
    fi
    
    # Python3
    if command -v python3 &> /dev/null; then
        log_info "Python3: $(python3 --version)"
    else
        log_error "Python3: 未インストール"
        all_good=false
    fi
    
    # pip3
    if command -v pip3 &> /dev/null; then
        log_info "pip3: $(pip3 --version | cut -d' ' -f2)"
    else
        log_error "pip3: 未インストール"
        all_good=false
    fi
    
    if [ "$all_good" = true ]; then
        log_info "全ての依存関係が満たされています"
    else
        log_warn "一部の依存関係が不足しています"
    fi
    
    echo ""
}

# Claude Codeインストール確認
check_claude_code() {
    log_header "Claude Code確認"
    
    if command -v claude &> /dev/null; then
        log_info "Claude Code: インストール済み"
        
        # バージョン確認（可能であれば）
        claude --version 2>/dev/null || log_warn "バージョン情報を取得できません"
        
        # 実行パス
        log_info "実行パス: $(which claude)"
    else
        log_error "Claude Code: 未インストール"
        log_warn "npm install -g @anthropic-ai/claude-code を実行してください"
    fi
    
    echo ""
}

# uvパッケージ確認
check_uv() {
    log_header "uvパッケージ確認"
    
    if command -v uv &> /dev/null; then
        log_info "uv: インストール済み ($(uv --version))"
        log_info "実行パス: $(which uv)"
    else
        log_error "uv: 未インストール"
        log_warn "pip3 install --user uv を実行してください"
    fi
    
    echo ""
}

# 環境変数確認
check_environment_variables() {
    log_header "環境変数確認"
    
    local vars=(
        "CLAUDE_CODE_USE_BEDROCK"
        "ANTHROPIC_MODEL"
        "AWS_REGION"
        "CLAUDE_CODE_REQUEST_DELAY"
        "CLAUDE_CODE_MAX_RETRIES"
        "CLAUDE_CODE_TIMEOUT"
        "CLAUDE_CODE_BATCH_SIZE"
        "GITHUB_TOKEN"
    )
    
    for var in "${vars[@]}"; do
        if [ -n "${!var}" ]; then
            if [ "$var" = "GITHUB_TOKEN" ]; then
                log_info "$var: 設定済み (***秘匿***)"
            else
                log_info "$var: ${!var}"
            fi
        else
            log_warn "$var: 未設定"
        fi
    done
    
    echo ""
}

# MCPサーバー確認
check_mcp_servers() {
    log_header "MCPサーバー確認"
    
    if command -v claude &> /dev/null; then
        log_info "登録済みMCPサーバー:"
        claude mcp list 2>/dev/null || log_warn "MCPサーバー一覧を取得できません"
    else
        log_error "Claude Codeが未インストールのため、MCPサーバーを確認できません"
    fi
    
    echo ""
}

# GitHub API接続テスト
test_github_api() {
    log_header "GitHub API接続テスト"
    
    if [ -z "$GITHUB_TOKEN" ]; then
        log_warn "GITHUB_TOKENが設定されていません"
        log_warn "GitHub MCPサーバーを使用する場合は、トークンを設定してください"
        return
    fi
    
    if [ "$GITHUB_TOKEN" = "your_github_token_here" ]; then
        log_warn "GITHUB_TOKENがダミー値のままです"
        log_warn "実際のGitHubトークンに置き換えてください"
        return
    fi
    
    log_info "GitHub API接続をテスト中..."
    
    if command -v curl &> /dev/null; then
        local response=$(curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user)
        
        if echo "$response" | grep -q "login"; then
            local username=$(echo "$response" | grep -o '"login":"[^"]*' | cut -d'"' -f4)
            log_info "GitHub API接続成功 (ユーザー: $username)"
        else
            log_error "GitHub API接続失敗"
            echo "レスポンス: $response"
        fi
    else
        log_warn "curlが見つからないため、GitHub API接続テストをスキップします"
    fi
    
    echo ""
}

# .bashrc設定確認
check_bashrc_config() {
    log_header ".bashrc設定確認"
    
    if [ -f ~/.bashrc ]; then
        if grep -q "Claude Code 設定" ~/.bashrc; then
            log_info ".bashrcにClaude Code設定が見つかりました"
            
            log_info "設定内容:"
            grep -A 10 "Claude Code 設定" ~/.bashrc | grep "export" | while read line; do
                echo "  $line"
            done
        else
            log_warn ".bashrcにClaude Code設定が見つかりません"
        fi
    else
        log_error ".bashrcファイルが存在しません"
    fi
    
    echo ""
}

# 推奨事項表示
show_recommendations() {
    log_header "推奨事項"
    
    local issues=()
    
    # Claude Code未インストール
    if ! command -v claude &> /dev/null; then
        issues+=("Claude Codeをインストールしてください: npm install -g @anthropic-ai/claude-code")
    fi
    
    # uv未インストール
    if ! command -v uv &> /dev/null; then
        issues+=("uvパッケージをインストールしてください: pip3 install --user uv")
    fi
    
    # 環境変数未設定
    if [ -z "$CLAUDE_CODE_USE_BEDROCK" ]; then
        issues+=("環境変数が未設定です。setup_claude_code.shを実行してください")
    fi
    
    # GitHubトークン
    if [ -z "$GITHUB_TOKEN" ] || [ "$GITHUB_TOKEN" = "your_github_token_here" ]; then
        issues+=("GitHubトークンを設定してください: nano ~/.bashrc")
    fi
    
    if [ ${#issues[@]} -eq 0 ]; then
        log_info "設定に問題はありません！"
    else
        log_warn "以下の問題を解決してください:"
        for issue in "${issues[@]}"; do
            echo "  - $issue"
        done
    fi
    
    echo ""
}

# メイン実行
main() {
    echo -e "${BLUE}Claude Code 環境確認ツール${NC}"
    echo "実行日時: $(date)"
    echo ""
    
    check_dependencies
    check_claude_code
    check_uv
    check_environment_variables
    check_mcp_servers
    test_github_api
    check_bashrc_config
    show_recommendations
    
    log_info "環境確認が完了しました"
}

# スクリプト実行
main "$@"