import threading
import time
import traceback

from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.core.util import thlog

class WorkerThread(threading.Thread):
    def __init__(self, thread_id, target, args=(), custom_name: str = "worker_noname"):
        super().__init__(target=target, args=args)
        self.thread_id = thread_id
        self.is_active = True  
        self._stop_event = threading.Event()  # 종료 이벤트
        self.target = target
        self.args = args
        # self.max_retries = max_retries  # 최대 재시도 횟수
        # self.retry_interval = retry_interval  # 재시도 간격 (초)
        self.custom_name = custom_name  # 사용자 정의 이름
        self.name = f"worker_thread_{custom_name}"  # 쓰레드 이름 설정
        self.daemon = True  # 데몬 쓰레드로 설정하여 메인 프로그램 종료 시 자동으로 종료됨

    def run(self):
        """쓰레드의 작업을 정의하는 메서드"""

        def in_stop(): 
            self.is_active = False  # 작업이 끝났을 때 상태 변경
            self.stop()  # 작업 완료 후 자동으로 종료

        while not self._stop_event.is_set():
            try:
                self.target(*self.args)
                # print('---------------------------------------------------')
                break
            except Exception as e:
                # thlog(self.name, f" Worker stopped (id: {self.thread_id}): {e}")
                # print("Traceback (most recent call last):")
                # traceback.print_exc()
                # print(f"Error occurred at: {traceback.extract_tb(e.__traceback__)[-1]}")
                
                #에러나면 종료처리 짜피 감시자 쓰레드가 다시 실행시킴.
                in_stop()
                
        #프로그램 다 끝나면 종료처리
        in_stop()

        

    def stop(self):
        """쓰레드를 중지하는 메서드"""
        self._stop_event.set()  # 종료 이벤트 발생
