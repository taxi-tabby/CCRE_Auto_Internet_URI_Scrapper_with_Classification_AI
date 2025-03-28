import socket
import ssl
from urllib.parse import urlparse, urljoin
from typing import Dict, Union
import random

def _get_random_user_agent() -> str:
    """
    다양한 종류의 User-Agent 문자열 중 하나를 랜덤으로 생성하여 반환합니다.

    Returns:
        str: 랜덤 User-Agent 문자열
    """

    # 운영체제 목록
    os_list = [
        "Windows NT 10.0; Win64; x64",
        "Windows NT 6.1; Win64; x64",
        "Windows NT 6.0; Win64; x64",
        "Macintosh; Intel Mac OS X 10_15_7",
        "Macintosh; Intel Mac OS X 10_14_6",
        "Macintosh; Intel Mac OS X 10_13_6",
        "X11; Ubuntu; Linux x86_64",
        "Linux; Android 10",
        "iPhone; CPU iPhone OS 14_0 like Mac OS X",
        "iPad; CPU OS 14_0 like Mac OS X"
    ]
    
    # 브라우저 목록
    browser_list = [
        ("Chrome", 58, 100),
        ("Chrome", 60, 110),
        ("Chrome", 80, 120),
        ("Firefox", 70, 110),
        ("Firefox", 80, 120),
        ("Safari", 11, 14),
        ("Edge", 85, 100),
        ("Edge", 90, 105)
    ]
    
    # 엔진 목록 (렌더링 엔진)
    engine_list = [
        "AppleWebKit/537.36",  # Chrome, Safari
        "Gecko/20100101",      # Firefox
        "Edge/91.0.864.59",    # Edge
    ]
    
    # 랜덤으로 OS, 브라우저, 엔진을 선택
    os = random.choice(os_list)
    browser, min_version, max_version = random.choice(browser_list)
    engine = random.choice(engine_list)

    # 브라우저 버전 랜덤 생성
    version = random.randint(min_version, max_version)
    
    # User-Agent 문자열 생성
    if browser == "Chrome":
        user_agent = f"Mozilla/5.0 ({os}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.{random.randint(1000, 9999)}.{random.randint(100, 999)} Safari/537.36"
    elif browser == "Firefox":
        user_agent = f"Mozilla/5.0 ({os}) Gecko/20100101 Firefox/{version}.0"
    elif browser == "Safari":
        user_agent = f"Mozilla/5.0 ({os}) AppleWebKit/{random.randint(500, 537)}.36 (KHTML, like Gecko) Safari/{version}.{random.randint(100, 999)}"
    elif browser == "Edge":
        user_agent = f"Mozilla/5.0 ({os}) AppleWebKit/537.36 (KHTML, like Gecko) {engine} Safari/537.36 Edge/{version}.0"

    return user_agent




