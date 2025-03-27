import re

import re

def get_uri_pattern():
    """
    Returns a compiled regular expression pattern to match various types of URI-like strings.
    """
    # 새로운 정규식 패턴: 모든 프로토콜 지원하는 URI 추출
    pattern = r'([a-zA-Z][a-zA-Z\d+\-.]*://[^\s">]+)'  # 단순화된 패턴
    return re.compile(pattern)
