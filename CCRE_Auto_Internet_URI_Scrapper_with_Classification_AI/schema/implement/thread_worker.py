import threading
import time

class WorkerThread(threading.Thread):
    def __init__(self, thread_id, target, args=()):
        super().__init__(target=target, args=args)
        self.thread_id = thread_id
        self.is_active = True  
        self._stop_event = threading.Event()  # 종료 이벤트
        self.target = target
        self.args = args

    def run(self):
        """쓰레드의 작업을 정의하는 메서드"""
        try:
            self.target(*self.args)  # 작업을 수행
        except Exception as e:
            print(f"Error in thread {self.thread_id}: {e}")
        finally:
            self.is_active = False  # 작업이 끝났을 때 상태 변경
            self.stop()  # 작업 완료 후 자동으로 종료

    def stop(self):
        """쓰레드를 중지하는 메서드"""
        self._stop_event.set()  # 종료 이벤트 발생
