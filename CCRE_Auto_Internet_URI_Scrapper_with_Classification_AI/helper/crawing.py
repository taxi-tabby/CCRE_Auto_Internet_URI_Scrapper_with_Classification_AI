import socket
import ssl
import time
from urllib.parse import urlparse, urljoin
import random
from typing import Dict, Union

import requests





def get_random_user_agent() -> str:
    """
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












def send_http_request(
    url: str,
    headers: Dict[str, str] = None,
    cookies: Dict[str, str] = None,
    timeout: int = 2  # 타임아웃을 2초로 설정
) -> Dict[str, Union[Dict[str, str], bytes]]:
    """
    HTTP GET 요청을 보냅니다. 요청에 대한 헤더와 본문을 반환합니다.

    Args:
        url (str): 요청할 URL
        headers (dict): 추가할 HTTP 헤더 (기본값: None)
        cookies (dict): 쿠키 (기본값: None)
        timeout (int): 요청 타임아웃 시간 (기본값: 2초)

    Returns:
        dict: 서버의 응답 데이터 (헤더와 본문 포함)
            - "headers": 응답 헤더
            - "body": 응답 본문
    """
    # URL 확인 및 수정: 상대 경로가 있을 경우 절대 경로로 변환
    parsed_url = urlparse(url)

    # Scheme이 없으면 'https://'로 기본 설정
    if not parsed_url.scheme:
        url = "https://" + url  # 기본 HTTPS로 변경
        parsed_url = urlparse(url)

    # 호스트가 없으면 잘못된 URL이므로 이를 수정해야 함
    if not parsed_url.hostname:
        raise ValueError(f"Invalid URL: {url}")

    host = parsed_url.hostname

    # 기본 헤더 설정
    default_headers = {
        "Host": host,
        "Connection": "close",
        "User-Agent": get_random_user_agent()
    }

    # 사용자 정의 헤더 병합
    if headers:
        default_headers.update(headers)

    # 쿠키 헤더 추가
    if cookies:
        cookie_header = "; ".join([f"{key}={str(value)}" for key, value in cookies.items()])
        default_headers["Cookie"] = cookie_header
        cookie_header = "; ".join([f"{key}={str(value)}" for key, value in cookies.items()])
    try:
        # requests를 사용하여 동기식 GET 요청 보내기
        response = requests.get(url, headers=default_headers, cookies=cookies, timeout=timeout)

        # 응답 상태가 200인 경우
        if response.status_code == 200:
            # 응답 본문과 헤더를 반환
            return {
                "headers": dict(response.headers),
                "body": response.content
            }
        else:
            # 응답 상태 코드가 200이 아닌 경우
            raise Exception(f"HTTP request failed with status {response.status_code}")
    
    except requests.Timeout as e:
        return {"error": "TimeoutError", "message": f"Request to {url} timed out.", "details": str(e)}
    
    except requests.RequestException as e:
        return {"error": "ClientError", "message": str(e), "details": str(e)}
    
    except Exception as e:
        return {"error": "RequestError", "message": str(e), "details": str(e)}







def send_http_request_with_socket(
    url: str,
    port: int = 80,
    headers: Dict[str, str] = None,
    cookies: Dict[str, str] = None,
    is_https: bool = False
) -> bytes:
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    path = parsed_url.path if parsed_url.path else "/"

    # 기본 헤더 설정
    default_headers = {
        "Host": host,
        "Connection": "close",
        "User-Agent": get_random_user_agent(),
    }

    # 사용자 정의 헤더 병합
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
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        s = context.wrap_socket(s, server_hostname=host)

    s.settimeout(60)  # 타임아웃 설정

    MAX_RETRIES = 2
    for attempt in range(MAX_RETRIES):
        try:
            s.connect((host, port))
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
        except (socket.timeout, ConnectionAbortedError) as e:
            print(f"Retrying... ({attempt + 1}/{MAX_RETRIES}) - Error: {e}")
            time.sleep(1)
        except Exception as e:
            print(f"Unhandled error: {e}")
            raise
    else:
        print("Max retries reached. Request failed.")
        return b""  # 빈 응답 반환


    

def parse_http_response(response: Dict[str, Union[Dict[str, str], bytes]]) -> Dict[str, Union[Dict[str, str], str, int]]:
    """
    HTTP 응답을 파싱하여 헤더와 본문을 분리합니다.

    Args:
        response (dict): 서버의 응답 데이터 (헤더와 본문 포함)

    Returns:
        dict: 파싱된 응답 데이터
    """
    try:
        # 응답 데이터가 비어있는지 확인
        if not response:
            raise ValueError("Response is empty")

        # body와 headers 존재 여부 확인
        if "body" not in response or "headers" not in response:
            # print(f"Invalid response format: {response}")  # 디버깅용으로 응답을 출력
            raise ValueError("Invalid response format: Missing body or headers")

        # 본문(body)와 헤더(headers) 추출
        body = response["body"]
        headers = response["headers"]
        
        # 상태 코드 추출 (헤더에서 추출)
        status_code = headers.get("status_code", 200)  # 기본 상태 코드 200
        status_message = headers.get("status_message", "OK")
        content_type = headers.get("Content-Type", "unknown")
        http_version = headers.get("http_version", "HTTP/1.1")

        # 본문을 안전하게 디코딩 (UTF-8로 시도, 실패 시 'latin-1'을 사용)
        try:
            body = body.decode("utf-8", errors="ignore")  # UTF-8로 디코딩, 오류는 무시
        except UnicodeDecodeError:
            body = body.decode("latin-1", errors="ignore")  # UTF-8 실패 시 latin-1로 디코딩 시도

        return {
            "headers": headers,
            "body": body,
            "status_code": status_code,
            "status_message": status_message,
            "http_version": http_version,
            "content_type": content_type
        }

    except Exception as e:
        # 오류 발생 시 응답 내용과 함께 출력
        # print(f"Error parsing HTTP response: {e}")
        # print(f"Response content: {response}")
        raise e






async def fetch_with_redirects_async(url: str, max_redirects: int = 5, headers: Dict[str, str] = None, cookies: Dict[str, str] = None) -> Dict[str, Union[Dict[str, str], str, int]]:
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
        -   "content_type"
    """
    redirects = 0
    current_cookies = cookies or {}
    # current_protocol = urlparse(url).scheme

    while redirects < max_redirects:

        # 요청 보내기
        # print('-------- before send_http_request start: ', url)
        response = await send_http_request(url, headers=headers, cookies=current_cookies)
        parsed_response = parse_http_response(response)  # 이제 response는 dict 형태

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
        -   "content_type"
    """
    redirects = 0
    current_cookies = cookies or {}
    # current_protocol = urlparse(url).scheme

    while redirects < max_redirects:

        # 요청 보내기
        # print('-------- before send_http_request start: ', url)
        response = send_http_request(url, headers=headers, cookies=current_cookies)
        parsed_response = parse_http_response(response)  # 이제 response는 dict 형태

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




def socket_fetch_with_redirects(url: str, max_redirects: int = 5, headers: Dict[str, str] = None, cookies: Dict[str, str] = None):
    """
    원시 소켓을 사용하여 리다이렉션을 추적하며 최종 응답을 가져오는 함수.

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
        -   "content_type"
    """
    redirects = 0
    current_cookies = cookies or {}


    while redirects < max_redirects:

        parsed_url = urlparse(url)
        is_https = parsed_url.scheme == "https"
        

        # 요청 보내기
        response = send_http_request_with_socket(url=url, port=(443 if is_https else 80), headers=headers, cookies=current_cookies, is_https=is_https)

        
        

        # 응답 본문이 bytes 타입일 경우 str로 변환
        # if isinstance(response, bytes):
        #     response = response.decode('utf-8')  # 또는 적절한 인코딩 방식으로 변환


        # parse_http_response를 사용하여 응답 파싱
        parsed_response = parse_http_response({
            "headers": {},  # 헤더는 parse_http_response에서 처리
            "body": response
        })




        status_code = parsed_response["status_code"]

        # 상태 코드가 301 또는 302인 경우 리다이렉션 처리
        if status_code in (301, 302):

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