import threading
import time
from .thread_worker import WorkerThread

class WatcherThread(threading.Thread):
    def __init__(self, worker_threads, check_interval=2):
        super().__init__()
        self.worker_threads = worker_threads  
        self.check_interval = check_interval 
        self._stop_event = threading.Event()  # 중지 이벤트
        self.is_active = True  # 워커를 계속 관리하고 있는지 여부를 나타내는 플래그

    def run(self):
        """주기적으로 쓰레드들을 감시하며 상태를 체크하는 메서드"""
        while not self._stop_event.is_set():  # stop 이벤트가 설정되면 감시 종료
            time.sleep(self.check_interval)
            for worker in self.worker_threads:
                if not worker.is_alive():  # 워커가 살아 있지 않다면
                    print(f"Thread {worker.thread_id} is not alive.")
                    if self.is_active:  # 감시자가 활성 상태일 때만 재시작
                        self.restart_worker_thread(worker)

    def restart_worker_thread(self, worker):
        """쓰레드를 재시작하는 메서드"""
        if worker.is_alive():
            print(f"Stopping thread {worker.thread_id}...")
            worker.stop()
            worker.join()

        print(f"Restarting thread {worker.thread_id}...")
        # 새로운 워커 쓰레드를 생성하여 다시 시작
        new_worker = WorkerThread(worker.thread_id, worker.target, worker.args)
        self.worker_threads.remove(worker)  # 기존 워커 쓰레드를 리스트에서 제거
        self.worker_threads.append(new_worker)  # 새로운 워커 쓰레드를 리스트에 추가
        new_worker.start()

    def stop(self):
        """감시 쓰레드를 중지하는 메서드"""
        self._stop_event.set()  # 중지 이벤트 발생
        self.is_active = False  # 워커 재시작 방지
        if self.is_alive():
            self.join(timeout=0)  # 즉시 종료를 시도
