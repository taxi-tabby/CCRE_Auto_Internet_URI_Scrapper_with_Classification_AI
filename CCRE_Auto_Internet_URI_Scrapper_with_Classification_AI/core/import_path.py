# path_manager.py
import sys
from pathlib import Path

def add_module_path(module_path: str):
    path = Path(module_path)
    if path.exists() and path.is_dir():
        sys.path.append(str(path))
        # print(f"경로 {module_path}가 sys.path에 추가되었습니다.")
    else:
        print(f"The path {module_path} does not exist or is not a valid directory.")
