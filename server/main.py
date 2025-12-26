from network.server import MyServer
import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

if __name__ == "__main__":
    """The main entry point for the server application."""
    print("This is the main server file.")
    print("Starting server...")
    server = MyServer("0.0.0.0", 9000)
    server.start()
