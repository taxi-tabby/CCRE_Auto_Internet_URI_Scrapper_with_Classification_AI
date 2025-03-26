from urllib.parse import urljoin, urlparse
import os
from .regexp import get_uri_pattern



def extract_links_from_xml(http_body, base_url):
    """
    Extracts all URI-like patterns from the given content and returns them as a list of dictionaries.

    Args:
        http_body (str): The full HTTP body containing the XML or other content.
        base_url (str): The base URL to resolve relative links.

    Returns:
        list: A list of dictionaries containing URLs and their extensions (if any).
    """
    try:
        links = []

        # Extract URI-like patterns using a separate function
        uri_pattern = get_uri_pattern()
        matches = uri_pattern.findall(http_body)

        for match in matches:
            # Resolve relative URLs to absolute URLs
            absolute_url = urljoin(base_url, match.strip())
            # Extract file extension if present
            path = urlparse(absolute_url).path
            ext = os.path.splitext(path)[1][1:]  # Get extension without the dot
            if ext:
                links.append({"url": absolute_url, "ext": ext})
            else:
                links.append({"url": absolute_url, "ext": None})

        return links
    except Exception as e:
        print(f"Error extracting URIs: {e}")
        return []