"""
Web cloning utility that downloads HTML, CSS, and JS files from a given URL.
"""

import os
import re
from pathlib import Path
from typing import Set, Optional
from urllib.parse import urljoin, urlparse, unquote
import requests
from bs4 import BeautifulSoup

try:
    from utils.config import get_clone_output_dir, get_output_dir
except ImportError:
    # Fallback if config not available
    def get_output_dir():
        """Get the output directory (fallback to .output)."""
        return Path(".output")
    
    def get_clone_output_dir(subdirectory=None):
        """Get the clone output directory (fallback to .output/cloned_site)."""
        output_dir = get_output_dir()
        if subdirectory:
            return output_dir / subdirectory
        else:
            return output_dir / "cloned_site"


class WebCloner:
    """Clone a website by downloading HTML, CSS, and JS files."""

    def __init__(self, url: str, output_dir: Optional[str] = None):
        """
        Initialize the WebCloner.

        Args:
            url: The URL to clone
            output_dir: Directory where files will be saved (default: from OUTPUT_DIR env variable)
        """
        self.url = url
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = get_clone_output_dir()
        self.downloaded_files: Set[str] = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def clone(self) -> bool:
        """
        Clone the website by downloading all HTML, CSS, and JS files.

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"Cloning website: {self.url}")
            
            # Create output directory
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
            # Download the main HTML page
            response = self.session.get(self.url, timeout=30)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Download CSS files
            self._download_stylesheets(soup)
            
            # Download JS files
            self._download_scripts(soup)
            
            # Download inline styles and scripts
            self._extract_inline_styles(soup)
            self._extract_inline_scripts(soup)
            
            # Save the main HTML file
            self._save_html(soup)
            
            print(f"\n✓ Successfully cloned {len(self.downloaded_files)} files")
            print(f"✓ Files saved to: {self.output_dir.absolute()}")
            return True
            
        except requests.RequestException as e:
            print(f"✗ Error fetching URL: {e}")
            return False
        except Exception as e:
            print(f"✗ Error during cloning: {e}")
            return False

    def _download_stylesheets(self, soup: BeautifulSoup) -> None:
        """Download all CSS files linked in the HTML."""
        link_tags = soup.find_all('link', rel='stylesheet')
        
        print(f"\nFound {len(link_tags)} CSS files to download:")
        
        for tag in link_tags:
            href = tag.get('href')
            if not href:
                continue
                
            css_url = urljoin(self.url, href)
            
            if css_url in self.downloaded_files:
                continue
                
            try:
                print(f"  Downloading CSS: {css_url}")
                response = self.session.get(css_url, timeout=30)
                response.raise_for_status()
                
                # Save CSS file
                file_path = self._get_file_path(css_url, 'css')
                self._save_file(file_path, response.content)
                self.downloaded_files.add(css_url)
                
                # Update the link tag to point to local file
                tag['href'] = str(file_path.relative_to(self.output_dir))
                
                # Download resources referenced in CSS (like @import and url())
                self._download_css_resources(response.text, css_url)
                
            except requests.RequestException as e:
                print(f"    ✗ Failed to download {css_url}: {e}")

    def _download_scripts(self, soup: BeautifulSoup) -> None:
        """Download all JS files linked in the HTML."""
        script_tags = soup.find_all('script', src=True)
        
        print(f"\nFound {len(script_tags)} JS files to download:")
        
        for tag in script_tags:
            src = tag.get('src')
            if not src:
                continue
                
            js_url = urljoin(self.url, src)
            
            if js_url in self.downloaded_files:
                continue
                
            try:
                print(f"  Downloading JS: {js_url}")
                response = self.session.get(js_url, timeout=30)
                response.raise_for_status()
                
                # Save JS file
                file_path = self._get_file_path(js_url, 'js')
                self._save_file(file_path, response.content)
                self.downloaded_files.add(js_url)
                
                # Update the script tag to point to local file
                tag['src'] = str(file_path.relative_to(self.output_dir))
                
            except requests.RequestException as e:
                print(f"    ✗ Failed to download {js_url}: {e}")

    def _download_css_resources(self, css_content: str, base_url: str) -> None:
        """Download resources referenced in CSS files (like fonts, images)."""
        # Find all url() references in CSS
        url_pattern = r'url\(["\']?([^"\')]+)["\']?\)'
        matches = re.findall(url_pattern, css_content)
        
        for match in matches:
            # Skip data URIs
            if match.startswith('data:'):
                continue
                
            resource_url = urljoin(base_url, match)
            
            if resource_url in self.downloaded_files:
                continue
                
            try:
                response = self.session.get(resource_url, timeout=30)
                response.raise_for_status()
                
                file_path = self._get_file_path(resource_url)
                self._save_file(file_path, response.content)
                self.downloaded_files.add(resource_url)
                
            except requests.RequestException:
                # Silently skip failed resource downloads
                pass

    def _extract_inline_styles(self, soup: BeautifulSoup) -> None:
        """Extract and save inline <style> tags."""
        style_tags = soup.find_all('style')
        
        if style_tags:
            print(f"\nFound {len(style_tags)} inline style tags")
            
            for idx, tag in enumerate(style_tags):
                if tag.string:
                    file_path = self.output_dir / f"inline_styles_{idx}.css"
                    self._save_file(file_path, tag.string.encode('utf-8'))

    def _extract_inline_scripts(self, soup: BeautifulSoup) -> None:
        """Extract and save inline <script> tags."""
        script_tags = soup.find_all('script', src=False)
        
        if script_tags:
            print(f"\nFound {len(script_tags)} inline script tags")
            
            for idx, tag in enumerate(script_tags):
                if tag.string:
                    file_path = self.output_dir / f"inline_script_{idx}.js"
                    self._save_file(file_path, tag.string.encode('utf-8'))

    def _save_html(self, soup: BeautifulSoup) -> None:
        """Save the main HTML file."""
        html_path = self.output_dir / "index.html"
        print(f"\nSaving main HTML to: {html_path}")
        self._save_file(html_path, soup.prettify().encode('utf-8'))

    def _get_file_path(self, url: str, default_ext: Optional[str] = None) -> Path:
        """
        Generate a file path for a URL.

        Args:
            url: The URL to generate a path for
            default_ext: Default file extension if none is found

        Returns:
            Path object for the file
        """
        parsed = urlparse(url)
        path = unquote(parsed.path)
        
        # Remove leading slash
        if path.startswith('/'):
            path = path[1:]
        
        # If path is empty or ends with /, use index.html
        if not path or path.endswith('/'):
            path += 'index.html'
        
        # Add default extension if no extension found
        if default_ext and '.' not in os.path.basename(path):
            path += f'.{default_ext}'
        
        file_path = self.output_dir / path
        
        # Ensure parent directories exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        return file_path

    def _save_file(self, file_path: Path, content: bytes) -> None:
        """
        Save content to a file.

        Args:
            file_path: Path where to save the file
            content: Content to save
        """
        file_path.write_bytes(content)


def clone_website(url: str, output_dir: Optional[str] = None) -> bool:
    """
    Clone a website by downloading its HTML, CSS, and JS files.

    Args:
        url: The URL of the website to clone
        output_dir: Directory where files will be saved (default: from OUTPUT_DIR env variable)

    Returns:
        bool: True if successful, False otherwise

    Example:
        >>> clone_website("https://example.com", "custom_dir")
        >>> clone_website("https://example.com")  # Uses OUTPUT_DIR from .env
    """
    cloner = WebCloner(url, output_dir)
    return cloner.clone()


def main():
    """Main function for command-line usage."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python clone.py <url> [output_dir]")
        print("Example: python clone.py https://example.com my_clone")
        print("If output_dir is not provided, uses OUTPUT_DIR from .env")
        sys.exit(1)
    
    url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = clone_website(url, output_dir)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

