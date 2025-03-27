import json

def parse_json_string(json_string):
    """
    Parse a JSON string into a Python object.

    Args:
        json_string (str): The JSON string to parse.

    Returns:
        object: The parsed Python object (e.g., dict, list).
    """
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON string: {e}")
        return None