# AWS Lambda - URL Pinger

This Lambda function processes SQS messages containing URLs and pings them via HTTP requests.

## Features

- Processes SQS events with URLs
- Supports both plain URL strings and JSON formatted messages
- Returns detailed results including response times and status codes
- Comprehensive error handling and logging
- No external dependencies (uses standard library only)

## SQS Message Format

The Lambda accepts two message formats:

### Format 1: Plain URL

```
https://example.com
```

### Format 2: JSON with URL field

```json
{
  "url": "https://example.com"
}
```

## Configuration

### Lambda Settings

- **Runtime**: Python 3.9+ (or later)
- **Timeout**: 30 seconds (recommended)
- **Memory**: 128 MB (minimum)

### IAM Permissions Required

The Lambda execution role needs:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage",
        "sqs:GetQueueAttributes"
      ],
      "Resource": "arn:aws:sqs:*:*:your-queue-name"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

### SQS Trigger Configuration

1. Create an SQS queue
2. Configure the queue as a trigger for this Lambda
3. Set batch size (e.g., 10 messages)
4. Enable "Report batch item failures" for partial batch handling

## Deployment

### Option 1: AWS Console

1. Zip the `lambda.py` file
2. Upload to AWS Lambda via the console
3. Set handler to `lambda.lambda_handler`

### Option 2: AWS CLI

```bash
zip function.zip lambda.py
aws lambda create-function \
  --function-name url-pinger \
  --runtime python3.9 \
  --role arn:aws:iam::YOUR_ACCOUNT:role/YOUR_ROLE \
  --handler lambda.lambda_handler \
  --zip-file fileb://function.zip \
  --timeout 30
```

### Option 3: Infrastructure as Code

Use AWS SAM, Terraform, or CloudFormation to deploy.

## Response Format

The Lambda returns a dictionary with processing results:

```json
{
  "statusCode": 200,
  "total_processed": 2,
  "successful": 1,
  "failed": 1,
  "successful_pings": [
    {
      "message_id": "abc123",
      "url": "https://example.com",
      "status_code": 200,
      "response_time_ms": 145
    }
  ],
  "failed_pings": [
    {
      "message_id": "def456",
      "url": "https://invalid-url",
      "error": "Failed to connect to https://invalid-url: [Errno -2] Name or service not known"
    }
  ]
}
```

## Testing

### Test Event (SQS Event Format)

```json
{
  "Records": [
    {
      "messageId": "test-message-1",
      "body": "https://www.google.com"
    },
    {
      "messageId": "test-message-2",
      "body": "{\"url\": \"https://www.amazon.com\"}"
    }
  ]
}
```

### Local Testing

```python
from lambda import lambda_handler

# Test event
event = {
    "Records": [
        {
            "messageId": "test-1",
            "body": "https://www.google.com"
        }
    ]
}

result = lambda_handler(event, None)
print(result)
```

## Monitoring

Monitor the Lambda function using:

- CloudWatch Logs for detailed execution logs
- CloudWatch Metrics for invocation counts and errors
- X-Ray for distributed tracing (if enabled)

## Notes

- The function uses a 10-second timeout for each URL ping
- HTTP and HTTPS URLs are supported
- The function validates URLs before attempting to ping them
- Both successful and failed pings are logged and returned in the response
