import json
from typing import Optional
def parse_json_string(json_string: str) -> Optional[dict]:
    """
    Parse a JSON string into a Python dictionary.

    Args:
        json_string (str): The JSON string to parse.

    Returns:
        Optional[dict]: The parsed Python dictionary or None if parsing fails.
    """
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON string: {e}")
        return None
