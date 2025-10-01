"""
Simple test script for the URL Pinger Lambda function.
Run with: python test_lambda.py
"""

import json
import sys
from pathlib import Path
import importlib.util

# Add the current directory to the path
sys.path.insert(0, str(Path(__file__).parent))

# Import lambda handler from lambda.py file
# Using importlib to avoid 'lambda' reserved keyword issue
lambda_file = Path(__file__).parent / "lambda.py"
spec = importlib.util.spec_from_file_location("lambda_module", lambda_file)
lambda_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lambda_module)
lambda_handler = lambda_module.lambda_handler


def test_single_url():
    """Test with a single plain URL in SQS message"""
    print("\n=== Test 1: Single Plain URL ===")
    
    event = {
        "Records": [
            {
                "messageId": "test-msg-1",
                "body": "https://www.google.com"
            }
        ]
    }
    
    result = lambda_handler(event, None)
    print(f"Result: {json.dumps(result, indent=2)}")
    assert result['total_processed'] == 1
    assert result['successful'] >= 0
    print("✓ Test passed")


def test_json_format():
    """Test with JSON formatted URL in SQS message"""
    print("\n=== Test 2: JSON Format URL ===")
    
    event = {
        "Records": [
            {
                "messageId": "test-msg-2",
                "body": json.dumps({"url": "https://www.amazon.com"})
            }
        ]
    }
    
    result = lambda_handler(event, None)
    print(f"Result: {json.dumps(result, indent=2)}")
    assert result['total_processed'] == 1
    print("✓ Test passed")


def test_multiple_urls():
    """Test with multiple URLs in batch"""
    print("\n=== Test 3: Multiple URLs ===")
    
    event = {
        "Records": [
            {
                "messageId": "test-msg-3",
                "body": "https://www.github.com"
            },
            {
                "messageId": "test-msg-4",
                "body": json.dumps({"url": "https://www.python.org"})
            },
            {
                "messageId": "test-msg-5",
                "body": "https://httpbin.org/status/200"
            }
        ]
    }
    
    result = lambda_handler(event, None)
    print(f"Result: {json.dumps(result, indent=2)}")
    assert result['total_processed'] == 3
    print("✓ Test passed")


def test_invalid_url():
    """Test with an invalid URL"""
    print("\n=== Test 4: Invalid URL ===")
    
    event = {
        "Records": [
            {
                "messageId": "test-msg-6",
                "body": "not-a-valid-url"
            }
        ]
    }
    
    result = lambda_handler(event, None)
    print(f"Result: {json.dumps(result, indent=2)}")
    assert result['failed'] == 1
    assert 'Invalid URL format' in result['failed_pings'][0]['error']
    print("✓ Test passed")


def test_unreachable_url():
    """Test with an unreachable URL"""
    print("\n=== Test 5: Unreachable URL ===")
    
    event = {
        "Records": [
            {
                "messageId": "test-msg-7",
                "body": "https://this-domain-does-not-exist-12345.com"
            }
        ]
    }
    
    result = lambda_handler(event, None)
    print(f"Result: {json.dumps(result, indent=2)}")
    assert result['failed'] == 1
    print("✓ Test passed")


def test_mixed_success_failure():
    """Test with mix of valid and invalid URLs"""
    print("\n=== Test 6: Mixed Success and Failure ===")
    
    event = {
        "Records": [
            {
                "messageId": "test-msg-8",
                "body": "https://www.google.com"
            },
            {
                "messageId": "test-msg-9",
                "body": "invalid-url"
            }
        ]
    }
    
    result = lambda_handler(event, None)
    print(f"Result: {json.dumps(result, indent=2)}")
    assert result['total_processed'] == 2
    assert result['statusCode'] == 207  # Multi-Status
    print("✓ Test passed")


if __name__ == "__main__":
    print("Starting Lambda Function Tests...")
    print("=" * 50)
    
    try:
        test_single_url()
        test_json_format()
        test_multiple_urls()
        test_invalid_url()
        test_unreachable_url()
        test_mixed_success_failure()
        
        print("\n" + "=" * 50)
        print("✓ All tests passed successfully!")
        print("=" * 50)
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")

