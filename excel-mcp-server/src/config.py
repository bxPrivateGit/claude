import os

# 設定値
EXCEL_FOLDER_NAME = "excel"
MAX_FILE_SIZE_MB = 50
SUPPORTED_EXTENSIONS = ['.xlsx']

def get_excel_directory():
    """現在のディレクトリにexcelフォルダを作成・取得"""
    current_dir = os.getcwd()
    excel_dir = os.path.join(current_dir, EXCEL_FOLDER_NAME)
    os.makedirs(excel_dir, exist_ok=True)
    return excel_dir

def get_excel_filepath(filename):
    """Excelファイルのフルパスを取得"""
    excel_dir = get_excel_directory()
    if not filename.endswith('.xlsx'):
        filename += '.xlsx'
    return os.path.join(excel_dir, filename)



#def get_project_root():
#    """プロジェクトルートディレクトリを取得"""
#    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#
#def get_excel_directory():
#    """excelファイル保存ディレクトリを取得"""
#    project_root = get_project_root()
#    excel_dir = os.path.join(project_root, EXCEL_FOLDER_NAME)
#    os.makedirs(excel_dir, exist_ok=True)
#    return excel_dir
#
#def get_excel_filepath(filename):
#    """Excelファイルのフルパスを取得"""
#    excel_dir = get_excel_directory()
#    if not filename.endswith('.xlsx'):
#        filename += '.xlsx'
#    return os.path.join(excel_dir, filename)