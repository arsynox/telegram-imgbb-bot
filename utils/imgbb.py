# utils/imgbb.py

import requests
from config import IMGBB_API_KEYS


class ImgbbUploadError(Exception):
    pass


def upload_image_to_imgbb(server_key, image_bytes):
    """
    Upload image bytes to imgbb using the API key for the given server.
    Returns the image URL on success.
    Raises ImgbbUploadError on failure.
    """
    api_key = IMGBB_API_KEYS.get(server_key)
    if not api_key:
        raise ImgbbUploadError(f"No API key configured for server '{server_key}'")

    url = "https://api.imgbb.com/1/upload"
    files = {
        "image": image_bytes,
    }
    params = {
        "key": api_key,
    }

    try:
        response = requests.post(url, params=params, files=files, timeout=15)
        response.raise_for_status()
        data = response.json()
        if data.get("success"):
            return data["data"]["url"]
        else:
            raise ImgbbUploadError(f"ImgBB API error: {data.get('error', {}).get('message', 'Unknown error')}")
    except requests.RequestException as e:
        raise ImgbbUploadError(f"Request failed: {e}")
