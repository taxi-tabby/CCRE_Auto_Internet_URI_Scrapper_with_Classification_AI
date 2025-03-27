from urllib.parse import urljoin, urlparse
import os
from .regexp import get_uri_pattern
from collections import defaultdict


def _classify_uri(uri: str):
    """
    Classifies the given URI-like string into its type.

    Args:
        uri (str): The URI to classify.

    Returns:
        str: The type of the URI.
    """
    if uri.startswith(("http://", "https://")):
        return "http"
    elif uri.startswith("ftp://"):
        return "ftp"
    elif uri.startswith("file://"):
        return "file"
    elif uri.startswith("mailto:"):
        return "mailto"
    elif uri.startswith(("ws://", "wss://")):
        return "websocket"
    elif uri.startswith("www."):
        return "www"
    elif uri.startswith("data:"):
        return "data_uri"
    elif uri.startswith("./") or uri.startswith("../"):
        return "relative_path"
    elif uri.startswith("/"):
        return "absolute_path"
    elif "@" in uri:
        return "email"
    else:
        return "domain"

def extract_links_from_xml(http_body: str):
    """
    Extracts all URI-like patterns from the given content and returns them as a list of dictionaries.

    Args:
        http_body (str): The full HTTP body containing the XML or other content.

    Returns:
        list: A list of dictionaries containing URLs, their extensions (if any), and a flag indicating if it's a relative path.
    """
    try:
        links = []

        # Extract URI-like patterns using a separate function
        uri_pattern = get_uri_pattern()
        matches = uri_pattern.findall(http_body)

        for match in matches:
            # Clean the match string and extract the path
            url = match.strip()
            parsed_url = urlparse(url)
            path = parsed_url.path

            # Determine if it's a relative URL
            is_relative = not parsed_url.scheme  # If no scheme, it's relative

            # Extract file extension if present
            ext = os.path.splitext(path)[1][1:]  # Get extension without the dot

            # Classify the URI type
            uri_type = _classify_uri(url)

            # Add URL, extension, relative flag, and URI type to the result
            links.append({
                "url": url,
                "ext": ext if ext else None,
                "is_relative": is_relative,
                "classified": uri_type
            })

        return links
    except Exception as e:
        print(f"Error extracting URIs: {e}")
        return []