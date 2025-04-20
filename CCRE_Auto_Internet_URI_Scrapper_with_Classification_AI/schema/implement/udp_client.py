import socket
import threading
from typing import Callable, Optional, Tuple

# 콜백 타입 정의
InitCallbackType = Callable[[bool, str, str], None]
ReceiveHandlerCallbackType = Callable[[str, Tuple[str, int]], None]

class UDPClient:
    def __init__(self, callback: Optional[ReceiveHandlerCallbackType] = None, init_callback: Optional[InitCallbackType] = None):
        self.server_ip = None
        self.server_port = None
        self._client_port = None  # Renamed to avoid naming conflict
        self.client_socket = None
        self.running = False  # 클라이언트 실행 여부
        self.lock = threading.Lock()
        self.callback = callback  # 응답 처리 콜백 함수
        self.init_callback = init_callback  # 초기화 콜백 함수
        self.client_thread = None  # 응답 수신을 위한 스레드
    
    def init_connection(self):
        """연결 정보를 초기화합니다."""
        # 기존 연결이 있는 경우 종료
        if self.running:
            self.stop()
            
        # 연결 상태 초기화
        self.server_ip = None
        self.server_port = None
        self._client_port = None
        self.client_socket = None
        self.running = False
        self.client_thread = None
        print("연결 정보가 초기화되었습니다.")
        
        
        
    def connect(self, server_ip: str, server_port: int, client_port: Optional[int] = None) -> bool:
        """서버에 연결합니다."""
        try:
            self.server_ip = server_ip
            self.server_port = server_port
            self._client_port = client_port
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            

            if self._client_port:
                self.client_socket.bind(('0.0.0.0', self._client_port))  # 클라이언트 포트 바인딩
                
            if self.init_callback:
                self.init_callback(True, "연결 성공", f"{server_ip}:{server_port}")
                
            return True
        
        except Exception as e:
            if self.init_callback:
                self.init_callback(False, f"연결 실패: {e}", f"{server_ip}:{server_port}")
                
            print(f"연결 실패: {e}")
            return False






    def set_callback(self, callback: ReceiveHandlerCallbackType):
        """응답을 처리할 콜백 함수를 설정합니다."""
        self.callback = callback
        print("콜백 함수가 설정되었습니다.")


    def set_init_callback(self, init_callback: InitCallbackType):
        """초기화 콜백 함수를 설정합니다."""
        self.init_callback = init_callback
        

    def send_message(self, message: str) -> bool:
        """서버로 메시지를 전송하고 응답을 받습니다."""
        try:
            # 서버로 메시지 전송
            self.client_socket.sendto(message.encode(), (self.server_ip, self.server_port))
            print(f"서버로 메시지를 보냈습니다: {message}")
            return True
        except Exception as e:
            print(f"메시지 전송 중 오류: {e}")
            return False
        
        
    def listen_for_responses(self):
        """서버로부터 오는 응답을 수신하는 메서드"""
        while self.running:
            try:
                # 소켓이 유효한지 확인
                if not self.client_socket:
                    print("소켓이 닫혔습니다. 응답 수신을 종료합니다.")
                    break
                    
                # Use timeout to avoid blocking forever
                self.client_socket.settimeout(0.5)  # 0.5초 타임아웃
                
                try:
                    data, server_address = self.client_socket.recvfrom(1024)
                    if self.callback:
                        self.callback(data.decode(), server_address)
                    else:
                        print(f"응답 받음: {data.decode()} from {server_address}")
                except socket.timeout:
                    # 타임아웃은 오류가 아니므로 계속 실행
                    continue
                except socket.error as e:
                    if not self.running:
                        # 이미 종료 중이면 메시지 출력하지 않음
                        break
                    print(f"응답 수신 중 소켓 오류: {e}")
                    break
                    
            except Exception as e:
                if not self.running:
                    # 정상적으로 종료 중이면 오류 메시지 출력하지 않음
                    break
                print(f"응답 수신 중 오류: {e}")
                break
            
            
            
    def start_listening(self):
        """클라이언트의 응답 수신을 위한 스레드를 시작합니다."""
        if self.client_thread is not None and self.client_thread.is_alive():
            print("클라이언트는 이미 실행 중입니다.")
            return False  # 이미 스레드가 실행 중이면 새로 시작하지 않음
        
        if self.client_socket is None:
            print("연결이 설정되지 않았습니다. connect()를 먼저 호출하세요.")
            return False

        try:
            self.running = True
            self.client_thread = threading.Thread(target=self.listen_for_responses, daemon=True)
            self.client_thread.start()
            print("클라이언트가 응답을 수신합니다...")
            return True
        except Exception as e:
            print(f"클라이언트 응답 수신 스레드 시작 실패: {e}")
            return False

    def stop(self):
        """클라이언트를 종료하고 스레드를 안전하게 종료합니다."""
        if self.running:
            self.running = False
            if self.client_thread:
                self.client_thread.join()  # 응답 수신 스레드 종료
            self.client_socket.close()
            print("클라이언트가 종료되었습니다.")
            return True
        else:
            print("클라이언트는 이미 종료되었습니다.")
            return False
        
        
    def is_running(self) -> bool:
        """서버가 실행 중인지 확인합니다."""
        return self.running