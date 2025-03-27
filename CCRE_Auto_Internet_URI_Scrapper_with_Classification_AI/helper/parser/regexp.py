import re



def get_uri_pattern():
    """
    Returns a compiled regular expression pattern to match only valid URI-like strings.
    This includes absolute URIs (http, https, ftp) and relative URIs (starting with '/', './', or '../').
    """
    pattern = r'(?i)\b(?:https?|ftp):\/\/(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?:\/[^\s"<>]*)?|\b(?:\/(?:[a-zA-Z0-9-._~:/?#[\]@!$&\'()*+,;=]+|\.[a-zA-Z0-9-._~:/?#[\]@!$&\'()*+,;=]+)+|\.\.\/[a-zA-Z0-9-._~:/?#[\]@!$&\'()*+,;=]+(?:\/[^\s"<>]*)?)'
    return re.compile(pattern)