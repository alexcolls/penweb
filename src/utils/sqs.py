"""Utility library for AWS Lambda functions handling SQS messages."""

import json
import logging
import re
from typing import Dict, Any, Optional, Union
from urllib.parse import urlparse

# Configure logging
logger = logging.getLogger(__name__)


def parse_sqs_message(message_body: str) -> Dict[str, Any]:
    """
    Parse SQS message body and extract instruction dictionary.

    Expected message formats:
    1. Plain URL string: "https://example.com"
    2. JSON with url and action: {"url": "https://example.com", "action": "ping"}
    3. JSON with url only: {"url": "https://example.com"} (defaults to ping)
    
    Args:
        message_body: Raw SQS message body
        
    Returns:
        Dictionary with parsed instruction:
        {
            "status": 0|1,  # 0 = wrong message, 1 = valid
            "url": str,     # URL (if valid)
            "action": str,  # action (ping/clone/ddos/attempt_login)
            "error": str    # error message (if status = 0)
        }
    """
    if not message_body or not message_body.strip():
        return {
            "status": 0,
            "url": None,
            "action": None,
            "error": "Empty message body"
        }
    
    message_body = message_body.strip()
    
    # Try to parse as JSON first
    try:
        body_json = json.loads(message_body)
        
        # Handle JSON format
        if isinstance(body_json, dict):
            url = body_json.get('url', '').strip()
            action = body_json.get('action', 'ping').strip().lower()
            
            # Validate URL
            url_validation = validate_url(url)
            if not url_validation["valid"]:
                return {
                    "status": 0,
                    "url": None,
                    "action": None,
                    "error": f"Invalid URL in JSON: {url_validation['error']}"
                }
            
            # Validate action
            action_validation = validate_action(action)
            if not action_validation["valid"]:
                return {
                    "status": 0,
                    "url": url,
                    "action": None,
                    "error": f"Invalid action: {action_validation['error']}"
                }
            
            return {
                "status": 1,
                "url": url,
                "action": action,
                "error": None
            }
        
        # Handle JSON array or other types
        elif isinstance(body_json, (list, str, int, float, bool)):
            return {
                "status": 0,
                "url": None,
                "action": None,
                "error": f"Invalid JSON format: expected object, got {type(body_json).__name__}"
            }
            
    except json.JSONDecodeError:
        # Not JSON, treat as plain URL string
        url = message_body.strip()
        
        # Validate URL
        url_validation = validate_url(url)
        if not url_validation["valid"]:
            return {
                "status": 0,
                "url": None,
                "action": None,
                "error": f"Invalid URL format: {url_validation['error']}"
            }
        
        # Default action is 'ping' for plain URLs
        return {
            "status": 1,
            "url": url,
            "action": "ping",
            "error": None
        }
    
    except Exception as e:
        return {
            "status": 0,
            "url": None,
            "action": None,
            "error": f"Unexpected error parsing message: {str(e)}"
        }


def validate_url(url: str) -> Dict[str, Union[bool, str]]:
    """
    Validate URL format.
    
    Args:
        url: URL string to validate
        
    Returns:
        Dictionary with validation result:
        {
            "valid": bool,
            "error": str (if invalid)
        }
    """
    if not url:
        return {
            "valid": False,
            "error": "URL is empty"
        }
    
    url = url.strip()
    
    # Check if URL starts with http:// or https://
    if not url.startswith(('http://', 'https://')):
        return {
            "valid": False,
            "error": "URL must start with http:// or https://"
        }
    
    # Parse URL to validate format
    try:
        parsed = urlparse(url)
        
        # Check if URL has a valid netloc (domain)
        if not parsed.netloc:
            return {
                "valid": False,
                "error": "URL must have a valid domain"
            }
        
        # Basic domain validation (at least one dot for TLD)
        if '.' not in parsed.netloc:
            return {
                "valid": False,
                "error": "URL must have a valid domain with TLD"
            }
        
        return {
            "valid": True,
            "error": None
        }
        
    except Exception as e:
        return {
            "valid": False,
            "error": f"Invalid URL format: {str(e)}"
        }


def validate_action(action: str) -> Dict[str, Union[bool, str]]:
    """
    Validate action parameter.
    
    Args:
        action: Action string to validate
        
    Returns:
        Dictionary with validation result:
        {
            "valid": bool,
            "error": str (if invalid)
        }
    """
    if not action:
        return {
            "valid": False,
            "error": "Action is empty"
        }
    
    action = action.strip().lower()
    valid_actions = ['ping', 'clone', 'ddos', 'attempt_login']
    
    if action not in valid_actions:
        return {
            "valid": False,
            "error": f"Invalid action '{action}'. Must be one of: {', '.join(valid_actions)}"
        }
    
    return {
        "valid": True,
        "error": None
    }


def instruction_parser(message_body: str) -> Dict[str, Any]:
    """
    Main instruction parser that combines all validation logic.
    
    This is the main function to use for parsing SQS messages.
    
    Args:
        message_body: Raw SQS message body
        
    Returns:
        Dictionary with complete instruction:
        {
            "status": 0|1,  # 0 = wrong message, 1 = right url & action
            "url": str,     # URL (if valid)
            "action": str,  # action (if valid)
            "error": str    # error message (if status = 0)
        }
    """
    try:
        result = parse_sqs_message(message_body)
        
        # Log the result for debugging
        if result["status"] == 1:
            logger.info(f"Successfully parsed instruction: URL={result['url']}, Action={result['action']}")
        else:
            logger.warning(f"Failed to parse instruction: {result['error']}")
        
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error in instruction_parser: {str(e)}")
        return {
            "status": 0,
            "url": None,
            "action": None,
            "error": f"Parser error: {str(e)}"
        }


def extract_message_metadata(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract metadata from SQS record.
    
    Args:
        record: SQS record dictionary
        
    Returns:
        Dictionary with message metadata:
        {
            "message_id": str,
            "receipt_handle": str,
            "source": str,
            "timestamp": str
        }
    """
    return {
        "message_id": record.get('messageId', 'unknown'),
        "receipt_handle": record.get('receiptHandle', ''),
        "source": record.get('eventSource', 'unknown'),
        "timestamp": record.get('attributes', {}).get('SentTimestamp', '')
    }


def create_response(status_code: int, message: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Create standardized response for Lambda function.
    
    Args:
        status_code: HTTP status code
        message: Response message
        data: Optional additional data
        
    Returns:
        Standardized response dictionary
    """
    response = {
        "statusCode": status_code,
        "message": message
    }
    
    if data:
        response.update(data)
    
    return response
