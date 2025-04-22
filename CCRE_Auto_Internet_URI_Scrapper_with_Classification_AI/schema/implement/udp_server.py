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
                # 소켓이 유효한지 확인
                if not self.server_socket:
                    print("소켓이 닫혔습니다. 클라이언트 핸들러를 종료합니다.")
                    break
                    
                # 소켓에 타임아웃 설정
                self.server_socket.settimeout(3)  # 0.5초 타임아웃
                
                try:
                    data, client_address = self.server_socket.recvfrom(1024)
                    client_ip = client_address[0]

                    # 화이트리스트 검사
                    if self.whitelist and client_ip not in self.whitelist:
                        print(f"허용되지 않은 IP: {client_ip}에서 접근을 차단했습니다.")
                        continue

                    # print(f"받은 데이터: {data.decode()} from {client_ip}")

                    # 콜백이 설정되어 있으면 콜백으로 처리
                    if self.callback:
                        self.callback(self.server_socket, data.decode(), client_address)
                    else:
                        # 기본 응답 (콜백이 없을 경우)
                        response = "There is no callback function."
                        self.server_socket.sendto(response.encode(), client_address)
                        
                except socket.timeout:
                    # 타임아웃은 오류가 아니므로 계속 실행
                    continue
                except socket.error as e:
                    # 소켓 오류 처리
                    if not self.running:
                        # 이미 서버 종료 중이면 종료
                        print("UDP Socket server handler says: Server is shutting down.")
                        break
                    
                    print(f"UDPServer socket err: {e}")
                    break
                    
            except Exception as e:
                if not self.running:
                    # 서버가 정상적으로 종료 중이면 오류 메시지 출력하지 않음
                    break
                print(f"UDPServer client process err: {e}")
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
            if not self.running:
                return False
                
            # 상태 먼저 업데이트
            self.running = False
            
            # 소켓 안전하게 닫기
            if self.server_socket:
                try:
                    # Windows에서는 바인딩된 소켓을 닫기 전에 shutdown이 필요할 수 있음
                    self.server_socket.shutdown(socket.SHUT_RDWR)
                except (socket.error, OSError):
                    # 이미 닫혔거나 오류 상태일 수 있음
                    pass
                    
                try:
                    self.server_socket.close()
                except (socket.error, OSError):
                    pass
                    
                self.server_socket = None
                
            # 스레드 안전하게 종료
            if self.server_thread and self.server_thread.is_alive():
                # 짧은 대기 시간으로 시도
                self.server_thread.join(timeout=2.0)
                
                # 스레드가 여전히 실행 중인지 확인
                if self.server_thread.is_alive():
                    print("경고: 서버 스레드를 정상적으로 종료할 수 없습니다.")
                    # 여기서 더 강력한 종료 방법을 사용할 수 있지만 권장되지 않음
                
            return True
                
            
    def is_running(self) -> bool:
        """서버가 실행 중인지 확인합니다."""
        return self.running
    
    
    def send_to_client(self, message: str, client_address: Tuple[str, int]) -> bool:
        """특정 클라이언트에게 메시지를 전송합니다.
        
        Args:
            message: 전송할 메시지
            client_address: (IP, 포트) 형태의 클라이언트 주소
            
        Returns:
            bool: 전송 성공 여부
        """
        if not self.running or not self.server_socket:
            print("서버가 실행 중이 아닙니다.")
            return False
            
        try:
            self.server_socket.sendto(message.encode(), client_address)
            print(f"메시지 전송 완료: {message} to {client_address[0]}:{client_address[1]}")
            return True
        except Exception as e:
            print(f"메시지 전송 실패: {e}")
            return False



    def broadcast(self, message: str, clients: list = None) -> bool:
        """모든 클라이언트 또는 지정된 클라이언트 목록에 메시지를 전송합니다.
        
        Args:
            message: 전송할 메시지
            clients: (IP, 포트) 튜플의 목록, None이면 화이트리스트 사용
            
        Returns:
            bool: 적어도 하나의 클라이언트에게 전송 성공 여부
        """
        if not self.running or not self.server_socket:
            print("서버가 실행 중이 아닙니다.")
            return False
            
        # 클라이언트 목록이 제공되지 않으면 화이트리스트 사용
        target_clients = clients if clients else [(ip, self.port) for ip in self.whitelist]
        if not target_clients:
            print("전송할 클라이언트가 없습니다.")
            return False
            
        success = False
        for client in target_clients:
            try:
                self.server_socket.sendto(message.encode(), client)
                print(f"브로드캐스트 메시지 전송: {message} to {client[0]}:{client[1]}")
                success = True
            except Exception as e:
                print(f"클라이언트 {client[0]}:{client[1]}에 전송 실패: {e}")
                
        return success
    