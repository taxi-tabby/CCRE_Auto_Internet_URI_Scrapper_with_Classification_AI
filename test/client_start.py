import sys
import os

# 테스트용 루트 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.module import server_start
server_start()