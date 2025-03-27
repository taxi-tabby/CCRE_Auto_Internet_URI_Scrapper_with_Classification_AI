from urllib.parse import urljoin, urlparse
import os
from .regexp import get_uri_pattern
from collections import defaultdict




def classify_uris(text: str):
    """
    Extracts and classifies URI-like strings from the input text into a single list with type attributes.

    Args:
        text (str): The input text containing URI-like strings.

    Returns:
        list: A list of dictionaries where each dictionary contains a URI and its type.
    """
    uri_pattern = get_uri_pattern()
    matches = uri_pattern.findall(text)

    # List to store classified URIs with their types
    classified_uris = []

    for match in matches:
        if match.startswith(("http://", "https://")):
            uri_type = "http"
        elif match.startswith("ftp://"):
            uri_type = "ftp"
        elif match.startswith("file://"):
            uri_type = "file"
        elif match.startswith("mailto:"):
            uri_type = "mailto"
        elif match.startswith(("ws://", "wss://")):
            uri_type = "websocket"
        elif match.startswith("www."):
            uri_type = "www"
        elif match.startswith("data:"):
            uri_type = "data_uri"
        elif match.startswith("./") or match.startswith("../"):
            uri_type = "relative_path"
        elif match.startswith("/"):
            uri_type = "absolute_path"
        elif "@" in match:
            uri_type = "email"
        else:
            uri_type = "domain"

        classified_uris.append({"uri": match, "type": uri_type})

    return classified_uris









def extract_links_from_xml(http_body: str):
    """
    Extracts all URI-like patterns from the given content and returns them as a list of dictionaries.

    Args:
        http_body (str): The full HTTP body containing the XML or other content.

    Returns:
        list: A list of dictionaries containing URLs and their extensions (if any).
    """
    try:
        links = []

        # Extract URI-like patterns using a separate function
        uri_pattern = get_uri_pattern()
        matches = uri_pattern.findall(http_body)

        for match in matches:
            # Extract file extension if present
            path = urlparse(match.strip()).path
            ext = os.path.splitext(path)[1][1:]  # Get extension without the dot
            if ext:
                links.append({"url": match.strip(), "ext": ext})
            else:
                links.append({"url": match.strip(), "ext": None})

        return links
    except Exception as e:
        print(f"Error extracting URIs: {e}")
        return []