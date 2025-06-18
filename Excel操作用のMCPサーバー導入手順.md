# Excel操作MCPサーバー

## 概要
SageMaker Studio上のClaudeCodeからExcelファイルを操作するためのMCPサーバーです。

## 機能
- 新規Excelファイル作成
- 表データの読み書き
- シート一覧取得
- ファイル一覧取得
- 基本的な書式設定（ヘッダー太字、枠線、列幅自動調整）


## プロジェクト構成
excel-mcp-server/                 ← プロジェクトルート
├── src/                         ← ソースコード
│   ├── __init__.py              ← Pythonパッケージ化用（「srcパッケージ」と認識させるための特別なファイル）
│   ├── server.py                ← MCPサーバーメイン
│   ├── excel_operations.py      ← Excel操作クラス
│   └── config.py                ← 設定管理
├── requirements.txt             ← 依存関係
├── run_server.py                ← 実行スクリプト（MCPサーバーを起動するためのエントリーポイント）
├── .gitignore                   ← Git除外設定
└── README.md                    ← プロジェクト説明

## 導入手順

```bash

Step 1: リポジトリからソースコードをclone
# Excel操作用のMCPサーバーをclone
git clone --branch main https://git-codecommit.ap-northeast-1.amazonaws.com/v1/repos/excel-mcp-server

# Cloneしてできたディレクトリへ移動する
cd excel-mcp-server/


Step 2: 依存関係のインストール

# SageMaker Studioのターミナルで実行
cd excel-mcp-server
pip install -r requirements.txt


Step 3: 動作確認テスト
# サーバーが正常に起動するかテスト
python3 test_server.py


Step 4: ClaudeCodeと統合
# プロジェクトディレクトリに移動
cd ~/your-project-directory

# 絶対パスを指定してMCPサーバーを追加
claude mcp add excel-server python3 /home/sagemaker-user/excel-mcp-server/run_server.py

# Claude を起動
claude 
