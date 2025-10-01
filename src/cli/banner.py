"""ASCII art banner for the CLI."""

BANNER = """
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║         ██████╗ ███████╗███╗   ██╗██╗    ██╗███████╗██████╗            ║
║         ██╔══██╗██╔════╝████╗  ██║██║    ██║██╔════╝██╔══██╗           ║
║         ██████╔╝█████╗  ██╔██╗ ██║██║ █╗ ██║█████╗  ██████╔╝           ║
║         ██╔═══╝ ██╔══╝  ██║╚██╗██║██║███╗██║██╔══╝  ██╔══██╗           ║
║         ██║     ███████╗██║ ╚████║╚███╔███╔╝███████╗██████╔╝           ║
║         ╚═╝     ╚══════╝╚═╝  ╚═══╝ ╚══╝╚══╝ ╚══════╝╚═════╝            ║
║                                                                          ║
║                  Website Penetration Testing Toolkit                    ║
║                      v1.0 - Security Testing Suite                      ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

WARNING = """
╔══════════════════════════════════════════════════════════════════════════╗
║                          ⚠️  LEGAL WARNING ⚠️                            ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  These tools are designed for AUTHORIZED SECURITY TESTING ONLY.          ║
║                                                                          ║
║  • Only use on systems you OWN or have EXPLICIT PERMISSION to test       ║
║  • Unauthorized access to computer systems is ILLEGAL                    ║
║  • You are SOLELY RESPONSIBLE for your actions                           ║
║  • The authors assume NO LIABILITY for misuse of these tools             ║
║                                                                          ║
║  By continuing, you acknowledge you have proper authorization.           ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
"""


def print_banner():
    """Print the ASCII art banner."""
    print("\033[96m" + BANNER + "\033[0m")  # Cyan color


def print_warning():
    """Print the legal warning."""
    print("\033[93m" + WARNING + "\033[0m")  # Yellow color


def clear_screen():
    """Clear the terminal screen."""
    import os
    os.system('clear' if os.name == 'posix' else 'cls')

