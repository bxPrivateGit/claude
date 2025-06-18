import asyncio
import json
from typing import Any, Sequence
from mcp.server import Server
from mcp.types import Resource, Tool, TextContent
from .excel_operations import ExcelOperations
from .config import get_excel_directory

# MCPサーバーの初期化
server = Server("excel-mcp-server")

@server.list_resources()
async def list_resources() -> list[Resource]:
    """利用可能なExcelファイルをリソースとして一覧表示"""
    result = ExcelOperations.list_excel_files()
    resources = []
    
    if result["success"]:
        for file_info in result["files"]:
            # 各ファイルのシート情報も取得
            sheets_result = ExcelOperations.list_sheets(file_info["filename"])
            if sheets_result["success"]:
                for sheet_name in sheets_result["sheets"]:
                    resources.append(Resource(
                        uri=f"excel://{file_info['filename']}/{sheet_name}",
                        name=f"{file_info['filename']} - {sheet_name}",
                        mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        description=f"Excelファイル: {file_info['filename']}, シート: {sheet_name}"
                    ))
    
    return resources

@server.read_resource()
async def read_resource(uri: str) -> str:
    """Excelリソースの内容を読み取り"""
    try:
        # URI解析: excel://filename.xlsx/SheetName
        if not uri.startswith("excel://"):
            raise ValueError("無効なURI形式です")
        
        path = uri.replace("excel://", "")
        parts = path.split("/")
        if len(parts) != 2:
            raise ValueError("URI形式が正しくありません")
        
        filename, sheet_name = parts
        
        # データ読み込み
        result = ExcelOperations.read_excel_data(filename, sheet_name)
        
        if result["success"]:
            return json.dumps({
                "content": result["data"],
                "summary": f"ファイル: {filename}, シート: {sheet_name}, "
                          f"行数: {result['rows']}, 列数: {result['columns']}"
            }, ensure_ascii=False, indent=2)
        else:
            return json.dumps({"error": result["error"]}, ensure_ascii=False)
            
    except Exception as e:
        return json.dumps({"error": f"リソース読み取りエラー: {str(e)}"}, ensure_ascii=False)

@server.list_tools()
async def list_tools() -> list[Tool]:
    """利用可能なツール一覧"""
    return [
        Tool(
            name="create_excel_file",
            description="新しいExcelファイルを作成します",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "作成するExcelファイル名（.xlsx拡張子は自動追加）"
                    },
                    "sheet_name": {
                        "type": "string",
                        "description": "初期シート名（オプション、デフォルト: Sheet1）",
                        "default": "Sheet1"
                    }
                },
                "required": ["filename"]
            }
        ),
        Tool(
            name="write_excel_data",
            description="Excelファイルに表データを書き込みます",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "対象のExcelファイル名"
                    },
                    "sheet_name": {
                        "type": "string",
                        "description": "書き込み先シート名"
                    },
                    "data": {
                        "type": "array",
                        "description": "書き込むデータ（JSON配列形式）",
                        "items": {
                            "type": "object"
                        }
                    },
                    "start_cell": {
                        "type": "string",
                        "description": "開始セル位置（例: A1）",
                        "default": "A1"
                    },
                    "include_header": {
                        "type": "boolean",
                        "description": "ヘッダー行を含むかどうか",
                        "default": True
                    }
                },
                "required": ["filename", "sheet_name", "data"]
            }
        ),
        Tool(
            name="read_excel_data",
            description="Excelファイルから表データを読み込みます",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "読み込み対象のExcelファイル名"
                    },
                    "sheet_name": {
                        "type": "string",
                        "description": "読み込み対象シート名"
                    },
                    "range": {
                        "type": "string",
                        "description": "読み込むセル範囲（例: A1:C10、オプション）"
                    },
                    "has_header": {
                        "type": "boolean",
                        "description": "ヘッダー行があるかどうか",
                        "default": True
                    }
                },
                "required": ["filename", "sheet_name"]
            }
        ),
        Tool(
            name="list_sheets",
            description="Excelファイル内のシート一覧を取得します",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "対象のExcelファイル名"
                    }
                },
                "required": ["filename"]
            }
        ),
        Tool(
            name="list_excel_files",
            description="利用可能なExcelファイル一覧を取得します",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None) -> Sequence[TextContent]:
    """ツール実行"""
    if arguments is None:
        arguments = {}
    
    try:
        if name == "create_excel_file":
            result = ExcelOperations.create_excel_file(
                filename=arguments["filename"],
                sheet_name=arguments.get("sheet_name", "Sheet1")
            )
        
        elif name == "write_excel_data":
            result = ExcelOperations.write_excel_data(
                filename=arguments["filename"],
                sheet_name=arguments["sheet_name"],
                data=arguments["data"],
                start_cell=arguments.get("start_cell", "A1"),
                include_header=arguments.get("include_header", True)
            )
        
        elif name == "read_excel_data":
            result = ExcelOperations.read_excel_data(
                filename=arguments["filename"],
                sheet_name=arguments["sheet_name"],
                range_cells=arguments.get("range"),
                has_header=arguments.get("has_header", True)
            )
        
        elif name == "list_sheets":
            result = ExcelOperations.list_sheets(
                filename=arguments["filename"]
            )
        
        elif name == "list_excel_files":
            result = ExcelOperations.list_excel_files()
        
        else:
            result = {"success": False, "error": f"不明なツール: {name}"}
        
        return [TextContent(
            type="text",
            text=json.dumps(result, ensure_ascii=False, indent=2)
        )]
        
    except Exception as e:
        error_result = {
            "success": False,
            "error": f"ツール実行エラー ({name}): {str(e)}"
        }
        return [TextContent(
            type="text",
            text=json.dumps(error_result, ensure_ascii=False, indent=2)
        )]

async def main():
    """メイン実行関数"""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())