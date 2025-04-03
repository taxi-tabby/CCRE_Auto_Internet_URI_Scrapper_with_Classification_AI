import aiohttp
import re
from urllib.parse import urlparse

import requests


async def fetch_robots_txt(path: str) -> str:
    """
    주어진 URL에서 robots.txt 내용을 가져옵니다. (비동기 버전)

    Args:
        path (str): 로봇이 접근하려는 경로를 포함한 URL (예: "https://example.com/somepath").

    Returns:
        str: robots.txt 내용. 가져올 수 없으면 빈 문자열 반환.
    """
    base_url = f"{urlparse(path).scheme}://{urlparse(path).hostname}"
    robots_url = f"{base_url}/robots.txt"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(robots_url) as response:
                if response.status != 200:
                    return ""  # robots.txt를 가져올 수 없으면 빈 문자열 반환
                return await response.text()
    except Exception:
        return ""  # 오류가 발생하면 빈 문자열 반환

# def fetch_robots_txt(path: str) -> str:
#     """
#     주어진 URL에서 robots.txt 내용을 가져옵니다. (동기 버전)

#     Args:
#         path (str): 로봇이 접근하려는 경로를 포함한 URL (예: "https://example.com/somepath").

#     Returns:
#         str: robots.txt 내용. 가져올 수 없으면 빈 문자열 반환.
#     """
#     base_url = f"{urlparse(path).scheme}://{urlparse(path).hostname}"
#     robots_url = f"{base_url}/robots.txt"

#     try:
#         response = requests.get(robots_url)

#         if response.status_code != 200:
#             return ""  # robots.txt를 가져올 수 없으면 빈 문자열 반환

#         return response.text
#     except Exception:
#         return ""  # 오류가 발생하면 빈 문자열 반환
    
    
def check_robot_permission_from_rules(robot_name: str, ruleset: str, path: str) -> bool:
    """
    주어진 ruleset과 robot_name을 사용하여 robots.txt 규칙을 체크합니다.

    Args:
        robot_name (str): 체크할 로봇의 이름 (예: "Googlebot").
        ruleset (str): robots.txt 내용.
        path (str): 로봇이 접근하려는 경로 (예: "/somepath").

    Returns:
        bool: 로봇이 해당 경로에 접근할 수 있으면 True, 그렇지 않으면 False.
    """
    if not ruleset:
        return True  # ruleset이 없으면 기본적으로 접근 가능

    # 로봇 이름과 path에 대한 규칙 찾기
    user_agent_pattern = re.compile(r"User-agent:\s*(\S+)", re.IGNORECASE)
    allow_pattern = re.compile(r"Allow:\s*(\S.*)", re.IGNORECASE)
    deny_pattern = re.compile(r"Deny:\s*(\S.*)", re.IGNORECASE)

    user_agents = []
    allows = []
    denies = []

    # user_agent와 allow/deny 규칙을 추출
    current_user_agent = None
    for line in ruleset.splitlines():
        line = line.strip()
        # 로봇 이름에 해당하는 User-agent 찾기
        user_agent_match = user_agent_pattern.match(line)
        if user_agent_match:
            current_user_agent = user_agent_match.group(1).lower()

        if current_user_agent:
            # Allow 및 Deny 규칙 추출
            if allow_pattern.match(line):
                allows.append((current_user_agent, line.split(":", 1)[1].strip()))
            if deny_pattern.match(line):
                denies.append((current_user_agent, line.split(":", 1)[1].strip()))

        # '*'는 모든 로봇에 대한 규칙
        if current_user_agent == "*":
            if allow_pattern.match(line):
                allows.append((current_user_agent, line.split(":", 1)[1].strip()))
            if deny_pattern.match(line):
                denies.append((current_user_agent, line.split(":", 1)[1].strip()))

    # 특정 로봇에 대해 allow/deny 규칙 체크
    for user_agent, deny_path in denies:
        if user_agent == robot_name.lower() or user_agent == "*":
            if path.startswith(deny_path):
                return False  # Deny 규칙이 있으면 False 반환
            elif deny_path.endswith("*") and path.startswith(deny_path[:-1]):
                return False  # `/*` 규칙도 처리

    for user_agent, allow_path in allows:
        if user_agent == robot_name.lower() or user_agent == "*":
            if path.startswith(allow_path):
                return True  # Allow 규칙이 있으면 True 반환
            elif allow_path.endswith("*") and path.startswith(allow_path[:-1]):
                return True  # `/*` 규칙도 처리

    return True  # 규칙이 없으면 기본적으로 True 반환
