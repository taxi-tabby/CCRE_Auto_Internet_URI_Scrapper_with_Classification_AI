import socket
import threading
from typing import Callable, Optional, Tuple


InitCallbackType = Callable[[bool, str, str], None]
ReceiveHandlerCallbackType = Callable[[socket.socket, str, Tuple[str, int]], None]

class UDPServer:
    def __init__(self, host='0.0.0.0', port=12345, whitelist=None, callback=None, init_callback: InitCallbackType = None):
        self.host = host
        self.port = port
        self.whitelist = whitelist if whitelist else []
        self.server_socket = None
        self.server_thread = None
        self.running = False  # 서버 실행 여부
        self.lock = threading.Lock()
        self.callback: ReceiveHandlerCallbackType = callback  # 콜백 함수 저장 (기본값 None), _RetAddress는 Tuple[str, int] 로 대체 가능.
        self.init_callback: InitCallbackType = init_callback  # 초기화 콜백 함수 저장 (기본값 None)

    def add_to_whitelist(self, ip):
        """화이트리스트에 IP를 추가합니다."""
        with self.lock:
            if ip not in self.whitelist:
                self.whitelist.append(ip)
                print(f"{ip}가 화이트리스트에 추가되었습니다.")
                return True
            print(f"{ip}는 이미 화이트리스트에 있습니다.")
            return False

    def remove_from_whitelist(self, ip):
        """화이트리스트에서 IP를 제거합니다."""
        with self.lock:
            if ip in self.whitelist:
                self.whitelist.remove(ip)
                print(f"{ip}가 화이트리스트에서 제거되었습니다.")
                return True
            print(f"{ip}는 화이트리스트에 없습니다.")
            return False

    def set_callback(self, callback: ReceiveHandlerCallbackType):
        """콜백 함수를 설정합니다."""
        self.callback = callback
        
    def set_init_callback(self, init_callback: InitCallbackType):
        """초기화 콜백 함수를 설정합니다."""
        self.init_callback = init_callback
        

    def handle_client(self):
        """클라이언트의 요청을 처리하는 함수"""
        while self.running:
            try:
                data, client_address = self.server_socket.recvfrom(1024)
                client_ip = client_address[0]

                # 화이트리스트 검사
                if self.whitelist and client_ip not in self.whitelist:
                    print(f"허용되지 않은 IP: {client_ip}에서 접근을 차단했습니다.")
                    continue

                print(f"받은 데이터: {data.decode()} from {client_ip}")

                # 콜백이 설정되어 있으면 콜백으로 처리
                if self.callback:
                    self.callback(self.server_socket, data.decode(), client_address, )
                else:
                    # 기본 응답 (콜백이 없을 경우)
                    response = "Hello, UDP client!"
                    self.server_socket.sendto(response.encode(), client_address)
            except Exception as e:
                print(f"클라이언트 처리 중 오류: {e}")
                break

    def listen(self):
        """서버가 클라이언트의 메시지를 수신합니다."""
        if self.server_thread is not None and self.server_thread.is_alive():
            print("서버는 이미 실행 중입니다.")
            return False  # 이미 스레드가 실행 중이면 새로 시작하지 않음

        try:
            # UDP 소켓 설정
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server_socket.bind((self.host, self.port))
            self.running = True

            # 스레드로 클라이언트 핸들링
            self.server_thread = threading.Thread(target=self.handle_client, daemon=True)
            self.server_thread.start()
            self.init_callback(True, self.host, self.port)
            
            return True
        except Exception as e:
            self.init_callback(False, self.host, self.port)
            return False

    def stop(self):
        """서버를 종료하고 스레드를 안전하게 종료합니다."""
        with self.lock:
            if self.running:
                self.running = False
                if self.server_socket:
                    self.server_socket.close()  # 소켓 종료
                if self.server_thread:
                    self.server_thread.join()  # 스레드 종료
                return True
            else:
                return False
            
            
    def is_running(self) -> bool:
        """서버가 실행 중인지 확인합니다."""
        return self.running