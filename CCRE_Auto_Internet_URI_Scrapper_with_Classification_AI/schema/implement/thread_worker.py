import threading
import time
import traceback

from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.core.util import thlog

class WorkerThread(threading.Thread):
    def __init__(self, thread_id, target, args=(), max_retries=2, retry_interval=5):
        super().__init__(target=target, args=args)
        self.thread_id = thread_id
        self.is_active = True  
        self._stop_event = threading.Event()  # 종료 이벤트
        self.target = target
        self.args = args
        self.max_retries = max_retries  # 최대 재시도 횟수
        self.retry_interval = retry_interval  # 재시도 간격 (초)

    def run(self):
        """쓰레드의 작업을 정의하는 메서드"""
        retry_count = 0  # 재시도 횟수
        while retry_count < self.max_retries and not self._stop_event.is_set():
            try:
                self.target(*self.args)  # 작업을 수행
                break  # 작업이 성공적으로 끝났으면 루프를 탈출
            except Exception as e:
                
                thlog(self.name, f" Worker stopped (id: {self.thread_id}): {e}")
                # print("Traceback (most recent call last):")
                # traceback.print_exc()
                # print(f"Error occurred at: {traceback.extract_tb(e.__traceback__)[-1]}")
                
                retry_count += 1  # 재시도 횟수 증가
                if retry_count < self.max_retries:
                    thlog(self.name, f"Worker retrying... ({retry_count}/{self.max_retries})")
                    time.sleep(self.retry_interval)  # 재시도 전에 대기
                else:
                    thlog(self.name, f"Worker max retries reached. Exiting thread {self.thread_id}.")
                    self._stop_event.set()  # 최대 재시도 횟수에 도달하면 종료 이벤트 발생

        self.is_active = False  # 작업이 끝났을 때 상태 변경
        self.stop()  # 작업 완료 후 자동으로 종료

    def stop(self):
        """쓰레드를 중지하는 메서드"""
        self._stop_event.set()  # 종료 이벤트 발생
