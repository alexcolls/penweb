"""AWS Lambda function to ping URLs from SQS messages."""
import json
import logging
from typing import Dict, Any

from utils.ping import ping_url

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler that processes SQS messages containing URLs and pings them.
    
    Expected SQS message format:
    - Body can be a plain URL string
    - Or JSON with a 'url' field: {"url": "https://example.com"}
    
    Args:
        event: SQS event containing Records
        context: Lambda context object
        
    Returns:
        Dictionary with processing results
    """
    successful_pings = []
    failed_pings = []
    
    # Process each SQS record
    for record in event.get('Records', []):
        message_id = record.get('messageId', 'unknown')
        message_body = record.get('body', '')
        
        try:
            # Try to parse as JSON first
            try:
                body_json = json.loads(message_body)
                url = body_json.get('url', message_body)
            except (json.JSONDecodeError, AttributeError):
                # If not JSON, treat the entire body as URL
                url = message_body.strip()
            
            logger.info(f"Processing message {message_id} with URL: {url}")
            
            # Validate URL
            if not url or not url.startswith(('http://', 'https://')):
                raise ValueError(f"Invalid URL format: {url}")
            
            # Ping the URL
            response = ping_url(url)
            
            successful_pings.append({
                'message_id': message_id,
                'url': url,
                'status_code': response['status_code'],
                'response_time_ms': response['response_time_ms']
            })
            
            logger.info(f"Successfully pinged {url} - Status: {response['status_code']}")
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Failed to process message {message_id}: {error_msg}")
            failed_pings.append({
                'message_id': message_id,
                'url': url if 'url' in locals() else 'unknown',
                'error': error_msg
            })
    
    # Return summary
    result = {
        'statusCode': 200 if not failed_pings else 207,  # 207 Multi-Status if partial success
        'total_processed': len(event.get('Records', [])),
        'successful': len(successful_pings),
        'failed': len(failed_pings),
        'successful_pings': successful_pings,
        'failed_pings': failed_pings
    }
    
    logger.info(f"Processing complete: {result['successful']} successful, {result['failed']} failed")
    
    return result

