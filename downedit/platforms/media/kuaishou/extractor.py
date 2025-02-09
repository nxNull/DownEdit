
import re
import secrets

__all__ = [
    "extract_user_id",
    "extract_live_url_segment",
    "extract_url_segment"
]


def extract_user_id(input_string: str) -> str:
    """
    Extracts the user ID from a KuaiShou profile URL or direct user ID input.

    Args:
        input_string (str): The input string, which can be a KuaiShou profile URL or a user ID.

    Returns:
        str: The extracted user ID, or an empty string if no valid ID is found.
    """
    user_id_pattern = r"(?:https?://(?:www|live)\.kuaishou\.com/profile/)?([a-zA-Z0-9]+)"
    match = re.match(user_id_pattern, input_string.strip())
    return match.group(1) if match else ""


def extract_live_url_segment(url: str) -> str:
    """
    Extracts the specific part of the URL and converts the slashes to underscores.

    Args:
        url (str): The input URL to extract the segment from.

    Returns:
        str: The extracted and converted segment.
    """
    pattern = r"/upic/([\d/]+/[a-zA-Z0-9_]+)"
    match = re.search(pattern, url)

    if match:
        extracted_part = match.group(1)
        converted_part = extracted_part.replace("/", "_")
        return converted_part
    else:
        return secrets.token_hex(16)


def extract_url_segment(url: str) -> str:
    """
    Extracts the specific part of the URL and converts the slashes to underscores.

    Args:
        url (str): The input URL to extract the segment from.

    Returns:
        str: The extracted and converted segment.
    """
    pattern = r"/ksc2/(.+?)\.mp4\?.+"
    match = re.search(pattern, url)

    if match:
        extracted_part = match.group(1).replace('/', '_')
        return extracted_part
    else:
        return secrets.token_hex(16)
