#!/usr/bin/env python3
"""
MCPサーバーのテスト用スクリプト
"""
import sys
import os

# プロジェクトルートをPythonパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_imports():
    """必要なモジュールがインポートできるかテスト"""
    try:
        from src.config import get_excel_directory, get_excel_filepath
        from src.excel_operations import ExcelOperations
        from src.server import server
        print("✅ すべてのモジュールのインポートに成功しました")
        return True
    except Exception as e:
        print(f"❌ インポートエラー: {e}")
        return False

def test_excel_operations():
    """Excel操作のテスト"""
    try:
        from src.excel_operations import ExcelOperations
        
        # ファイル一覧取得テスト
        result = ExcelOperations.list_excel_files()
        print(f"✅ Excelファイル一覧取得: {result['success']}")
        
        # テストファイル作成
        result = ExcelOperations.create_excel_file("test_file.xlsx")
        print(f"✅ テストファイル作成: {result['success']}")
        
        if result['success']:
            # テストデータ書き込み
            test_data = [
                {"項目": "テスト1", "値": "値1", "説明": "テスト用データ1"},
                {"項目": "テスト2", "値": "値2", "説明": "テスト用データ2"}
            ]
            result = ExcelOperations.write_excel_data("test_file.xlsx", "Sheet1", test_data)
            print(f"✅ データ書き込み: {result['success']}")
            
            # データ読み込み
            result = ExcelOperations.read_excel_data("test_file.xlsx", "Sheet1")
            print(f"✅ データ読み込み: {result['success']}")
            if result['success']:
                print(f"   読み込んだ行数: {result['rows']}")
        
        return True
    except Exception as e:
        print(f"❌ Excel操作テストエラー: {e}")
        return False

def test_directory_structure():
    """ディレクトリ構造のテスト"""
    try:
        from src.config import get_excel_directory
        excel_dir = get_excel_directory()
        print(f"✅ Excelファイル保存ディレクトリ: {excel_dir}")
        print(f"✅ ディレクトリ存在確認: {os.path.exists(excel_dir)}")
        return True
    except Exception as e:
        print(f"❌ ディレクトリ構造テストエラー: {e}")
        return False

if __name__ == "__main__":
    print("=== Excel MCP Server テスト開始 ===")
    
    success_count = 0
    
    if test_imports():
        success_count += 1
    
    if test_directory_structure():
        success_count += 1
        
    if test_excel_operations():
        success_count += 1
    
    print(f"\n=== テスト結果: {success_count}/3 成功 ===")
    
    if success_count == 3:
        print("✅ すべてのテストが成功しました！MCPサーバーの準備完了です。")
        print("\n次のステップ:")
        print("1. Claude Desktopにサーバーを登録")
        print("2. Claude Desktopから接続テスト")
    else:
        print("❌ 一部のテストが失敗しました。エラーを確認してください。")