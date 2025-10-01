"""Utility function for pinging URLs."""
import time
import urllib.request
import urllib.error
from typing import Dict, Any


def ping_url(url: str, timeout: int = 10) -> Dict[str, Any]:
    """
    Ping a URL by making an HTTP GET request.
    
    Args:
        url: The URL to ping
        timeout: Request timeout in seconds (default: 10)
        
    Returns:
        Dictionary with status_code and response_time_ms
        
    Raises:
        urllib.error.URLError: If the request fails
    """
    start_time = time.time()
    
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'AWS-Lambda-URL-Pinger/1.0'}
        )
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            status_code = response.getcode()
            response_time_ms = int((time.time() - start_time) * 1000)
            
            return {
                'status_code': status_code,
                'response_time_ms': response_time_ms
            }
            
    except urllib.error.HTTPError as e:
        # HTTP error (4xx, 5xx), but we got a response
        response_time_ms = int((time.time() - start_time) * 1000)
        return {
            'status_code': e.code,
            'response_time_ms': response_time_ms
        }
        
    except urllib.error.URLError as e:
        # Connection error, DNS error, etc.
        response_time_ms = int((time.time() - start_time) * 1000)
        raise Exception(f"Failed to connect to {url}: {str(e.reason)}")
        
    except Exception as e:
        raise Exception(f"Unexpected error pinging {url}: {str(e)}")

