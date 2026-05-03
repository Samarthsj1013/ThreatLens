import requests
import base64
from config import VIRUSTOTAL_API_KEY


def lookup_hash(file_hash: str) -> dict:
    """Look up a file hash on VirusTotal."""
    if not VIRUSTOTAL_API_KEY:
        return {"error": "No VirusTotal API key set in .env"}

    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 404:
            return {"error": "Hash not found in VirusTotal database"}
        response.raise_for_status()
        data = response.json()
        return parse_vt_response(data)
    except requests.RequestException as e:
        return {"error": str(e)}


def lookup_url(target_url: str) -> dict:
    """Look up a URL on VirusTotal."""
    if not VIRUSTOTAL_API_KEY:
        return {"error": "No VirusTotal API key set in .env"}

    # VirusTotal requires base64-encoded URL ID
    url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
    url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 404:
            # Submit URL for scanning first
            submit_url = "https://www.virustotal.com/api/v3/urls"
            submit_response = requests.post(
                submit_url,
                headers=headers,
                data={"url": target_url},
                timeout=15
            )
            submit_response.raise_for_status()
            return {"error": "URL submitted for scanning — try again in 30 seconds"}
        response.raise_for_status()
        data = response.json()
        return parse_vt_response(data)
    except requests.RequestException as e:
        return {"error": str(e)}


def parse_vt_response(data: dict) -> dict:
    """Parse VirusTotal API response into clean dict."""
    try:
        attrs = data["data"]["attributes"]
        stats = attrs.get("last_analysis_stats", {})
        results = attrs.get("last_analysis_results", {})

        # Get detections only
        detections = {
            engine: info.get("result", "")
            for engine, info in results.items()
            if info.get("category") in ["malicious", "suspicious"]
        }

        return {
            "malicious": stats.get("malicious", 0),
            "suspicious": stats.get("suspicious", 0),
            "harmless": stats.get("harmless", 0),
            "undetected": stats.get("undetected", 0),
            "total": sum(stats.values()),
            "name": attrs.get("meaningful_name", "") or attrs.get("name", ""),
            "type": attrs.get("type_description", ""),
            "size": attrs.get("size", ""),
            "detections": detections
        }
    except (KeyError, TypeError) as e:
        return {"error": f"Failed to parse VT response: {e}"}