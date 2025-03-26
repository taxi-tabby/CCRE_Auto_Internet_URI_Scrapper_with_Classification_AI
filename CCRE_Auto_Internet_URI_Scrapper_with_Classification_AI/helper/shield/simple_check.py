import re
import pyclamd

def check_for_malicious_code(input_string):
    """
    Checks if the given string contains patterns commonly associated with malicious code.

    Args:
        input_string (str): The string to check.

    Returns:
        bool: True if malicious patterns are found, False otherwise.
    """
    # Define patterns commonly associated with malicious code for both Linux and Windows
    malicious_patterns = [
        # Python-specific patterns
        r"(eval\()",
        r"(exec\()",
        r"(os\.system\()",
        r"(subprocess\.Popen\()",
        r"(base64\.b64decode\()",
        r"(importlib\.import_module\()",
        r"(__import__\()",
        r"(open\(.+\))",

        # Linux-specific patterns
        r"(rm\s+-rf\s+/)",
        r"(wget\s+http)",
        r"(curl\s+-O\s+http)",
        r"(chmod\s+\+x\s+)",
        r"(ssh\s+.+@.+)",

        # Windows-specific patterns
        r"(powershell\.exe)",
        r"(cmd\.exe)",
        r"(del\s+/f\s+/q\s+)",
        r"(taskkill\s+/f\s+/im\s+)",
        r"(reg\s+add\s+)",
        r"(reg\s+delete\s+)",
        r"(copy\s+/y\s+)",
        r"(net\s+user\s+.+/add)",
        r"(net\s+localgroup\s+.+/add)"
    ]

    # Combine all patterns into a single regex
    combined_pattern = "|".join(malicious_patterns)

    # Search for malicious patterns in the input string
    if re.search(combined_pattern, input_string, re.IGNORECASE):
        return True
    return False




def check_with_clamd(input_string: str) -> bool:
    """
    Checks if the given string contains malicious content using ClamAV via pyclamd.

    Args:
        input_string (str): The string to check.

    Returns:
        bool: True if malicious content is detected, False otherwise.
    """
    try:
        # Initialize pyclamd
        cd = pyclamd.ClamdNetworkSocket()  # Assumes ClamAV is running on the default network socket
        if not cd.ping():
            raise ConnectionError("ClamAV service is not available.")

        # Scan the input string
        result = cd.scan_stream(input_string.encode('utf-8'))
        if result:
            return True
        
    except Exception as e:
        print(f"Error while scanning with ClamAV: {e}")
        
    return False
