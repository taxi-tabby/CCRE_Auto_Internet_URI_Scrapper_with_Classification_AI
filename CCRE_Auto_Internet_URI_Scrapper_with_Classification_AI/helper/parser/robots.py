import re
from urllib.request import urlopen
from urllib.parse import urlparse


def check_robot_permission(path: str, robot_name: str) -> bool:
    """
    주어진 path와 robot_name을 사용하여 robots.txt 규칙을 체크합니다.

    Args:
        path (str): 로봇이 접근하려는 경로를 포함한 URL (예: "https://example.com/somepath").
        robot_name (str): 체크할 로봇의 이름 (예: "Googlebot").

    Returns:
        bool: 로봇이 해당 경로에 접근할 수 있으면 True, 그렇지 않으면 False.
    """
    
    # base_url을 path에서 자동으로 추출
    base_url = f"{urlparse(path).scheme}://{urlparse(path).hostname}"

    # robots.txt 파일을 읽을 URL 생성
    robots_url = f"{base_url}/robots.txt"

    # print(f"Checking robots.txt for {robot_name} at {robots_url}")

    try:
        # robots.txt 파일 가져오기
        response = urlopen(robots_url)
        robots_txt = response.read().decode('utf-8')

        # 로봇 이름과 path에 대한 규칙 찾기
        user_agent_pattern = re.compile(r"User-agent:\s*(\S+)")
        allow_pattern = re.compile(r"Allow:\s*(\S.*)")
        deny_pattern = re.compile(r"Deny:\s*(\S.*)")
        
        user_agents = []
        allows = []
        denies = []

        for line in robots_txt.splitlines():
            # 로봇 이름에 해당하는 User-agent 찾기
            user_agent_match = user_agent_pattern.match(line.strip())
            if user_agent_match:
                current_user_agent = user_agent_match.group(1).lower()
                user_agents.append(current_user_agent)

            # Allow 및 Deny 규칙 추출
            if "Allow:" in line:
                allows.append(line.strip())
            if "Deny:" in line:
                denies.append(line.strip())

        # 특정 로봇에 대해 allow/deny 규칙 체크
        if robot_name.lower() in user_agents:
            for deny in denies:
                if path.startswith(deny.split(":")[1].strip()):
                    return False  # Deny 규칙이 있으면 False 반환

            for allow in allows:
                if path.startswith(allow.split(":")[1].strip()):
                    return True  # Allow 규칙이 있으면 True 반환

        return True  # 규칙이 없으면 기본적으로 True 반환

    except Exception as e:
        # print(f"Error occurred while fetching robots.txt: {e}")
        return False  # 오류가 발생하면 접근이 불가능한 것으로 간주
