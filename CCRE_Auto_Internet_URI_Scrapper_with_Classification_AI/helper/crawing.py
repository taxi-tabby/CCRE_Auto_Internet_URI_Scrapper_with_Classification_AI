import socket

def send_http_request(host, port, request):
    # 소켓 생성
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 서버에 연결
    s.connect((host, port))
    
    # HTTP 요청 전송
    s.sendall(request.encode())
    
    # 응답 받기
    response = b""
    while True:
        data = s.recv(4096)
        if not data:
            break
        response += data
    
    s.close()
    
    return response

def parse_http_response(response):
    # 응답을 헤더와 본문으로 분리
    headers, body = response.split(b"\r\n\r\n", 1)
    
    # 헤더 파싱
    headers_dict = {}
    for line in headers.decode().split("\r\n"):
        if ": " in line:
            key, value = line.split(": ", 1)
            headers_dict[key] = value
    
    # 본문 반환
    body = body.decode('utf-8', errors='ignore')  # 본문을 문자열로 변환
    
    return {
        "headers": headers_dict,
        "body": body
    }

def create_http_get_request(url):
    # URL을 파싱하여 host와 path 구분
    _, rest = url.split("://")
    host, path = rest.split("/", 1) if "/" in rest else (rest, "")
    path = "/" + path if path else "/"
    
    # HTTP GET 요청 문자열 생성
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    return host, request