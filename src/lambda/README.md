# AWS Lambda - URL Pinger

This Lambda function processes SQS messages containing URLs and pings them via HTTP requests. It's designed for monitoring website availability, measuring response times, and validating endpoint health.

## Features

- Processes SQS events with URLs in batch mode
- Supports both plain URL strings and JSON formatted messages
- Returns detailed results including response times and status codes
- Comprehensive error handling and logging
- Modular design with separate utility functions
- Uses Python standard library (urllib) for HTTP requests

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

### Prerequisites

The Lambda function requires these files:
- `src/lambda/entrypoint.py` - Main Lambda handler
- `src/utils/ping.py` - URL ping utility

### Option 1: AWS Console

1. Create a deployment package:
   ```bash
   cd /home/kali/labs/blue-yellow
   mkdir -p lambda-package/utils
   cp src/lambda/entrypoint.py lambda-package/
   cp src/utils/ping.py lambda-package/utils/
   cd lambda-package
   zip -r ../lambda-function.zip .
   cd ..
   rm -rf lambda-package
   ```

2. Upload `lambda-function.zip` to AWS Lambda via the console
3. Set handler to `entrypoint.lambda_handler`
4. Configure runtime as Python 3.9 or later

### Option 2: AWS CLI

```bash
# Create deployment package
cd /home/kali/labs/blue-yellow
mkdir -p lambda-package/utils
cp src/lambda/entrypoint.py lambda-package/
cp src/utils/ping.py lambda-package/utils/
cd lambda-package
zip -r ../lambda-function.zip .
cd ..

# Deploy to AWS
aws lambda create-function \
  --function-name url-pinger \
  --runtime python3.9 \
  --role arn:aws:iam::YOUR_ACCOUNT:role/YOUR_ROLE \
  --handler entrypoint.lambda_handler \
  --zip-file fileb://lambda-function.zip \
  --timeout 30 \
  --memory-size 128

# Clean up
rm -rf lambda-package
```

### Option 3: Infrastructure as Code

Use AWS SAM, Terraform, or CloudFormation to deploy.

**Example Terraform:**
```hcl
resource "aws_lambda_function" "url_pinger" {
  filename      = "lambda-function.zip"
  function_name = "url-pinger"
  role          = aws_iam_role.lambda_role.arn
  handler       = "entrypoint.lambda_handler"
  runtime       = "python3.9"
  timeout       = 30
  memory_size   = 128
}
```

**Example AWS SAM template.yaml:**
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Resources:
  UrlPingerFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: entrypoint.lambda_handler
      Runtime: python3.9
      CodeUri: lambda-package/
      Timeout: 30
      MemorySize: 128
      Events:
        SQSEvent:
          Type: SQS
          Properties:
            Queue: !GetAtt UrlQueue.Arn
            BatchSize: 10
```

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

Run the included test suite:

```bash
# From project root
cd /home/kali/labs/blue-yellow
poetry run python test/test_lambda.py
```

Or test manually in Python:

```python
import sys
sys.path.insert(0, '/home/kali/labs/blue-yellow/src')

from lambda.entrypoint import lambda_handler

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

### Unit Tests

The project includes comprehensive unit tests in `test/test_lambda.py`:

- ✓ Single plain URL
- ✓ JSON format URL
- ✓ Multiple URLs in batch
- ✓ Invalid URL handling
- ✓ Unreachable URL handling
- ✓ Mixed success and failure scenarios

Run tests:
```bash
poetry run python test/test_lambda.py
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
