"""
Utility function for testing rate limiting by making repeated requests to a URL.
"""

import time
import random
from typing import Optional, Dict, Any
from urllib.parse import urlencode


def make_requests_until_blocked(
    url: str,
    period: float = 1.0,
    max_attempts: Optional[int] = None,
    randomize_params: bool = True,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Makes random requests to a URL every X seconds until blocked.
    
    Args:
        url: The target URL to make requests to
        period: Time interval in seconds between requests (default: 1.0)
        max_attempts: Maximum number of attempts before stopping (None = unlimited)
        randomize_params: Whether to add random query parameters to requests
        verbose: Whether to print progress information
    
    Returns:
        Dictionary containing:
            - success_count: Number of successful requests
            - total_attempts: Total number of requests made
            - blocked: Whether the requests were blocked
            - status_code: Final HTTP status code received
            - error_message: Error message if any
    """
    try:
        import requests
    except ImportError:
        raise ImportError("requests library is required. Install it with: pip install requests")
    
    success_count = 0
    total_attempts = 0
    blocked = False
    final_status = None
    error_message = None
    
    # List of user agents to randomize
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15",
    ]
    
    if verbose:
        print(f"Starting requests to {url}")
        print(f"Period: {period} seconds")
        print("-" * 50)
    
    try:
        while True:
            # Check max attempts limit
            if max_attempts is not None and total_attempts >= max_attempts:
                if verbose:
                    print(f"\nReached maximum attempts limit: {max_attempts}")
                break
            
            total_attempts += 1
            
            # Prepare request with randomization
            headers = {
                "User-Agent": random.choice(user_agents),
                "Accept": "text/html,application/json,*/*",
            }
            
            # Add random query parameters if enabled
            request_url = url
            if randomize_params:
                params = {
                    "timestamp": str(time.time()),
                    "rand": str(random.randint(1000, 9999)),
                }
                separator = "&" if "?" in url else "?"
                request_url = f"{url}{separator}{urlencode(params)}"
            
            try:
                # Make the request
                response = requests.get(
                    request_url,
                    headers=headers,
                    timeout=10
                )
                
                final_status = response.status_code
                
                # Check if request was blocked
                if response.status_code in [429, 403, 503]:
                    blocked = True
                    error_message = f"Blocked with status code {response.status_code}"
                    if verbose:
                        print(f"\n🚫 Request #{total_attempts}: BLOCKED - Status {response.status_code}")
                    break
                elif response.status_code >= 400:
                    blocked = True
                    error_message = f"Error status code {response.status_code}"
                    if verbose:
                        print(f"\n❌ Request #{total_attempts}: ERROR - Status {response.status_code}")
                    break
                else:
                    success_count += 1
                    if verbose:
                        print(f"✓ Request #{total_attempts}: Success (Status {response.status_code})")
                
            except requests.exceptions.ConnectionError as e:
                blocked = True
                error_message = f"Connection error: {str(e)}"
                if verbose:
                    print(f"\n🚫 Request #{total_attempts}: Connection blocked/refused")
                break
            except requests.exceptions.Timeout:
                blocked = True
                error_message = "Request timeout"
                if verbose:
                    print(f"\n⏱️  Request #{total_attempts}: Timeout (possibly blocked)")
                break
            except requests.exceptions.RequestException as e:
                blocked = True
                error_message = f"Request exception: {str(e)}"
                if verbose:
                    print(f"\n❌ Request #{total_attempts}: Exception - {str(e)}")
                break
            
            # Wait for the specified period before next request
            time.sleep(period)
            
    except KeyboardInterrupt:
        if verbose:
            print("\n\n⚠️  Interrupted by user")
        error_message = "Interrupted by user"
    
    # Prepare result summary
    result = {
        "success_count": success_count,
        "total_attempts": total_attempts,
        "blocked": blocked,
        "status_code": final_status,
        "error_message": error_message,
    }
    
    if verbose:
        print("\n" + "=" * 50)
        print("SUMMARY:")
        print(f"  Total attempts: {total_attempts}")
        print(f"  Successful requests: {success_count}")
        print(f"  Blocked: {'Yes' if blocked else 'No'}")
        if final_status:
            print(f"  Final status code: {final_status}")
        if error_message:
            print(f"  Message: {error_message}")
        print("=" * 50)
    
    return result


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python ddos.py <url> [period_seconds]")
        print("Example: python ddos.py https://example.com 0.5")
        sys.exit(1)
    
    target_url = sys.argv[1]
    period_seconds = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    
    result = make_requests_until_blocked(
        url=target_url,
        period=period_seconds,
        verbose=True
    )

