import re




# def get_uri_pattern():
#     pattern = r'(https?://[^\s\'"<>]+|//[^\s\'"<>]+|[^\'"\s<>]+(?=\s*[\)";]))'
#     return re.compile(pattern)



def get_uri_pattern():
    """
    Returns a compiled regular expression pattern to match only absolute URIs
    within JavaScript and CSS code. It excludes relative URIs and handles `url()` in CSS.
    """
    # 절대 URI만 추출하는 정규식 패턴 (url() 내에서도 처리)
    pattern = r'(?i)(?:https?|ftp):\/\/(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?:\/[^\s"<>)]*)'

    # 컴파일하여 반환
    return re.compile(pattern)


# def get_uri_pattern():
#     """
#     Returns a compiled regular expression pattern to match only valid URI-like strings.
#     This includes absolute URIs (http, https, ftp) and relative URIs (starting with '/', './', or '../').
#     """
#     pattern = r'(?i)\b(?:https?|ftp):\/\/(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?:\/[^\s"<>]*)?|\b(?:\/(?:[a-zA-Z0-9-._~:/?#[\]@!$&\'()*+,;=]+|\.[a-zA-Z0-9-._~:/?#[\]@!$&\'()*+,;=]+)+|\.\.\/[a-zA-Z0-9-._~:/?#[\]@!$&\'()*+,;=]+(?:\/[^\s"<>]*)?)'
#     return re.compile(pattern)