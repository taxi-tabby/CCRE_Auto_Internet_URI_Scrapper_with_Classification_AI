import re

def normalize_uri_path(uri: str) -> str:
    """
    Normalize the URI path by replacing multiple consecutive slashes with a single slash.

    Args:
        uri (str): The input URI.

    Returns:
        str: The normalized URI with single slashes.
    """
    return re.sub(r'/{2,}', '/', uri)