def send_http_request(url: str, port: int = 80, headers: Dict[str, str] = None, cookies: Dict[str, str] = None, is_https: bool = False) -> bytes:
    """
    원시 소켓을 사용하여 HTTP GET 요청을 보냅니다. 인증 헤더를 자동으로 처리.

    Args:
        url (str): 요청할 URL
        port (int): 포트 번호 (기본값: 80)
        headers (dict): 추가할 HTTP 헤더 (기본값: None)
        cookies (dict): 쿠키 (기본값: None)
        is_https (bool): HTTPS 사용 여부 (기본값: False)

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
        "User-Agent": _get_random_user_agent(),
    }

    # 사용자 정의 헤더 병합 (기존 값 업데이트)
    if headers:
        default_headers.update(headers)

    # 쿠키 헤더 추가
    if cookies:
        cookie_header = "; ".join([f"{key}={value}" for key, value in cookies.items()])
        default_headers["Cookie"] = cookie_header

    # HTTP GET 요청 생성
    header_lines = "\r\n".join(f"{key}: {value}" for key, value in default_headers.items())
    request = f"GET {path} HTTP/1.1\r\n{header_lines}\r\n\r\n"

    # 소켓 생성 및 서버 연결
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if is_https:
        # SSLContext 생성하여 TLS 버전 설정 (기본 SSLContext 사용)
        context = ssl.create_default_context()

        # 암호화 방식을 기본값으로 설정 (서버와의 호환성 증가)
        context.set_ciphers("DEFAULT")  # 기본 제공 암호화 방식 사용

        # SSLv2, SSLv3 비활성화
        context.options |= ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3
        
        # SSL 연결 설정 시 server_hostname을 추가로 설정
        s = context.wrap_socket(s, server_hostname=host)  # server_hostname을 추가해야 함

    s.settimeout(5)
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

def fetch_with_redirects(url: str, max_redirects: int = 5, headers: Dict[str, str] = None, cookies: Dict[str, str] = None) -> Dict[str, Union[Dict[str, str], str, int]]:
    """
    리다이렉션을 추적하며 최종 응답을 가져오는 함수.

    Args:
        url (str): 요청할 URL
        max_redirects (int): 최대 리다이렉션 횟수
        headers (dict): 추가할 HTTP 헤더 (기본값: None)
        cookies (dict): 쿠키 (기본값: None)

    Returns:
        dict: 최종 응답 데이터 (헤더, 본문, 상태 코드 포함)
        -   "headers"
        -   "body"
        -   "status_code"
        -   "status_message"
        -   "http_version"
    """
    redirects = 0
    current_cookies = cookies or {}
    current_protocol = urlparse(url).scheme

    while redirects < max_redirects:
        # 현재 URL에 대해 HTTP/HTTPS 여부를 확인
        is_https = current_protocol == "https"
        parsed_url = urlparse(url)
        port = 443 if is_https else 80
        
        # 요청 보내기
        response = send_http_request(url, headers=headers, cookies=current_cookies, port=port, is_https=is_https)
        parsed_response = parse_http_response(response)

        print(f"Redirect {redirects + 1}: Status code {parsed_response['status_code']}, Location: {parsed_response['headers'].get('Location')}")

        # 상태 코드가 301 또는 302인 경우 리다이렉션 처리
        if parsed_response["status_code"] in (301, 302):
            location = parsed_response["headers"].get("Location")
            if not location:
                raise Exception("Redirect response missing 'Location' header")

            # 상대경로로 오는 경우 절대경로로 변환
            if not location.startswith("http"):
                location = urljoin(url, location)  # 상대 경로를 절대 경로로 변환

            url = location
            redirects += 1

            # 새로운 쿠키 업데이트
            cookies_header = parsed_response["headers"].get("Set-Cookie")
            if cookies_header:
                # 쿠키 파싱 및 현재 쿠키에 추가
                for cookie in cookies_header.split(","):
                    cookie_parts = cookie.split(";")
                    cookie_name_value = cookie_parts[0].strip().split("=")
                    if len(cookie_name_value) == 2:
                        current_cookies[cookie_name_value[0]] = cookie_name_value[1]
                
        else:
            # 리다이렉션이 아닌 경우 최종 응답 반환
            return parsed_response

    raise Exception("Too many redirects")




















# def send_http_request(url: str, port: int = 80, headers: Dict[str, str] = None, cookies: Dict[str, str] = None, is_https: bool = False) -> bytes:
#     """
#     원시 소켓을 사용하여 HTTP GET 요청을 보냅니다. 인증 헤더를 자동으로 처리.

#     Args:
#         url (str): 요청할 URL
#         port (int): 포트 번호 (기본값: 80)
#         headers (dict): 추가할 HTTP 헤더 (기본값: None)
#         cookies (dict): 쿠키 (기본값: None)
#         is_https (bool): HTTPS 사용 여부 (기본값: False)

#     Returns:
#         bytes: 서버의 응답 데이터
#     """
#     parsed_url = urlparse(url)
#     host = parsed_url.hostname
#     path = parsed_url.path if parsed_url.path else "/"

#     # 기본 헤더 설정
#     default_headers = {
#         "Host": host,
#         "Connection": "close",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",  # 일반적인 User-Agent
#     }

#     # 사용자 정의 헤더 병합 (기존 값 업데이트)
#     if headers:
#         default_headers.update(headers)

#     # 쿠키 헤더 추가
#     if cookies:
#         cookie_header = "; ".join([f"{key}={value}" for key, value in cookies.items()])
#         default_headers["Cookie"] = cookie_header

#     # HTTP GET 요청 생성
#     header_lines = "\r\n".join(f"{key}: {value}" for key, value in default_headers.items())
#     request = f"GET {path} HTTP/1.1\r\n{header_lines}\r\n\r\n"

#     # 소켓 생성 및 서버 연결
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     if is_https:
#         # SSLContext 생성하여 TLS 버전 설정 (기본 SSLContext 사용)
#         context = ssl.create_default_context()

#         # 암호화 방식을 기본값으로 설정 (서버와의 호환성 증가)
#         context.set_ciphers("DEFAULT")  # 기본 제공 암호화 방식 사용

#         # SSLv2, SSLv3 비활성화
#         context.options |= ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3
#         s = context.wrap_socket(s, server_hostname=host)

