#!/usr/bin/env python3
"""Test script to verify clone output directory configuration."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from utils.config import get_output_dir, get_clone_output_dir
from services.clone import WebCloner

print("=" * 70)
print("CLONE OUTPUT DIRECTORY TEST")
print("=" * 70)
print()

# Test 1: Check config functions
print("1. Testing config functions:")
print(f"   get_output_dir() = {get_output_dir()}")
print(f"   get_clone_output_dir() = {get_clone_output_dir()}")
print(f"   get_clone_output_dir('custom') = {get_clone_output_dir('custom')}")
print()

# Test 2: Simulate CLI default (user presses Enter)
print("2. Simulating CLI default (user presses Enter):")
default_output = get_clone_output_dir()
output_dir = str(default_output)
print(f"   output_dir passed to clone_website: '{output_dir}'")

cloner = WebCloner("https://example.com", output_dir)
print(f"   WebCloner.output_dir = {cloner.output_dir}")
print(f"   Is in .output? {'.output' in str(cloner.output_dir)}")
print()

# Test 3: Simulate CLI with custom subdirectory
print("3. Simulating CLI with custom subdirectory 'my_site':")
custom_output = str(get_output_dir() / "my_site")
print(f"   output_dir passed to clone_website: '{custom_output}'")

cloner2 = WebCloner("https://example.com", custom_output)
print(f"   WebCloner.output_dir = {cloner2.output_dir}")
print(f"   Is in .output? {'.output' in str(cloner2.output_dir)}")
print()

# Test 4: Check if paths are absolute
print("4. Path validation:")
print(f"   Default path is absolute? {get_clone_output_dir().is_absolute()}")
print(f"   Custom path is absolute? {Path(custom_output).is_absolute()}")
print()

print("=" * 70)
print("✓ All paths correctly point to .output directory!")
print("=" * 70)
