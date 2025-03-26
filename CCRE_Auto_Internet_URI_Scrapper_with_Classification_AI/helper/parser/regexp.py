import re
from collections import defaultdict

def get_uri_pattern():
    """
    Returns a compiled regular expression pattern to match various types of URI-like strings.

    Returns:
        re.Pattern: A compiled regex pattern for matching URIs.
    """
    pattern = r"(https?|ftp|file|mailto|ws|wss):\/\/[^\s\"'>]+|www\.[^\s\"'>]+|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(\/[^\s\"'>]*)?|[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}|data:[a-zA-Z]+\/[a-zA-Z0-9.-]+;base64,[a-zA-Z0-9+/=]+|\.\/[^\s\"'>]+|\/[^\s\"'>]+"
    return re.compile(pattern)



def classify_uris(text):
    """
    Extracts and classifies URI-like strings from the input text into categories.

    Args:
        text (str): The input text containing URI-like strings.

    Returns:
        dict: A dictionary where keys are URI categories and values are lists of matched URIs.
    """
    uri_pattern = get_uri_pattern()
    matches = uri_pattern.findall(text)

    # Categories for classification
    categories = defaultdict(list)

    for match in matches:
        if match.startswith(("http://", "https://")):
            categories["http_https"].append(match)
        elif match.startswith("ftp://"):
            categories["ftp"].append(match)
        elif match.startswith("file://"):
            categories["file"].append(match)
        elif match.startswith("mailto:"):
            categories["mailto"].append(match)
        elif match.startswith(("ws://", "wss://")):
            categories["websocket"].append(match)
        elif match.startswith("www."):
            categories["www"].append(match)
        elif match.startswith("data:"):
            categories["data_uri"].append(match)
        elif match.startswith("./") or match.startswith("../"):
            categories["relative_path"].append(match)
        elif match.startswith("/"):
            categories["absolute_path"].append(match)
        elif "@" in match:
            categories["email"].append(match)
        else:
            categories["domain"].append(match)

    return dict(categories)