#     s.settimeout(5)
#     s.connect((host, port))

#     # 요청 전송
#     s.sendall(request.encode())

#     # 응답 받기
#     response = b""
#     while True:
#         data = s.recv(4096)
#         if not data:
#             break
#         response += data

#     s.close()
#     return response

# def parse_http_response(response: bytes) -> Dict[str, Union[Dict[str, str], str, int]]:
#     """
#     HTTP 응답을 파싱하여 헤더와 본문을 분리합니다.

#     Args:
#         response (bytes): 서버의 응답 데이터

#     Returns:
#         dict: 파싱된 응답 데이터
#     """
#     headers, body = response.split(b"\r\n\r\n", 1)

#     # 헤더 파싱
#     headers_dict = {}
#     header_lines = headers.decode().split("\r\n")
#     status_line = header_lines[0]  # 상태 라인 (예: HTTP/1.1 200 OK)
#     for line in header_lines[1:]:
#         if ": " in line:
#             key, value = line.split(": ", 1)
#             headers_dict[key] = value

#     # 본문 반환
#     body = body.decode("utf-8", errors="ignore")  # 본문을 문자열로 변환

#     return {
#         "headers": headers_dict,
#         "body": body,
#         "status_code": int(status_line.split(" ")[1]),  # 상태 코드 추출
#         "status_message": " ".join(status_line.split(" ")[2:]),  # 상태 메시지 추출
#         "http_version": status_line.split(" ")[0],  # HTTP 버전 추출
#     }

# def fetch_with_redirects(url: str, max_redirects: int = 5, headers: Dict[str, str] = None, cookies: Dict[str, str] = None) -> Dict[str, Union[Dict[str, str], str, int]]:
#     """
#     리다이렉션을 추적하며 최종 응답을 가져오는 함수.

#     Args:
#         url (str): 요청할 URL
#         max_redirects (int): 최대 리다이렉션 횟수
#         headers (dict): 추가할 HTTP 헤더 (기본값: None)
#         cookies (dict): 쿠키 (기본값: None)

#     Returns:
#         dict: 최종 응답 데이터 (헤더, 본문, 상태 코드 포함)
#         -   "headers"
#         -   "body"
#         -   "status_code"
#         -   "status_message"
#         -   "http_version"
#     """
#     redirects = 0
#     current_cookies = cookies or {}
#     current_protocol = urlparse(url).scheme

#     while redirects < max_redirects:
#         # 현재 URL에 대해 HTTP/HTTPS 여부를 확인
#         is_https = current_protocol == "https"
#         parsed_url = urlparse(url)
#         port = 443 if is_https else 80
        
#         # 요청 보내기
#         response = send_http_request(url, headers=headers, cookies=current_cookies, port=port, is_https=is_https)
#         parsed_response = parse_http_response(response)

#         # print(f"Redirect {redirects + 1}: Status code {parsed_response['status_code']}, Location: {parsed_response['headers'].get('Location')}")

#         # 상태 코드가 301 또는 302인 경우 리다이렉션 처리
#         if parsed_response["status_code"] in (301, 302):
#             location = parsed_response["headers"].get("Location")
#             if not location:
#                 raise Exception("Redirect response missing 'Location' header")

#             # 상대경로로 오는 경우 절대경로로 변환
#             if not location.startswith("http"):
#                 location = urljoin(url, location)  # 상대 경로를 절대 경로로 변환

#             url = location
#             redirects += 1

#             # 새로운 쿠키 업데이트
#             cookies_header = parsed_response["headers"].get("Set-Cookie")
#             if cookies_header:
#                 # 쿠키 파싱 및 현재 쿠키에 추가
#                 for cookie in cookies_header.split(","):
#                     cookie_parts = cookie.split(";")
#                     cookie_name_value = cookie_parts[0].strip().split("=")
#                     if len(cookie_name_value) == 2:
#                         current_cookies[cookie_name_value[0]] = cookie_name_value[1]
                
#         else:
#             # 리다이렉션이 아닌 경우 최종 응답 반환
#             return parsed_response

#     raise Exception("Too many redirects")

# # # 테스트 실행
# # try:
# #     custom_headers = {"User-Agent": "CCRE_URI_CRAW_CLIENT/1.0"}
# #     initial_cookies = {"session_id": "12345"}
# #     final_response = fetch_with_redirects("http://example.com", headers=custom_headers, cookies=initial_cookies)
# #     print(final_response["body"])
# # except Exception as e:
# #     print(f"Error: {e}")
