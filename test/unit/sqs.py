#!/usr/bin/env python3
"""Test script to demonstrate the utility library functionality."""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from lib import instruction_parser, validate_url, validate_action

def test_instruction_parser():
    """Test the instruction_parser function with various inputs."""
    
    print("=== Testing instruction_parser ===\n")
    
    test_cases = [
        # Valid cases
        ("https://example.com", "Plain URL (should default to ping)"),
        ('{"url": "https://example.com"}', "JSON with URL only (should default to ping)"),
        ('{"url": "https://example.com", "action": "ping"}', "JSON with URL and ping action"),
        ('{"url": "https://example.com", "action": "clone"}', "JSON with URL and clone action"),
        ('{"url": "https://example.com", "action": "ddos"}', "JSON with URL and ddos action"),
        ('{"url": "https://example.com", "action": "attempt_login"}', "JSON with URL and attempt_login action"),
        
        # Invalid cases
        ("", "Empty message"),
        ("invalid-url", "Invalid URL format"),
        ('{"url": "invalid-url"}', "JSON with invalid URL"),
        ('{"url": "https://example.com", "action": "invalid_action"}', "JSON with invalid action"),
        ('{"invalid": "format"}', "JSON without URL field"),
        ('{"url": "https://example.com", "action": ""}', "JSON with empty action"),
        ('not-json', "Invalid JSON format"),
        ('[]', "JSON array instead of object"),
        ('"just-a-string"', "JSON string instead of object"),
    ]
    
    for message_body, description in test_cases:
        print(f"Test: {description}")
        print(f"Input: {message_body}")
        result = instruction_parser(message_body)
        print(f"Result: {result}")
        
        if result['status'] == 1:
            print(f"✅ Valid instruction - URL: {result['url']}, Action: {result['action']}")
        else:
            print(f"❌ Invalid instruction - Error: {result['error']}")
        
        print("-" * 60)


def test_validation_functions():
    """Test the individual validation functions."""
    
    print("\n=== Testing validation functions ===\n")
    
    # Test URL validation
    print("Testing validate_url:")
    url_tests = [
        "https://example.com",
        "http://test.org",
        "https://subdomain.example.com/path",
        "invalid-url",
        "",
        "ftp://example.com",
        "https://",
        "https://example",
    ]
    
    for url in url_tests:
        result = validate_url(url)
        status = "✅" if result['valid'] else "❌"
        print(f"  {status} {url}: {result}")
    
    print("\nTesting validate_action:")
    action_tests = [
        "ping",
        "clone", 
        "ddos",
        "attempt_login",
        "invalid_action",
        "",
        "PING",  # Should be converted to lowercase
        "Clone",  # Should be converted to lowercase
    ]
    
    for action in action_tests:
        result = validate_action(action)
        status = "✅" if result['valid'] else "❌"
        print(f"  {status} '{action}': {result}")


if __name__ == "__main__":
    test_instruction_parser()
    test_validation_functions()
    
    print("\n=== Summary ===")
    print("The utility library provides:")
    print("1. instruction_parser() - Main function to parse SQS messages")
    print("2. validate_url() - Validate URL format")
    print("3. validate_action() - Validate action parameter")
    print("4. extract_message_metadata() - Extract SQS record metadata")
    print("5. create_response() - Create standardized Lambda responses")
    print("\nReturn format:")
    print("- status: 0 = wrong message, 1 = right url & action")
    print("- url: Valid URL string (if status = 1)")
    print("- action: Valid action (ping/clone/ddos/attempt_login)")
    print("- error: Error message (if status = 0)")
