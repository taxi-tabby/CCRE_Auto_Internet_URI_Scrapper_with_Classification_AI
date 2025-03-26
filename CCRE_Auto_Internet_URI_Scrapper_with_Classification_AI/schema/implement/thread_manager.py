import threading
import time
from .thread_worker import WorkerThread
from .thread_watcher import WatcherThread


class ThreadManager:
    def __init__(self):
        self.worker_threads = []  # 관리할 작업 쓰레드
        self.watcher_thread = None  # 관리할 감시자 쓰레드

    def add_worker(self, target, args=(), thread_id: (int|None)=None):
        """작업 쓰레드를 추가하는 메서드"""
        worker_thread = WorkerThread(thread_id, target, args)
        self.worker_threads.append(worker_thread)
        return worker_thread

    def add_watcher(self, check_interval=2):
        """감시자 쓰레드를 추가하는 메서드"""
        self.watcher_thread = WatcherThread(self.worker_threads, check_interval)
        return self.watcher_thread

    def start_all(self):
        """모든 쓰레드를 시작하는 메서드"""
        for worker in self.worker_threads:
            worker.start()
        if self.watcher_thread:
            self.watcher_thread.start()

    def stop_all(self):
        """모든 쓰레드를 종료하는 메서드"""
        for worker in self.worker_threads:
            print(worker.thread_id, 'worker thread signaled to stop')
            worker.stop()
           
        if self.watcher_thread:
            print('watcher thread signaled to stop')
            self.watcher_thread.stop()

    def join_all(self):
        """모든 쓰레드가 종료될 때까지 기다리는 메서드"""
        for worker in self.worker_threads:
            worker.join()
        if self.watcher_thread:
            self.watcher_thread.join()

    def get_active_worker_count(self):
        """현재 활성화된 작업 쓰레드 수를 반환하는 메서드"""
        return sum(1 for worker in self.worker_threads if worker.is_alive())

    def get_active_watcher_count(self):
        """현재 활성화된 감시자 쓰레드 수를 반환하는 메서드"""
        return 1 if self.watcher_thread and self.watcher_thread.is_alive() else 0