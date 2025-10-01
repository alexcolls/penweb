"""Interactive CLI menu for pentesting utilities."""

import sys
import os
from pathlib import Path
from typing import Optional, List

# Add src directory to path if running from subdirectory
src_dir = Path(__file__).parent.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Load environment variables
try:
    from dotenv import load_dotenv
    # Load .env from project root
    project_root = Path(__file__).parent.parent.parent
    env_path = project_root / ".env"
    load_dotenv(dotenv_path=env_path)
except ImportError:
    pass  # dotenv not installed, will use system environment variables

from cli.banner import print_banner, print_warning, clear_screen
from services.ping import ping_url
from services.clone import clone_website
from services.d2 import make_requests_until_blocked
from services.attempt_login import attempt_credential_combinations
from utils.logger import setup_logging, get_logger
from utils.config import get_output_dir, get_clone_output_dir

# Set up logging
logger = setup_logging('penweb')


class PentestMenu:
    """Interactive menu for pentesting utilities."""

    def __init__(self):
        """Initialize the menu."""
        self.running = True

    def display_main_menu(self):
        """Display the main menu options."""
        print("\n" + "=" * 78)
        print("                          MAIN MENU - Select a Tool")
        print("=" * 78 + "\n")
        print("  \033[92m[1]\033[0m 🌐 Ping URL             - Test URL availability and response time")
        print("  \033[92m[2]\033[0m 📋 Clone Website        - Download website HTML, CSS, and JS files")
        print("  \033[91m[3]\033[0m 💥 DDoS Test (OFFENSIVE) - Test rate limiting with repeated requests")
        print("  \033[91m[4]\033[0m 🔐 Login Test (OFFENSIVE) - Test login security with credential combinations")
        print()
        print("  \033[93m[0]\033[0m 🚪 Exit                 - Quit the application")
        print()
        print("=" * 78)

    def get_choice(self) -> str:
        """Get user's menu choice."""
        try:
            choice = input("\n\033[96mSelect an option [0-4]: \033[0m").strip()
            return choice
        except (EOFError, KeyboardInterrupt):
            print("\n\n\033[93m⚠️  Interrupted by user\033[0m")
            return "0"

    def get_url_input(self, prompt: str = "Enter target URL") -> Optional[str]:
        """Get URL input from user."""
        try:
            url = input(f"\n\033[96m{prompt}: \033[0m").strip()
            
            if not url:
                print("\033[91m✗ Error: URL cannot be empty\033[0m")
                return None
            
            if not url.startswith(('http://', 'https://')):
                print("\033[93m⚠️  Warning: URL should start with http:// or https://\033[0m")
                add_https = input("\033[96mAdd https:// automatically? (Y/n): \033[0m").strip().lower()
                if add_https != 'n':
                    url = f"https://{url}"
            
            return url
        except (EOFError, KeyboardInterrupt):
            print("\n\033[93m⚠️  Input cancelled\033[0m")
            return None

    def get_yes_no(self, prompt: str) -> bool:
        """Get yes/no confirmation from user."""
        try:
            response = input(f"\n\033[96m{prompt} (y/N): \033[0m").strip().lower()
            return response in ['y', 'yes']
        except (EOFError, KeyboardInterrupt):
            return False

    def pause(self):
        """Pause and wait for user input."""
        try:
            input("\n\033[90mPress Enter to continue...\033[0m")
        except (EOFError, KeyboardInterrupt):
            pass

    # ==================== TOOL 1: PING URL ====================
    def tool_ping(self):
        """Execute the ping URL tool."""
        clear_screen()
        print("\n" + "=" * 78)
        print("                          🌐 PING URL - Test Availability")
        print("=" * 78)
        
        url = self.get_url_input("Enter URL to ping")
        if not url:
            return
        
        logger.info(f"Tool: Ping URL - Target: {url}")
        print("\n\033[93m⏳ Pinging URL...\033[0m")
        
        try:
            result = ping_url(url)
            
            logger.info(f"Ping successful - Status: {result['status_code']}, Time: {result['response_time_ms']}ms")
            
            print("\n" + "=" * 78)
            print("                               RESULTS")
            print("=" * 78)
            print(f"\n\033[92m✓ Success!\033[0m")
            print(f"  URL:           {url}")
            print(f"  Status Code:   {result['status_code']}")
            print(f"  Response Time: {result['response_time_ms']} ms")
            print()
            
        except Exception as e:
            logger.error(f"Ping failed - URL: {url}, Error: {str(e)}")
            print(f"\n\033[91m✗ Error: {str(e)}\033[0m")
        
        self.pause()

    # ==================== TOOL 2: CLONE WEBSITE ====================
    def tool_clone(self):
        """Execute the website cloning tool."""
        clear_screen()
        print("\n" + "=" * 78)
        print("                      📋 CLONE WEBSITE - Download Resources")
        print("=" * 78)
        
        url = self.get_url_input("Enter website URL to clone")
        if not url:
            return
        
        # Get output directory
        default_output = get_clone_output_dir()
        try:
            print(f"\n\033[90mDefault output directory: {default_output}\033[0m")
            custom_dir = input("\033[96mCustom subdirectory name (press Enter for default): \033[0m").strip()
            if custom_dir:
                # User provided a custom name, use it within OUTPUT_DIR
                output_dir = str(get_output_dir() / custom_dir)
            else:
                # Use default from config - pass None to let clone service use its default
                output_dir = None
        except (EOFError, KeyboardInterrupt):
            print("\n\033[93m⚠️  Input cancelled\033[0m")
            return
        
        output_display = output_dir if output_dir else str(default_output)
        logger.info(f"Tool: Clone Website - Target: {url}, Output: {output_display}")
        print(f"\n\033[93m⏳ Cloning website to '{output_display}'...\033[0m\n")
        print("-" * 78)
        
        try:
            success = clone_website(url, output_dir)
            
            if success:
                logger.info(f"Clone successful - URL: {url}, Output: {output_display}")
                print("\n" + "=" * 78)
                print(f"\n\033[92m✓ Website cloned successfully to: {output_display}/\033[0m")
                print()
            else:
                logger.warning(f"Clone failed - URL: {url}")
                print("\n\033[91m✗ Failed to clone website\033[0m")
                
        except Exception as e:
            logger.error(f"Clone error - URL: {url}, Error: {str(e)}")
            print(f"\n\033[91m✗ Error: {str(e)}\033[0m")
        
        self.pause()

    # ==================== TOOL 3: DDOS TEST (OFFENSIVE) ====================
    def tool_ddos(self):
        """Execute the DDoS/rate limiting test tool."""
        clear_screen()
        print("\n" + "=" * 78)
        print("                  💥 DDOS TEST - Rate Limiting Analysis")
        print("=" * 78)
        print("\n\033[91m⚠️  OFFENSIVE TOOL - Ensure you have authorization!\033[0m")
        
        if not self.get_yes_no("Do you have authorization to test this target?"):
            print("\n\033[93m⚠️  Test cancelled - Authorization required\033[0m")
            self.pause()
            return
        
        url = self.get_url_input("Enter target URL")
        if not url:
            return
        
        # Get configuration
        try:
            period_input = input("\n\033[96mRequest interval in seconds (default: 1.0): \033[0m").strip()
            period = float(period_input) if period_input else 1.0
            
            max_input = input("\033[96mMaximum attempts (default: unlimited, press Enter): \033[0m").strip()
            max_attempts = int(max_input) if max_input else None
            
        except ValueError:
            print("\n\033[91m✗ Invalid input - using defaults\033[0m")
            period = 1.0
            max_attempts = None
        except (EOFError, KeyboardInterrupt):
            print("\n\033[93m⚠️  Input cancelled\033[0m")
            return
        
        print("\n" + "=" * 78)
        print(f"Starting DDoS test on: {url}")
        print(f"Interval: {period}s | Max attempts: {max_attempts or 'Unlimited'}")
        print("Press Ctrl+C to stop")
        print("=" * 78 + "\n")
        
        try:
            result = make_requests_until_blocked(
                url=url,
                period=period,
                max_attempts=max_attempts,
                randomize_params=True,
                verbose=True
            )
        except Exception as e:
            print(f"\n\033[91m✗ Error: {str(e)}\033[0m")
        
        self.pause()

    # ==================== TOOL 4: LOGIN TEST (OFFENSIVE) ====================
    def tool_login(self):
        """Execute the login credential testing tool."""
        clear_screen()
        print("\n" + "=" * 78)
        print("               🔐 LOGIN TEST - Credential Combination Testing")
        print("=" * 78)
        print("\n\033[91m⚠️  OFFENSIVE TOOL - Ensure you have authorization!\033[0m")
        
        if not self.get_yes_no("Do you have authorization to test this target?"):
            print("\n\033[93m⚠️  Test cancelled - Authorization required\033[0m")
            self.pause()
            return
        
        url = self.get_url_input("Enter login page URL")
        if not url:
            return
        
        # Get emails
        print("\n\033[96mEnter email addresses to test (comma-separated):\033[0m")
        print("\033[90mExample: admin@site.com, user@site.com, test@site.com\033[0m")
        try:
            emails_input = input("\033[96mEmails: \033[0m").strip()
            if not emails_input:
                print("\n\033[91m✗ Error: At least one email is required\033[0m")
                self.pause()
                return
            emails = [e.strip() for e in emails_input.split(',') if e.strip()]
        except (EOFError, KeyboardInterrupt):
            print("\n\033[93m⚠️  Input cancelled\033[0m")
            return
        
        # Get password keywords
        print("\n\033[96mEnter password keywords (comma-separated):\033[0m")
        print("\033[90mExample: password, admin, welcome\033[0m")
        try:
            keywords_input = input("\033[96mKeywords: \033[0m").strip()
            if not keywords_input:
                print("\n\033[91m✗ Error: At least one keyword is required\033[0m")
                self.pause()
                return
            keywords = [k.strip() for k in keywords_input.split(',') if k.strip()]
        except (EOFError, KeyboardInterrupt):
            print("\n\033[93m⚠️  Input cancelled\033[0m")
            return
        
        # Get delay
        try:
            delay_input = input("\n\033[96mDelay between attempts in seconds (default: 1.0): \033[0m").strip()
            delay = float(delay_input) if delay_input else 1.0
            
            max_input = input("\033[96mMaximum attempts (default: unlimited, press Enter): \033[0m").strip()
            max_attempts = int(max_input) if max_input else None
        except ValueError:
            print("\n\033[91m✗ Invalid input - using defaults\033[0m")
            delay = 1.0
            max_attempts = None
        except (EOFError, KeyboardInterrupt):
            print("\n\033[93m⚠️  Input cancelled\033[0m")
            return
        
        print("\n" + "=" * 78)
        print(f"Starting login test on: {url}")
        print(f"Emails: {len(emails)} | Keywords: {len(keywords)} | Delay: {delay}s")
        print("Press Ctrl+C to stop")
        print("=" * 78 + "\n")
        
        try:
            result = attempt_credential_combinations(
                url=url,
                emails=emails,
                keywords=keywords,
                delay=delay,
                max_attempts=max_attempts,
                verbose=True
            )
        except Exception as e:
            print(f"\n\033[91m✗ Error: {str(e)}\033[0m")
        
        self.pause()

    # ==================== MAIN RUN LOOP ====================
    def run(self):
        """Run the interactive menu."""
        clear_screen()
        print_banner()
        print_warning()
        
        if not self.get_yes_no("\nDo you acknowledge the legal warning and agree to use these tools responsibly?"):
            print("\n\033[93m⚠️  You must acknowledge the warning to continue.\033[0m")
            print("\033[90mExiting...\033[0m\n")
            sys.exit(0)
        
        while self.running:
            clear_screen()
            print_banner()
            self.display_main_menu()
            
            choice = self.get_choice()
            
            if choice == "1":
                self.tool_ping()
            elif choice == "2":
                self.tool_clone()
            elif choice == "3":
                self.tool_ddos()
            elif choice == "4":
                self.tool_login()
            elif choice == "0":
                self.running = False
                clear_screen()
                print("\n\033[92m" + "=" * 78 + "\033[0m")
                print("\033[92m                    Thank you for using PenWeb!\033[0m")
                print("\033[92m                         Stay safe. Stay legal.\033[0m")
                print("\033[92m" + "=" * 78 + "\033[0m\n")
            else:
                print("\n\033[91m✗ Invalid choice. Please select 0-4.\033[0m")
                self.pause()


def start_cli():
    """Start the CLI application."""
    try:
        logger.info("PenWeb CLI started")
        menu = PentestMenu()
        menu.run()
        logger.info("PenWeb CLI exited normally")
    except KeyboardInterrupt:
        logger.warning("Application interrupted by user")
        print("\n\n\033[93m⚠️  Application interrupted by user\033[0m")
        print("\033[90mExiting...\033[0m\n")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error in CLI: {str(e)}")
        print(f"\n\033[91m✗ Fatal error: {str(e)}\033[0m\n")
        sys.exit(1)

