import socket
from urllib.parse import urlparse
from typing import Dict, Union


def send_http_request(url: str, port: int = 80, headers: Dict[str, str] = None) -> bytes:
    """
    원시 소켓을 사용하여 HTTP GET 요청을 보냅니다.

    Args:
        url (str): 요청할 URL
        port (int): 포트 번호 (기본값: 80)
        headers (dict): 추가할 HTTP 헤더 (기본값: None)

    Returns:
        bytes: 서버의 응답 데이터
    """
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    path = parsed_url.path if parsed_url.path else "/"

    # 기본 헤더 설정
    default_headers = {
        "Host": host,
        "Connection": "close",
    }

    # 사용자 정의 헤더 병합 (기존 값 업데이트)
    if headers:
        default_headers.update(headers)

    # HTTP GET 요청 생성
    header_lines = "\r\n".join(f"{key}: {value}" for key, value in default_headers.items())
    request = f"GET {path} HTTP/1.1\r\n{header_lines}\r\n\r\n"

    # 소켓 생성 및 서버 연결
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)  # 타임아웃 설정
    s.connect((host, port))

    # 요청 전송
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


def parse_http_response(response: bytes) -> Dict[str, Union[Dict[str, str], str, int]]:
    """
    HTTP 응답을 파싱하여 헤더와 본문을 분리합니다.

    Args:
        response (bytes): 서버의 응답 데이터

    Returns:
        dict: 파싱된 응답 데이터
    """
    headers, body = response.split(b"\r\n\r\n", 1)

    # 헤더 파싱
    headers_dict = {}
    header_lines = headers.decode().split("\r\n")
    status_line = header_lines[0]  # 상태 라인 (예: HTTP/1.1 200 OK)
    for line in header_lines[1:]:
        if ": " in line:
            key, value = line.split(": ", 1)
            headers_dict[key] = value

    # 본문 반환
    body = body.decode("utf-8", errors="ignore")  # 본문을 문자열로 변환

    return {
        "headers": headers_dict,
        "body": body,
        "status_code": int(status_line.split(" ")[1]),  # 상태 코드 추출
        "status_message": " ".join(status_line.split(" ")[2:]),  # 상태 메시지 추출
        "http_version": status_line.split(" ")[0],  # HTTP 버전 추출
    }


def fetch_with_redirects(url: str, max_redirects: int = 5, headers: Dict[str, str] = None) -> Dict[str, Union[Dict[str, str], str, int]]:
    """
    리다이렉션을 추적하며 최종 응답을 가져오는 함수.

    Args:
        url (str): 요청할 URL
        max_redirects (int): 최대 리다이렉션 횟수
        headers (dict): 추가할 HTTP 헤더 (기본값: None)

    Returns:
        dict: 최종 응답 데이터 (헤더, 본문, 상태 코드 포함)
        -   "headers"
        -   "body"
        -   "status_code"
        -   "status_message"
        -   "http_version"
    """
    redirects = 0
    while redirects < max_redirects:
        response = send_http_request(url, headers=headers)
        parsed_response = parse_http_response(response)

        # 상태 코드가 301 또는 302인 경우 리다이렉션 처리
        if parsed_response["status_code"] in (301, 302):
            location = parsed_response["headers"].get("Location")
            if not location:
                raise Exception("Redirect response missing 'Location' header")
            
            # print(f"Redirected to: {location}")

            # 절대 URL이 아닌 경우 처리
            if not location.startswith("http"):
                parsed_url = urlparse(url)
                location = f"{parsed_url.scheme}://{parsed_url.hostname}{location}"

            url = location
            redirects += 1
        else:
            # 리다이렉션이 아닌 경우 최종 응답 반환
            return parsed_response

    raise Exception("Too many redirects")


# # 테스트 실행
# try:
#     custom_headers = {"User-Agent": "CCRE_URI_CRAW_CLIENT/1.0"}
#     final_response = fetch_with_redirects("http://google.com", headers=custom_headers)
#     print(final_response["body"])
# except Exception as e:
#     print(f"Error: {e}")