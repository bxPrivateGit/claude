#!/usr/bin/env python3
"""
Excel MCP Server 実行スクリプト
"""
import sys
import os

# プロジェクトルートをPythonパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# サーバーを起動
from src.server import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())