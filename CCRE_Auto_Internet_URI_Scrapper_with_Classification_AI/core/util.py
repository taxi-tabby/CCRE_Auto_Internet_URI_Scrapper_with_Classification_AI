
from datetime import datetime
import pytz

from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.core.predef import GLOBAL_TIMEZONE


def thlog(root_key: str, *args):
    """쓰레드 로그 출력용 함수."""
    time_zone = pytz.timezone(GLOBAL_TIMEZONE)
    current_time = datetime.now(time_zone).strftime("%Y-%m-%d %H:%M:%S")
    
    # args의 모든 항목을 문자열로 변환
    args = map(str, args)
    
    print(f"[{current_time}] [{root_key}] {' '.join(args)}")