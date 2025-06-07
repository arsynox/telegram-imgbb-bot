import requests
import config

async def upload_image_to_imgbb(image_bytes: bytes, server_name: str):
    """Uploads image bytes to the selected imgbb server"""
    server = config.SERVERS.get(server_name)
    if not server:
        return None, "Server not found"

    api_key = server["api_key"]
    url = "https://api.imgbb.com/1/upload"

    payload = {
        "key": api_key,
        "image": image_bytes.encode("base64") if isinstance(image_bytes, str) else image_bytes,
    }

    # Note: imgbb expects base64 encoded image string; We'll convert bytes to base64 string
    import base64
    encoded_img = base64.b64encode(image_bytes).decode("utf-8")

    payload["image"] = encoded_img

    response = requests.post(url, data=payload)
    if response.status_code == 200:
        json_resp = response.json()
        if json_resp.get("success"):
            return json_resp["data"]["url"], None
        else:
            return None, json_resp.get("error", {}).get("message", "Unknown error")
    else:
        return None, f"HTTP Error: {response.status_code}"
