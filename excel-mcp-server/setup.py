
from setuptools import setup, find_packages

setup(
    name="excel-mcp-server",
    version="1.0.0",
    description="Excel操作用MCPサーバー",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "mcp>=1.0.0",
        "openpyxl>=3.1.0",
        "pandas>=2.0.0",
        "pytest>=7.0.0",
    ],
    entry_points={
        "console_scripts": [
            "excel-mcp-server=src.server:main",
        ],
    },
)